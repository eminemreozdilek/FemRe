import numpy as np
import pyvista as pv

from model.material import *
from model import Model
from solver.linear_solver import solve_model
from prep import mathematical_lattice_editor as mle
import post

from file_io.gmsh import read_msh

if __name__ == "__main__":
    total_force = 6000.0
    mesh = read_msh("./untitled.msh")[2]
    mesh.plot(show_edges=True, show_bounds=True)

    steel = BaseMaterial(
        material_id=1,
        youngs_modulus=210e3,
        poissons_ratio=0.3,
        yield_strength=225,
        tangent_modulus=2.0e3, )

    model = Model()
    component_1 = model.add_component(mesh, steel, name="beam_1")

    fixed_nodes = model.select_nodes_by_coordinates(x=(0.0, 0.0), z=(0.0, 0.0))
    model.set_nodal_displacement(fixed_nodes, uz=0.0)
    fixed_nodes = model.select_nodes_by_coordinates(x=(5.0, 5.0), z=(0.0, 0.0))
    model.set_nodal_displacement(fixed_nodes, uz=0.0)
    fixed_nodes = model.select_nodes_by_coordinates(x=(0.0, 0.0), y=(0.0, 0.0), z=(0.0, 0.0))
    model.set_nodal_displacement(fixed_nodes, ux=0.0, uy=0.0, uz=0.0)

    loaded_nodes = model.select_nodes_by_coordinates(z=(1.0, 1.0))
    force = - total_force / loaded_nodes.size
    model.add_nodal_force(loaded_nodes, fz=force)

    results = model.solve_linear()
    post.attach_nodal_displacements(model)  # "U", "U_mag"

    # Reactions at supports
    post.attach_nodal_reactions(model)  # "R", "R_mag"

    # Element stresses/strains (cell results)
    post.attach_element_stress_strain(model)  # "S", "E", "yielded"
    post.attach_element_voigt_components(model, "S")  # "S_xx", "S_yy", ..., "S_xz"

    # Von Mises as a single scalar per element
    post.attach_element_von_mises(model)  # "S_vm"

    # Plot von Mises on the deformed shape
    post.plot_on_components(
        model,
        scalars="S_vm",
        association="cell",
        warp_by="U",
        warp_factor=0.0,
        show_edges=False,
    )

    post.plot_on_components(model,
                            scalars="S_xx",
                            association="cell",
                            warp_by="U",
                            warp_factor=0.0)
