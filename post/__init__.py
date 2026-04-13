import numpy as np
import pyvista as pv
from pyvista import CellType

class PostProcessor:
    def __init__(self, model, deformation_factor=1.0):
        self.model = model
        self.deformation_factor = deformation_factor
        
        if self.model.u is None or self.model.f is None:
            raise RuntimeError("Model must be solved before post-processing. Call solve_linear() first.")
            
        self.mesh = self._build_global_mesh()
        self._compute_and_assign_results()

    def _build_global_mesh(self) -> pv.UnstructuredGrid:
        """Constructs a single global PyVista mesh from the model's nodes and elements."""
        # 1. Create mapping from Node ID to a 0-based contiguous index
        sorted_nids = sorted(self.model.nodes_by_id.keys())
        self.nid_to_idx = {nid: i for i, nid in enumerate(sorted_nids)}
        
        # 2. Extract coordinates
        points = np.array([self.model.nodes_by_id[nid].coordinates for nid in sorted_nids], dtype=float)
        
        # 3. Build cell connectivity
        cells = []
        cell_types = []
        
        for eid in sorted(self.model.elements_by_id.keys()):
            elem_data = self.model.elements_by_id[eid]
            nids = elem_data.node_ids
            indices = [self.nid_to_idx[nid] for nid in nids]
            
            # Format: [number_of_points, p0, p1, ..., pn]
            cells.extend([len(indices)] + indices)
            
            # Map number of nodes to PyVista/VTK cell types
            if len(indices) == 8:
                cell_types.append(CellType.HEXAHEDRON)
            elif len(indices) == 4:
                cell_types.append(CellType.TETRA)
            elif len(indices) == 20:
                cell_types.append(CellType.QUADRATIC_HEXAHEDRON)
            elif len(indices) == 10:
                cell_types.append(CellType.QUADRATIC_TETRA)
            else:
                raise ValueError(f"Unsupported element node count: {len(indices)}")
                
        return pv.UnstructuredGrid(cells, np.array(cell_types, dtype=np.uint8), points)

    def _compute_and_assign_results(self):
        """Calculates and assigns point data and cell data to the PyVista mesh."""
        num_points = self.mesh.n_points
        u_mapped = np.zeros((num_points, 3))
        f_mapped = np.zeros((num_points, 3))
        
        # --- NODAL DATA (Point Data) ---
        for nid, idx in self.nid_to_idx.items():
            base = 3 * (nid - 1)
            u_mapped[idx] = self.model.u[base:base+3]
            f_mapped[idx] = self.model.f[base:base+3]
            
        self.mesh.point_data["Displacement"] = u_mapped
        self.mesh.point_data["Displacement_Magnitude"] = np.linalg.norm(u_mapped, axis=1)
        self.mesh.point_data["Reaction_Force"] = f_mapped
        self.mesh.point_data["Reaction_Force_Magnitude"] = np.linalg.norm(f_mapped, axis=1)

        # --- ELEMENTAL DATA (Cell Data) ---
        strains = []
        stresses = []
        vm_strains = []
        vm_stresses = []
        energies = []
        principal_stresses = []

        for eid in sorted(self.model.elements_by_id.keys()):
            elem_data = self.model.elements_by_id[eid]
            fe = elem_data.finite_element
            
            # Extract element displacement vector
            u_e = np.zeros(3 * len(elem_data.node_ids))
            for i, nid in enumerate(elem_data.node_ids):
                base = 3 * (nid - 1)
                u_e[3*i : 3*i+3] = self.model.u[base:base+3]
                
            # Compute base properties at element center (xi=0, eta=0, zeta=0)
            strain = fe.compute_strain(u_e)
            stress = fe.compute_stress(u_e)
            
            strains.append(strain)
            stresses.append(stress)
            vm_strains.append(fe.von_mises_strain(strain))
            vm_stresses.append(fe.von_mises_stress(stress))
            energies.append(fe.compute_strain_energy(u_e))
            
            # Compute Principal Stresses (Eigenvalues of the 3x3 stress tensor)
            # Voigt order in your element: [s_x, s_y, s_z, t_xy, t_yz, t_zx]
            S = np.array([
                [stress[0], stress[3], stress[5]],
                [stress[3], stress[1], stress[4]],
                [stress[5], stress[4], stress[2]]
            ])
            eigvals = np.linalg.eigvalsh(S)
            principal_stresses.append(eigvals[::-1]) # Sort descending (p1, p2, p3)

        self.mesh.cell_data["Strain_Voigt"] = np.array(strains)
        self.mesh.cell_data["Stress_Voigt"] = np.array(stresses)
        self.mesh.cell_data["Von_Mises_Strain"] = np.array(vm_strains)
        self.mesh.cell_data["Von_Mises_Stress"] = np.array(vm_stresses)
        self.mesh.cell_data["Strain_Energy"] = np.array(energies)
        self.mesh.cell_data["Principal_Stresses"] = np.array(principal_stresses)

    def get_deformed_mesh(self) -> pv.UnstructuredGrid:
        """Returns the mesh warped by the displacement vector."""
        return self.mesh.warp_by_vector("Displacement", factor=self.deformation_factor)

    def plot(self, scalar_field: str, show_edges=True, **kwargs):
        """
        Generic plotting method for any computed field.
        """
        valid_scalars = list(self.mesh.point_data.keys()) + list(self.mesh.cell_data.keys())
        if scalar_field not in valid_scalars:
            raise ValueError(f"Field '{scalar_field}' not found. Available fields: {valid_scalars}")

        plotter = pv.Plotter()
        plotter.add_text(f"Field: {scalar_field} (Deformation Scale: {self.deformation_factor}x)", font_size=12)
        
        deformed = self.get_deformed_mesh()
        plotter.add_mesh(
            deformed, 
            scalars=scalar_field, 
            show_edges=show_edges, 
            cmap="jet",
            **kwargs
        )
        plotter.add_axes()
        plotter.show()
        
    def plot_principal_stresses(self):
        """Specifically plot the maximum principal stress (P1)."""
        deformed = self.get_deformed_mesh()
        # Extract P1 (first column of the principal stresses array)
        deformed.cell_data["Max_Principal_Stress"] = deformed.cell_data["Principal_Stresses"][:, 0]
        self.plot("Max_Principal_Stress")