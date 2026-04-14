import file_io
import prep.mathematical_lattice_editor as mle
from model.material import BaseMaterial
from model import Model
import post

if __name__ == "__main__":
    total_force = 1000

    for vf in [0.1, 0.3, 0.5]:
        lattice_type = "Grid"
        lattice_path = f"example_inputs/{lattice_type}.lif"
        formula_str = file_io.lif_io.calculate_implicit_formula_string_from_lif(lattice_path)
        # formula_str = "cos(x) * sin(y) + cos(y) * sin(z) + cos(z) * sin(x)"
        thickness, voxel_array = mle.calculate_thickness(formula_str, vf, 50, network_phase=False)
        grid = mle.generate_voxel_mesh(voxel_array, repeats=(9, 3, 3), scale=5.0)
        grid.save(f"macro_{lattice_type}_{round(vf * 100)}_vf.vtu")
        # grid.plot(show_bounds=True, show_edges=True)

        E = 200000
        nu = 0.3
        eps_xx = 1.0
        steel = BaseMaterial(1, E, nu)

        model = Model()
        component_1 = model.add_component(grid, steel, name="beam_1")

        fixed_nodes = model.select_nodes_by_coordinates(x=(0.0, 0.0))
        model.set_nodal_displacement(fixed_nodes, ux=0.0, uy=0.0, uz=0.0)
        fixed_nodes = model.select_nodes_by_coordinates(x=(45.0, 45.0))
        model.set_nodal_displacement(fixed_nodes, ux=0.0)

        loaded_nodes = model.select_nodes_by_coordinates(y=(15.0, 15.0))
        force = - total_force / loaded_nodes.size
        model.add_nodal_force(loaded_nodes, fy=force)

        results = model.solve_linear()
        post_proc = post.PostProcessor(model, deformation_factor=1.0)
        mesh = post_proc.mesh
        mesh.save(f"macro_result_{vf}.vtu")
