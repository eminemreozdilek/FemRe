import sys
from typing import Dict, List, Optional, Type, Tuple

import numpy as np
import pyvista as pv
from pyvista import CellType
from scipy import sparse
from scipy.spatial import cKDTree

from model.material import BaseMaterial
from model.elements import *
from model.data_class import *
from solver.result_editor import model_element_fields
from solver.linear_solver import solve_model
from solver.linear_solver import *


class Model:
    def __init__(self) -> None:
        self.components: List[ComponentData] = []
        self.nodes_by_id: Dict[int, NodeData] = {}
        self.elements_by_id: Dict[int, ElementData] = {}
        self.contact_constraint_sets: List[ContactData] = []
        self.constraint_equation_dict: Dict[int, list] = {}
        self.constraint_equation_data_list: List[ConstraintEquationData] = []
        self.lambda_constraint_equations: Dict[int, float] = {}
        self.next_node_id: int = 1
        self.next_element_id: int = 1
        self.u = None
        self.f = None

    @property
    def number_of_nodes(self) -> int:
        return len(self.nodes_by_id)

    @property
    def number_of_elements(self) -> int:
        return len(self.elements_by_id)

    @staticmethod
    def __remove_unconnected_points(
            mesh: pv.UnstructuredGrid,
    ) -> pv.UnstructuredGrid:
        """
        Return a new UnstructuredGrid where points not referenced by any cell
        are removed and connectivity is reindexed.

        This is safer than relying on plotting-side cleanup because the global
        node/element registration must only see actually used nodes.
        """
        if mesh.n_cells == 0:
            raise ValueError("Mesh has no cells.")

        original_points = np.asarray(mesh.points)
        if original_points.shape[0] == 0:
            raise ValueError("Mesh has no points.")

        # PyVista/VTK stores cells as:
        # [n0, p0_1, p0_2, ..., n1, p1_1, p1_2, ...]
        cell_array = np.asarray(mesh.cells)
        cell_types = np.asarray(mesh.celltypes)
        offset = np.asarray(mesh.offset)

        used_point_ids = []
        i = 0
        while i < len(cell_array):
            npts = int(cell_array[i])
            conn = cell_array[i + 1:i + 1 + npts]
            used_point_ids.append(conn)
            i += npts + 1

        used_point_ids = np.unique(np.concatenate(used_point_ids))

        # If nothing to remove, still return a deep copy for safety
        if used_point_ids.size == mesh.n_points:
            return mesh.copy(deep=True)

        # Old point id -> new point id
        new_id_from_old = -np.ones(mesh.n_points, dtype=int)
        new_id_from_old[used_point_ids] = np.arange(used_point_ids.size, dtype=int)

        new_points = original_points[used_point_ids]

        # Rebuild flattened VTK cell array with remapped node ids
        new_cells_list = []
        i = 0
        while i < len(cell_array):
            npts = int(cell_array[i])
            conn = cell_array[i + 1:i + 1 + npts]
            new_conn = new_id_from_old[conn]

            if np.any(new_conn < 0):
                raise RuntimeError("Connectivity remap failed while removing unused points.")

            new_cells_list.append(np.concatenate(([npts], new_conn)))
            i += npts + 1

        new_cells = np.concatenate(new_cells_list).astype(np.int64)

        cleaned_mesh = pv.UnstructuredGrid(offset, new_cells, cell_types, new_points)

        # Preserve point_data for used points only
        for key in mesh.point_data.keys():
            arr = np.asarray(mesh.point_data[key])
            if arr.shape[0] == mesh.n_points:
                cleaned_mesh.point_data[key] = arr[used_point_ids]

        # Preserve cell_data as-is
        for key in mesh.cell_data.keys():
            arr = np.asarray(mesh.cell_data[key])
            if arr.shape[0] == mesh.n_cells:
                cleaned_mesh.cell_data[key] = arr.copy()

        return cleaned_mesh

    def add_component(
            self,
            mesh: pv.UnstructuredGrid,
            material: BaseMaterial,
            name: Optional[str] = None,
    ) -> ComponentData:
        cleaned_mesh = self.__remove_unconnected_points(mesh)

        component_id = len(self.components) + 1
        component_name = name if name is not None else f"component_{component_id}"

        component = ComponentData(
            component_id=component_id,
            name=component_name,
            mesh=cleaned_mesh,
            material=material,
        )

        self.components.append(component)
        self.__register_component_nodes(component)
        self.__register_component_elements(component)
        return component

    def __register_component_nodes(self,
                                   component: ComponentData
                                   ) -> None:
        mesh = component.mesh
        number_of_points = mesh.n_points
        local_point_indices = np.arange(number_of_points, dtype=int)
        global_node_ids = np.arange(
            self.next_node_id,
            self.next_node_id + number_of_points,
            dtype=int,
        )
        for local_index, global_node_id in zip(local_point_indices, global_node_ids):
            coordinates = np.asarray(mesh.points[local_index], dtype=float)
            self.nodes_by_id[global_node_id] = NodeData(
                node_id=global_node_id,
                coordinates=coordinates,
                prescribed_displacement=np.full(3, np.nan),
                external_force=np.zeros(3),
            )
        mesh.point_data["global_node_id"] = global_node_ids
        self.next_node_id += number_of_points

    def __element_class_from_cell_type(self,
                                       cell_type: int,
                                       number_of_nodes: int,
                                       ) -> Optional[Type[FiniteElement]]:
        if cell_type == CellType.TETRA:
            if number_of_nodes != 4:
                raise ValueError("tetrahedral cell with incorrect node count")
            return TetrahedralElement
        if cell_type == CellType.QUADRATIC_TETRA:
            if number_of_nodes != 10:
                raise ValueError("quadratic tetrahedral cell with incorrect node count")
            return SecondOrderTetrahedralElement
        if cell_type == CellType.HEXAHEDRON:
            if number_of_nodes != 8:
                raise ValueError("hexahedral cell with incorrect node count")
            return HexahedralElement
        if cell_type == CellType.QUADRATIC_HEXAHEDRON:
            if number_of_nodes != 20:
                raise ValueError("quadratic hexahedral cell with incorrect node count")
            return SecondOrderHexahedralElement
        return None

    def __cell_spatial_dimension(self,
                                 cell_type: int
                                 ) -> int:
        if cell_type in (
                CellType.TETRA,
                CellType.QUADRATIC_TETRA,
                CellType.HEXAHEDRON,
                CellType.QUADRATIC_HEXAHEDRON,):
            return 3
        if cell_type in (
                CellType.TRIANGLE,
                CellType.QUADRATIC_TRIANGLE,
                CellType.QUAD,
                CellType.QUADRATIC_QUAD,
                CellType.BIQUADRATIC_QUAD,):
            return 2
        if cell_type in (CellType.LINE,):
            return 1
        return 0

    def __register_component_elements(self,
                                      component: ComponentData
                                      ) -> None:
        mesh = component.mesh
        cells = mesh.cells
        celltypes = mesh.celltypes
        global_node_ids = mesh.point_data["global_node_id"]
        number_of_cells = mesh.n_cells
        global_element_ids = np.full(number_of_cells, -1, dtype=int)
        component_ids = np.full(number_of_cells, component.component_id, dtype=int)
        pointer = 0
        for local_cell_index, cell_type in enumerate(celltypes):
            number_of_nodes = int(cells[pointer])
            connectivity = cells[pointer + 1: pointer + 1 + number_of_nodes]
            pointer += 1 + number_of_nodes
            element_class = self.__element_class_from_cell_type(
                cell_type=int(cell_type),
                number_of_nodes=number_of_nodes,
            )
            spatial_dimension = self.__cell_spatial_dimension(int(cell_type))
            if element_class is None or spatial_dimension != 3:
                continue
            element_node_ids = global_node_ids[connectivity]
            node_coordinates = np.array(
                [self.nodes_by_id[int(node_id)].coordinates for node_id in element_node_ids],
                dtype=float,
            )
            finite_element = element_class(
                nodes=node_coordinates,
                material=component.material,
            )
            global_element_id = self.next_element_id
            self.next_element_id += 1
            element_data = ElementData(
                element_id=global_element_id,
                component_id=component.component_id,
                node_ids=element_node_ids.astype(int),
                finite_element=finite_element,
                spatial_dimension=spatial_dimension,
            )
            self.elements_by_id[global_element_id] = element_data
            global_element_ids[local_cell_index] = global_element_id
        mesh.cell_data["global_element_id"] = global_element_ids
        mesh.cell_data["component_id"] = component_ids

    def add_contact_constraints(
            self,
            parent_node_id_array: np.ndarray,
            child_node_id_array: np.ndarray,
            contact_constraint_array: np.ndarray,
    ) -> ContactData:
        parent_node_id_array = np.asarray(parent_node_id_array, dtype=int)
        child_node_id_array = np.asarray(child_node_id_array, dtype=int)
        contact_constraint_array = np.asarray(contact_constraint_array, dtype=int)
        if parent_node_id_array.shape != child_node_id_array.shape:
            raise ValueError("parent_node_id_array and child_node_id_array must have the same shape")
        if contact_constraint_array.shape[0] != parent_node_id_array.shape[0]:
            raise ValueError("contact_constraint_array must have the same number of rows as node pairs")
        if contact_constraint_array.shape[1] != 3:
            raise ValueError("contact_constraint_array must be of shape (n, 3)")
        constraint_set = ContactData(
            parent_node_id_array=parent_node_id_array,
            child_node_id_array=child_node_id_array,
            contact_constraint_array=contact_constraint_array,
        )
        self.contact_constraint_sets.append(constraint_set)
        return constraint_set

    def set_constraint_equation(
            self,
            constraint_dict: Dict[int, list],
    ) -> None:
        if constraint_dict is None:
            constraint_dict = {}
        if not isinstance(constraint_dict, dict):
            raise TypeError("constraint_dict must be a dictionary of equation definitions")

        normalized_constraint_dict: Dict[int, list] = {}
        parsed_constraint_list: List[ConstraintEquationData] = []
        merge_tolerance = 1.0e-14

        for raw_constraint_eq_id in sorted(constraint_dict.keys()):
            if not isinstance(raw_constraint_eq_id, (int, np.integer)):
                raise TypeError("constraint equation id must be an integer")
            constraint_eq_id = int(raw_constraint_eq_id)
            if constraint_eq_id <= 0:
                raise ValueError("constraint equation id must be a positive integer")

            equation_definition = constraint_dict[raw_constraint_eq_id]
            if not isinstance(equation_definition, (list, tuple)):
                raise TypeError(f"constraint equation {constraint_eq_id} must be a list or tuple")
            if len(equation_definition) < 2:
                raise ValueError(
                    f"constraint equation {constraint_eq_id} must contain at least one term and one constant"
                )

            raw_terms = equation_definition[:-1]
            raw_constant = equation_definition[-1]
            try:
                equation_constant = float(raw_constant)
            except (TypeError, ValueError):
                raise TypeError(
                    f"constraint equation {constraint_eq_id} constant must be numeric"
                ) from None
            if not np.isfinite(equation_constant):
                raise ValueError(
                    f"constraint equation {constraint_eq_id} constant must be finite"
                )

            coefficient_by_dof: Dict[int, float] = {}
            for term_index, raw_term in enumerate(raw_terms):
                if not isinstance(raw_term, (list, tuple, np.ndarray)):
                    raise TypeError(
                        f"constraint equation {constraint_eq_id} term {term_index} must be [node_id, dof, coeff]"
                    )
                if len(raw_term) != 3:
                    raise ValueError(
                        f"constraint equation {constraint_eq_id} term {term_index} must have exactly 3 entries"
                    )

                raw_node_id, raw_dof, raw_coeff = raw_term

                if not isinstance(raw_node_id, (int, np.integer)):
                    raise TypeError(
                        f"constraint equation {constraint_eq_id} term {term_index} node_id must be an integer"
                    )
                node_id = int(raw_node_id)
                if node_id not in self.nodes_by_id:
                    raise ValueError(
                        f"constraint equation {constraint_eq_id} term {term_index} references unknown node_id {node_id}"
                    )

                if not isinstance(raw_dof, (int, np.integer)):
                    raise TypeError(
                        f"constraint equation {constraint_eq_id} term {term_index} dof must be an integer"
                    )
                dof = int(raw_dof)
                if dof < 0 or dof > 2:
                    raise ValueError(
                        f"constraint equation {constraint_eq_id} term {term_index} has invalid dof {dof}; expected 0, 1, or 2"
                    )

                try:
                    coeff = float(raw_coeff)
                except (TypeError, ValueError):
                    raise TypeError(
                        f"constraint equation {constraint_eq_id} term {term_index} coefficient must be numeric"
                    ) from None
                if not np.isfinite(coeff):
                    raise ValueError(
                        f"constraint equation {constraint_eq_id} term {term_index} coefficient must be finite"
                    )
                if abs(coeff) <= merge_tolerance:
                    continue

                dof_index = self.__node_dof_index(node_id, dof)
                coefficient_by_dof[dof_index] = coefficient_by_dof.get(dof_index, 0.0) + coeff

            merged_terms = sorted(
                [
                    (dof_index, coeff_value)
                    for dof_index, coeff_value in coefficient_by_dof.items()
                    if abs(coeff_value) > merge_tolerance
                ],
                key=lambda item: item[0],
            )
            if not merged_terms:
                raise ValueError(
                    f"constraint equation {constraint_eq_id} has no non-zero terms after merging duplicate DOFs"
                )

            dof_indices = np.array([item[0] for item in merged_terms], dtype=np.int64)
            coefficients = np.array([item[1] for item in merged_terms], dtype=float)

            normalized_terms: List[object] = []
            for dof_index, coeff_value in merged_terms:
                normalized_node_id = int(dof_index // 3 + 1)
                normalized_dof = int(dof_index % 3)
                normalized_terms.append([normalized_node_id, normalized_dof, float(coeff_value)])
            normalized_terms.append(float(equation_constant))

            normalized_constraint_dict[constraint_eq_id] = normalized_terms
            parsed_constraint_list.append(
                ConstraintEquationData(
                    constraint_eq_id=constraint_eq_id,
                    dof_indices=dof_indices,
                    coefficients=coefficients,
                    equation_constant=float(equation_constant),
                )
            )

        self.constraint_equation_dict = normalized_constraint_dict
        self.constraint_equation_data_list = parsed_constraint_list
        self.lambda_constraint_equations = {}

    def auto_create_rigid_contacts_between_components(
            self,
            parent_component_id: int,
            child_component_id: int,
            tolerance: float,
    ) -> Optional[ContactData]:
        parent_component = None
        child_component = None
        for c in self.components:
            if c.component_id == parent_component_id:
                parent_component = c
            if c.component_id == child_component_id:
                child_component = c
        if parent_component is None or child_component is None:
            raise ValueError("component ids not found")
        parent_mesh = parent_component.mesh
        child_mesh = child_component.mesh
        parent_points = np.asarray(parent_mesh.points, dtype=float)
        child_points = np.asarray(child_mesh.points, dtype=float)
        parent_ids = np.asarray(parent_mesh.point_data["global_node_id"], dtype=int)
        child_ids = np.asarray(child_mesh.point_data["global_node_id"], dtype=int)
        if parent_points.size == 0 or child_points.size == 0:
            return None
        tree = cKDTree(parent_points)
        distances, indices = tree.query(child_points, distance_upper_bound=tolerance)
        mask = np.isfinite(distances) & (indices < parent_points.shape[0])
        if not np.any(mask):
            return None
        matched_parent_ids = parent_ids[indices[mask]]
        matched_child_ids = child_ids[mask]
        contact_constraint_array = np.ones((matched_parent_ids.shape[0], 3), dtype=int)
        return self.add_contact_constraints(
            parent_node_id_array=matched_parent_ids,
            child_node_id_array=matched_child_ids,
            contact_constraint_array=contact_constraint_array,
        )

    def select_nodes_by_coordinates(
            self,
            x: Optional[Tuple[float, float]] = None,
            y: Optional[Tuple[float, float]] = None,
            z: Optional[Tuple[float, float]] = None,
    ) -> np.ndarray:
        if x is float or x is int:
            x = (x, x)
        if y is float or y is int:
            y = (y, y)
        if z is float or z is int:
            z = (z, z)
        node_ids = np.array(sorted(self.nodes_by_id.keys()), dtype=int)
        coords = np.array(
            [self.nodes_by_id[int(node_id)].coordinates for node_id in node_ids],
            dtype=float,
        )
        mask = np.ones(node_ids.shape[0], dtype=bool)
        if x is not None:
            xmin, xmax = x
            mask &= (coords[:, 0] >= xmin) & (coords[:, 0] <= xmax)
        if y is not None:
            ymin, ymax = y
            mask &= (coords[:, 1] >= ymin) & (coords[:, 1] <= ymax)
        if z is not None:
            zmin, zmax = z
            mask &= (coords[:, 2] >= zmin) & (coords[:, 2] <= zmax)
        return node_ids[mask]

    def set_nodal_displacement(
            self,
            node_ids: np.ndarray,
            ux: Optional[float] = None,
            uy: Optional[float] = None,
            uz: Optional[float] = None,
    ) -> None:
        node_ids = np.asarray(node_ids, dtype=int)
        for node_id in node_ids:
            node = self.nodes_by_id[int(node_id)]
            if ux is not None:
                node.prescribed_displacement[0] = float(ux)
            if uy is not None:
                node.prescribed_displacement[1] = float(uy)
            if uz is not None:
                node.prescribed_displacement[2] = float(uz)

    def add_nodal_force(
            self,
            node_ids: np.ndarray,
            fx: Optional[float] = None,
            fy: Optional[float] = None,
            fz: Optional[float] = None,
    ) -> None:
        node_ids = np.asarray(node_ids, dtype=int)
        for node_id in node_ids:
            node = self.nodes_by_id[int(node_id)]
            if fx is not None:
                node.external_force[0] += float(fx)
            if fy is not None:
                node.external_force[1] += float(fy)
            if fz is not None:
                node.external_force[2] += float(fz)

    def get_node_coordinates(self, node_id: int) -> np.ndarray:
        return self.nodes_by_id[node_id].coordinates

    def get_element_node_ids(self, element_id: int) -> np.ndarray:
        return self.elements_by_id[element_id].node_ids

    def get_element_finite_element(self, element_id: int) -> FiniteElement:
        return self.elements_by_id[element_id].finite_element

    def total_number_of_dofs(self) -> int:
        return 3 * self.number_of_nodes

    def build_global_stiffness_matrix(self) -> sparse.csr_matrix:
        number_of_dofs = self.total_number_of_dofs()

        rows_chunks = []
        cols_chunks = []
        data_chunks = []
        dof_offsets = np.arange(3, dtype=np.int64)

        for element_data in self.elements_by_id.values():
            k_e = np.asarray(element_data.finite_element.stiffness_matrix(), dtype=float)

            node_ids = np.asarray(element_data.node_ids, dtype=np.int64)
            base = 3 * (node_ids - 1)
            element_dofs = (base[:, None] + dof_offsets[None, :]).ravel()

            nloc = int(element_dofs.size)
            # Expand indices for COO (vectorized)
            rows_chunks.append(np.repeat(element_dofs, nloc))
            cols_chunks.append(np.tile(element_dofs, nloc))
            data_chunks.append(k_e.reshape(-1))

        if not rows_chunks:
            return sparse.csr_matrix((number_of_dofs, number_of_dofs), dtype=float)

        rows = np.concatenate(rows_chunks).astype(np.int64, copy=False)
        cols = np.concatenate(cols_chunks).astype(np.int64, copy=False)
        data = np.concatenate(data_chunks).astype(float, copy=False)

        k_coo = sparse.coo_matrix((data, (rows, cols)), shape=(number_of_dofs, number_of_dofs))
        k_csr = k_coo.tocsr()
        k_csr.sum_duplicates()
        return k_csr

    def build_global_force_vector(self) -> np.ndarray:
        number_of_dofs = self.total_number_of_dofs()
        force_vector = np.zeros(number_of_dofs)
        for node_id, node in self.nodes_by_id.items():
            base_index = 3 * (int(node_id) - 1)
            force_vector[base_index: base_index + 3] = node.external_force
        return force_vector

    def __node_dof_index(self, node_id: int, component_index: int) -> int:
        return 3 * (node_id - 1) + component_index

    def build_dof_mapping_with_contacts(self) -> np.ndarray:
        number_of_dofs = self.total_number_of_dofs()
        parent_array = np.arange(number_of_dofs, dtype=int)

        def find_root(index: int) -> int:
            while parent_array[index] != index:
                parent_array[index] = parent_array[parent_array[index]]
                index = parent_array[index]
            return index

        def union_indices(index_a: int, index_b: int) -> None:
            root_a = find_root(index_a)
            root_b = find_root(index_b)
            if root_a != root_b:
                parent_array[root_b] = root_a

        for constraint_set in self.contact_constraint_sets:
            for parent_node_id, child_node_id, constraint_row in zip(
                    constraint_set.parent_node_id_array,
                    constraint_set.child_node_id_array,
                    constraint_set.contact_constraint_array, ):
                for component_index in range(3):
                    if int(constraint_row[component_index]) != 0:
                        dof_parent = self.__node_dof_index(int(parent_node_id), component_index)
                        dof_child = self.__node_dof_index(int(child_node_id), component_index)
                        union_indices(dof_parent, dof_child)

        root_indices = np.array([find_root(i) for i in range(number_of_dofs)], dtype=int)
        _, reduced_indices = np.unique(root_indices, return_inverse=True)
        return reduced_indices

    def solve_linear(self):
        self.f, self.u = solve_model(self)
        return self.f, self.u

    def get_elemental_results(self):
        self.__check_results_available()
        element_ids, element_strain, element_stress, element_yielded = model_element_fields(self, self.u)
        return element_ids, element_strain, element_stress, element_yielded

    def get_nodal_displacements(self):
        self.__check_results_available()
        return self.u.reshape(len(self.nodes_by_id), 3)

    def __check_results_available(self):
        if self.u is None or self.f is None:
            sys.stdout.write("No result is available!\n")
            self.solve_linear()

    def solve_nonlinear(self):
        pass
