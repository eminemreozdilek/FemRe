import numpy as np
import preprocessor.properties.material as mtrl
import preprocessor.models.nodes as nd
import preprocessor.models.elements as elmnt


def create_rectengle(data, size: tuple = (1, 1, 1), number_of_elements_per_edge: tuple = (1, 1, 1)):
    E = 28.0e6  # [kN/m^2]
    p = 0.22  # Poisson oranı
    unit_weight = 24.0  # [kN/m^3]
    thermal_expansion_coefficient = 1.0e-5  # [1/Celsius]

    weight_factor = 1.0
    temperature_change = 20.0  # [Celsius]
    top_surface_load_z = -150.0  # [kN/m^2]

    Lx, Ly, Lz = size
    Nx, Ny, Nz = number_of_elements_per_edge
    dx, dy, dz = Lx / Nx, Ly / Ny, Lz / Nz

    id = 1
    for zi in range(Nz + 1):
        for yi in range(Ny + 1):
            for xi in range(Nx + 1):
                new_node = nd.NodeSolid(node_id=id, coordinates=(xi * dx, yi * dy, zi * dz))
                data.update_node(new_node)
                id += 1

    id = 1
    for zi in range(Nz):
        for yi in range(Ny):
            for xi in range(Nx):
                n1 = (xi + 1) + yi * (Nx + 1) + zi * (Nx + 1) * (Ny + 1)
                n2 = n1 + 1
                n3 = n2 + (Nx + 1)
                n4 = n3 - 1
                n5 = n1 + (Nx + 1) * (Ny + 1)
                n6 = n5 + 1
                n7 = n6 + (Nx + 1)
                n8 = n7 - 1
                conn = [data.node_storage.loc[data.node_storage['NodeID'] == id, 'Node'].values[0] for id in
                        [n1, n2, n3, n4, n5, n6, n7, n8]]
                new_element = elmnt.ElementBrickEight(element_id=id, connected_nodes=conn,
                                                      material_of_element=new_material)
                data.update_element(new_element)
                id += 1
