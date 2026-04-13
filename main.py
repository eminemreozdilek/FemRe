import numpy as np
import pyvista as pv

import file_io
from model.material import *
from model import Model
from solver.linear_solver import solve_model
import post


def create_i_beam() -> pv.UnstructuredGrid:
    Lx, Ly, Lz = 45, 15, 15
    Nx, Ny, Nz = 45, 15, 15

    # Point coordinates (structured layout, but we'll build an UnstructuredGrid)
    x = np.linspace(0.0, Lx, Nx + 1)
    y = np.linspace(0.0, Ly, Ny + 1)
    z = np.linspace(0.0, Lz, Nz + 1)

    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")  # i,j,k indexing
    points = np.c_[X.ravel(order="F"), Y.ravel(order="F"), Z.ravel(order="F")]

    def pid(i, j, k):
        # Must match ravel(order="F") with indexing="ij"
        return i + (Nx + 1) * j + (Nx + 1) * (Ny + 1) * k

    # Build hexahedron connectivity
    cells = []
    celltypes = []

    VTK_HEXAHEDRON = 12  # VTK cell type id for hex

    for k in range(Nz):
        for j in range(Ny):
            for i in range(Nx):
                p0 = pid(i, j, k)
                p1 = pid(i + 1, j, k)
                p2 = pid(i + 1, j + 1, k)
                p3 = pid(i, j + 1, k)
                p4 = pid(i, j, k + 1)
                p5 = pid(i + 1, j, k + 1)
                p6 = pid(i + 1, j + 1, k + 1)
                p7 = pid(i, j + 1, k + 1)

                cells.extend([8, p0, p1, p2, p3, p4, p5, p6, p7])
                celltypes.append(VTK_HEXAHEDRON)

    cells = np.array(cells, dtype=np.int64)
    celltypes = np.array(celltypes, dtype=np.uint8)

    return pv.UnstructuredGrid(cells, celltypes, points)


def copy_and_translate_mesh(mesh: pv.UnstructuredGrid, translation_vector: np.ndarray) -> pv.UnstructuredGrid:
    translated_mesh = mesh.copy(deep=True)
    translated_mesh.points = translated_mesh.points + np.asarray(translation_vector, dtype=float)
    return translated_mesh


if __name__ == "__main__":
    total_force = 1000

    beam_1 = create_i_beam()
    # beam_2 = copy_and_translate_mesh(beam_1, np.array([45.0, 0.0, 0.0]))

    steel = BaseMaterial(
        material_id=1,
        youngs_modulus=200000,
        poissons_ratio=0.3,)

    model = Model()
    component_1 = model.add_component(beam_1, steel, name="beam_1")
    # component_2 = model.add_component(beam_2, steel, name="beam_2")
    # contact_data = model.auto_create_rigid_contacts_between_components(
    #     parent_component_id=component_1.component_id,
    #     child_component_id=component_2.component_id,
    #     tolerance=1e-3, )

    fixed_nodes = model.select_nodes_by_coordinates(x=(0.0, 0.0))
    model.set_nodal_displacement(fixed_nodes, ux=0.0, uy=0.0, uz=0.0)
    fixed_nodes = model.select_nodes_by_coordinates(x=(45.0, 45.0))
    model.set_nodal_displacement(fixed_nodes, ux=0.0)

    loaded_nodes = model.select_nodes_by_coordinates(y=(15.0,15.0))
    force = - total_force / loaded_nodes.size
    model.add_nodal_force(loaded_nodes, fy=force)

    results = model.solve_linear()
    post_proc = post.PostProcessor(model, deformation_factor=1.0)
    mesh = post_proc.mesh
    mesh.save("macro_result.vtu")
