import numpy as np
from scipy.spatial import cKDTree

import file_io.lif_io as li
import prep.mathematical_lattice_editor as mle
from model.material import *
from model import Model
import post


def _collect_model_nodes(model: Model) -> tuple[np.ndarray, np.ndarray, dict[int, np.ndarray]]:
    node_ids = np.array(sorted(model.nodes_by_id.keys()), dtype=int)
    coords = np.array([model.nodes_by_id[int(node_id)].coordinates for node_id in node_ids], dtype=float)
    coord_by_node_id = {
        int(node_id): coords[index]
        for index, node_id in enumerate(node_ids)
    }
    return node_ids, coords, coord_by_node_id


def _pair_boundary_nodes(
        source_node_ids: np.ndarray,
        target_node_ids: np.ndarray,
        coord_by_node_id: dict[int, np.ndarray],
        match_axes: tuple[int, int],
        tolerance: float,
        label: str,
) -> tuple[np.ndarray, np.ndarray]:
    source_node_ids = np.array(sorted(np.asarray(source_node_ids, dtype=int)), dtype=int)
    target_node_ids = np.array(sorted(np.asarray(target_node_ids, dtype=int)), dtype=int)

    if source_node_ids.size == 0:
        return np.zeros(0, dtype=int), np.zeros(0, dtype=int)
    if target_node_ids.size == 0:
        raise ValueError(f"No target nodes available while pairing {label}")

    source_points = np.array(
        [coord_by_node_id[int(node_id)][list(match_axes)] for node_id in source_node_ids],
        dtype=float,
    )
    target_points = np.array(
        [coord_by_node_id[int(node_id)][list(match_axes)] for node_id in target_node_ids],
        dtype=float,
    )

    tree = cKDTree(target_points)
    distances, indices = tree.query(source_points, distance_upper_bound=tolerance)

    if np.any(~np.isfinite(distances)):
        failed_indices = np.where(~np.isfinite(distances))[0]
        first_failed = int(failed_indices[0])
        raise ValueError(
            f"Failed to find periodic pair for {label} source node {int(source_node_ids[first_failed])}"
        )

    paired_target_ids = target_node_ids[indices]
    unique_targets, target_counts = np.unique(paired_target_ids, return_counts=True)
    if np.any(target_counts > 1):
        duplicate_target = int(unique_targets[np.where(target_counts > 1)[0][0]])
        raise ValueError(
            f"Duplicate periodic target node {duplicate_target} found while pairing {label}."
        )

    return source_node_ids, paired_target_ids.astype(int)


def _append_pair_equations(
        constraint_equations: dict[int, list],
        source_node_ids: np.ndarray,
        target_node_ids: np.ndarray,
        displacement_jump: tuple[float, float, float],
) -> None:
    for source_node_id, target_node_id in zip(source_node_ids, target_node_ids):
        for dof, jump_value in enumerate(displacement_jump):
            equation_id = len(constraint_equations) + 1
            constraint_equations[equation_id] = [
                [int(source_node_id), int(dof), -1.0],
                [int(target_node_id), int(dof), 1.0],
                float(jump_value),
            ]

if __name__ == "__main__":
    lattice_name = "grid"
    volume_fraction = 0.1
    resolution = 50
    lattice_formula = li.calculate_implicit_formula_string_from_lif(f"topology/{lattice_name}.lif")
    thickness, voxel = mle.calculate_thickness(lattice_formula,
                                               volume_fraction,
                                               resolution)
    mesh = mle.generate_voxel_mesh(voxel, (1, 1, 1), 1.0)
    steel = BaseMaterial(
        material_id=1,
        youngs_modulus=200000,
        poissons_ratio=0.3, )

    model = Model()
    component_1 = model.add_component(mesh, steel, name="beam_1")
    fixed_nodes = model.select_nodes_by_coordinates(x=(0.0, 0.0), )
    model.set_nodal_displacement(fixed_nodes, ux=0.0)
    fixed_nodes = model.select_nodes_by_coordinates(x=(0.0, 0.0), y=(0.0, 0.0), z=(0.0, 0.0))
    model.set_nodal_displacement(fixed_nodes, ux=0.0, uy=0.0, uz=0.0)
    fixed_nodes = model.select_nodes_by_coordinates(x=(1.0, 1.0))
    model.set_nodal_displacement(fixed_nodes, ux=1.0)
    results = model.solve_linear()
    post_proc = post.PostProcessor(model, deformation_factor=1.0)
    mesh = post_proc.mesh
    mesh.save("uniaxial_tensile_test.vtu")

    # Second analysis: 3-axis periodic boundary conditions with tensile ux jump.
    model = Model()
    component_1 = model.add_component(mesh, steel, name="beam_1")
    node_ids, coords, coord_by_node_id = _collect_model_nodes(model)

    minimum_coords = np.min(coords, axis=0)
    maximum_coords = np.max(coords, axis=0)
    model_size = float(np.max(maximum_coords - minimum_coords))
    boundary_tolerance = max(model_size * 1.0e-8, 1.0e-10)

    on_x0 = np.isclose(coords[:, 0], minimum_coords[0], atol=boundary_tolerance)
    on_x1 = np.isclose(coords[:, 0], maximum_coords[0], atol=boundary_tolerance)
    on_y0 = np.isclose(coords[:, 1], minimum_coords[1], atol=boundary_tolerance)
    on_y1 = np.isclose(coords[:, 1], maximum_coords[1], atol=boundary_tolerance)
    on_z0 = np.isclose(coords[:, 2], minimum_coords[2], atol=boundary_tolerance)
    on_z1 = np.isclose(coords[:, 2], maximum_coords[2], atol=boundary_tolerance)

    # Anchor one corner to remove rigid translation modes.
    reference_corner_mask = on_x0 & on_y0 & on_z0
    if not np.any(reference_corner_mask):
        raise ValueError("Could not find the reference corner on x=min, y=min, z=min.")
    reference_node_id = int(np.min(node_ids[reference_corner_mask]))
    model.set_nodal_displacement(np.array([reference_node_id], dtype=int), ux=0.0, uy=0.0, uz=0.0)

    on_y_boundary = on_y0 | on_y1
    on_z_boundary = on_z0 | on_z1

    constraint_eqs: dict[int, list] = {}
    total_pairs = 0

    # Corner -> edge -> face order for x-direction constraints.
    x_corner_mask = on_x0 & on_y_boundary & on_z_boundary
    x_edge_mask = on_x0 & (on_y_boundary ^ on_z_boundary)
    x_face_mask = on_x0 & (~on_y_boundary) & (~on_z_boundary)

    for label, source_mask in (
            ("x_corners", x_corner_mask),
            ("x_edges", x_edge_mask),
            ("x_faces", x_face_mask),
    ):
        source_ids, target_ids = _pair_boundary_nodes(
            source_node_ids=node_ids[source_mask],
            target_node_ids=node_ids[on_x1],
            coord_by_node_id=coord_by_node_id,
            match_axes=(1, 2),
            tolerance=boundary_tolerance,
            label=label,
        )
        _append_pair_equations(
            constraint_equations=constraint_eqs,
            source_node_ids=source_ids,
            target_node_ids=target_ids,
            displacement_jump=(1.0, 0.0, 0.0),
        )
        total_pairs += int(source_ids.size)

    # y-direction: exclude x-boundary nodes to avoid redundant corner/edge equations.
    y_base_mask = on_y0 & (~on_x0) & (~on_x1)
    y_edge_mask = y_base_mask & (on_z0 | on_z1)
    y_face_mask = y_base_mask & (~on_z0) & (~on_z1)

    for label, source_mask in (
            ("y_edges", y_edge_mask),
            ("y_faces", y_face_mask),
    ):
        source_ids, target_ids = _pair_boundary_nodes(
            source_node_ids=node_ids[source_mask],
            target_node_ids=node_ids[on_y1],
            coord_by_node_id=coord_by_node_id,
            match_axes=(0, 2),
            tolerance=boundary_tolerance,
            label=label,
        )
        _append_pair_equations(
            constraint_equations=constraint_eqs,
            source_node_ids=source_ids,
            target_node_ids=target_ids,
            displacement_jump=(0.0, 0.0, 0.0),
        )
        total_pairs += int(source_ids.size)

    # z-direction: exclude x and y boundaries so only remaining face-interior nodes are constrained.
    z_face_mask = on_z0 & (~on_x0) & (~on_x1) & (~on_y0) & (~on_y1)
    source_ids, target_ids = _pair_boundary_nodes(
        source_node_ids=node_ids[z_face_mask],
        target_node_ids=node_ids[on_z1],
        coord_by_node_id=coord_by_node_id,
        match_axes=(0, 1),
        tolerance=boundary_tolerance,
        label="z_faces",
    )
    _append_pair_equations(
        constraint_equations=constraint_eqs,
        source_node_ids=source_ids,
        target_node_ids=target_ids,
        displacement_jump=(0.0, 0.0, 0.0),
    )
    total_pairs += int(source_ids.size)

    print(f"Generated {len(constraint_eqs)} MPC equations from {total_pairs} periodic node pairs.")

    model.set_constraint_equation(constraint_eqs)
    results = model.solve_linear()
    post_proc = post.PostProcessor(model, deformation_factor=1.0)
    mesh = post_proc.mesh
    mesh.save("pbc_tensile_test.vtu")
    