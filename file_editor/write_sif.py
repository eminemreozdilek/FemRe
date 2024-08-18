import numpy as np

import applications.controller_static.storage as st


def write_input_file(filename: str, data: st.StaticFiniteElementMethod):
    file = open(filename, "w")
    node_df = data.mechanical_nodes
    file.write("#geometry defining\n")
    for index, row in node_df.iterrows():
        node = row["Node"]
        file.write(node.export_name + " " + str(node.node_id) + " " + str(node.coordinates[0]) + " " + str(
            node.coordinates[1]) + " " + str(node.coordinates[2] + "\n"))

    element_df = data.mechanical_elements
    for index, row in element_df.iterrows():
        omega = ""
        element = row["Element"]
        if element.export_name == "strut":
            omega = str(element.omega)
        nodes = ""
        for node in element.connected_nodes:
            nodes = nodes + str(node.node_id) + " "
        file.write(element.export_name + " " + str(element.element_id) + " " + nodes[:-1] + " " +
                   element.material.material_name + " " + element.section.section_name + " " + omega + "\n")

    section_df = data.section_storage
    for index, row in section_df:
        section = row["Section"]
        moment_of_inertia = section.moment_of_inertia.flatten()
        string_for_moment_of_inertia = ""
        for value in moment_of_inertia:
            string_for_moment_of_inertia = string_for_moment_of_inertia + str(value) + " "
        file.write("section " + section.section_name + " " + str(section.area) + " " +
                   string_for_moment_of_inertia[:-1] + "\n")

    file.write("#material defining\n")
    material_df = data.material_storage
    for index, row in material_df:
        material = row["Material"]
        file.write(
            "material" + material.material_name + " " + str(material.unit_weight) + " " + str(
                material.__youngs_modulus) + " " + str(material.poissons_ratio) + " " + str(
                material.thermal_expansion) + " " + str(material.thermal_conductivity) + "\n")

    file.write("#static case")
    for index, row in node_df.itterrow():
        node = row["Node"]
        if node.export_name == "nodestrut":
            if node.rest != np.zeros((6,)):
                vector_string = ""
                for value in node.rest:
                    vector_string += str(value) + " "
                file.write(node.export_name + " rest " + str(node.node_id) + " " + vector_string[:-1] + "\n")
            if node.force[0:3] != np.zeros((3,)):
                vector_string = ""
                for value in node.force[0:3]:
                    vector_string += str(value) + " "
                file.write(node.export_name + " force " + str(node.node_id) + " " + vector_string[:-1] + "\n")
            if node.force[3:6] != np.zeros(3, ):
                vector_string = ""
                for value in node.force[3:6]:
                    vector_string += str(value) + " "
                file.write(node.export_name + " moment " + str(node.node_id) + " " + vector_string[:-1] + "\n")
            if node.displacement != np.zeros((6,)):
                vector_string = ""
                for value in node.displacement:
                    vector_string += str(value) + " "
                file.write(node.export_name + " displacement " + str(node.node_id) + " " + vector_string[:-1] + "\n")
            if node.euler_angles != np.zeros((3,)):
                vector_string = ""
                for value in node.euler_angles:
                    vector_string += str(value) + " "
                file.write(node.export_name + " eulerangles " + str(node.node_id) + " " + vector_string[:-1] + "\n")

        elif node.export_name == "nodesolid":
            if node.rest != np.zeros((3,)):
                vector_string = ""
                for value in node.rest:
                    vector_string += str(value) + " "
                file.write(node.export_name + " rest " + str(node.node_id) + " " + vector_string[:-1] + "\n")
            if node.force != np.zeros((3,)):
                vector_string = ""
                for value in node.force:
                    vector_string += str(value) + " "
                file.write(node.export_name + " force " + str(node.node_id) + " " + vector_string[:-1] + "\n")
            if node.displacement != np.zeros((3,)):
                vector_string = ""
                for value in node.displacement:
                    vector_string += str(value) + " "
                file.write(node.export_name + " displacement " + str(node.node_id) + " " + vector_string[:-1] + "\n")

    for index, row in element_df.itterow():
        element = row["Element"]
        if element.export_name == "strut":
            if element.distributed_force != np.zeros((3,)):
                vector_string = ""
                for value in element.distributed_force:
                    vector_string += str(value) + " "
                file.write(
                    element.export_name + " distributedforce" + str(element.node_id) +
                    " " + vector_string[:-1] + "\n")
            if element.distributed_moment != np.zeros((3,)):
                vector_string = ""
                for value in element.distributed_moment:
                    vector_string += str(value) + " "
                file.write(
                    element.export_name + " distributedmoment " + str(element.node_id) +
                    " " + vector_string[:-1] + "\n")
        if element.export_name == "brick":
            if element.boundary_force_on_x != np.zeros((3,)):
                vector_string = ""
                for value in element.boundary_force_on_x:
                    vector_string += str(value) + " "
                file.write(
                    element.export_name + " boundaryforceonx" + str(element.node_id) +
                    " " + vector_string[:-1] + "\n")
            if element.boundary_force_on_y != np.zeros((3,)):
                vector_string = ""
                for value in element.boundary_force_on_y:
                    vector_string += str(value) + " "
                file.write(
                    element.export_name + " boundaryforceony" + str(element.node_id) +
                    " " + vector_string[:-1] + "\n")
            if element.boundary_force_on_z != np.zeros((3,)):
                vector_string = ""
                for value in element.boundary_force_on_z:
                    vector_string += str(value) + " "
                file.write(
                    element.export_name + " boundaryforceonz" + str(element.node_id) +
                    " " + vector_string[:-1] + "\n")
            if element.volume_force != np.zeros((3,)):
                vector_string = ""
                for value in element.volume_force:
                    vector_string += str(value) + " "
                file.write(
                    element.export_name + " volumeforce" + str(element.node_id) +
                    " " + vector_string[:-1] + "\n")
            if element.tempreture_change != 0.0:
                file.write(
                    element.export_name + " tempreturechange" + str(element.node_id) +
                    " " + str(element.tempreture_change) + "\n")

    file.close()
