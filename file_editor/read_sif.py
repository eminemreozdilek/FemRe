# import numpy as np
#
# import applications.controller_static.model_storage as st
# import preprocessor.models.nodes as nd
# import preprocessor.models.elements as el
# import preprocessor.properties.material as mt
# import preprocessor.properties.section as sc
#
#
# def read_input_file(input_file: str):
#     node_information = []
#     element_information = []
#     material_information = []
#     section_information = []
#     data = st.Storage()
#
#     file = open(input_file, 'r')
#     lines = file.readlines()
#     file.close()
#     for line in lines:
#         if not line.startswith('#'):
#             if line != "\n":
#                 line = line.replace("\n", "")
#                 data_in_line = line.split(' ')
#                 if data_in_line[0].lower() in ['nodestrut', 'nodesolid']:
#                     node_information.append(data_in_line)
#                 elif data_in_line[0].lower() in ['brick', 'strut']:
#                     element_information.append(data_in_line)
#                 elif data_in_line[0].lower() == 'material':
#                     material_information.append(data_in_line)
#                 elif data_in_line[0].lower() == 'section':
#                     section_information.append(data_in_line)
#
#     for row in node_information:
#         if row[0] == "nodesolid":
#             if row[1].isdigit():
#                 new_node = nd.NodeSolid(node_id=int(row[1]),
#                                         coordinates=(float(row[2]),
#                                                      float(row[3]),
#                                                      float(row[4])))
#                 data.update_node(new_node)
#             else:
#                 node = data.node_storage.loc[data.node_storage['NodeID'] == int(row[2]), 'Node'].values[0]
#                 if row[1] == "rest":
#                     node.set_rest((int(row[3]), int(row[4]), int(row[5])))
#                 elif row[1] == "force":
#                     node.set_force((float(row[3]), float(row[4]), float(row[5])))
#                 elif row[1] == "displacement":
#                     node.set_displacement((float(row[3]), float(row[4]), float(row[5])))
#
#         elif row[0] == "nodestrut":
#             if row[1].isdigit():
#                 new_node = nd.NodeStrut(node_id=int(row[1]),
#                                         coordinates=(float(row[2]),
#                                                      float(row[3]),
#                                                      float(row[4])))
#                 data.update_node(new_node)
#             else:
#                 node = data.node_storage.loc[data.node_storage['NodeID'] == int(row[2]), 'Node'].values[0]
#                 if row[1] == "rest":
#                     node.set_rest((int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), int(row[8])))
#                 elif row[1] == "force":
#                     node.set_force((float(row[3]), float(row[4]), float(row[5])))
#                 elif row[1] == "moment":
#                     node.set_moment((float(row[3]), float(row[4]), float(row[5])))
#                 elif row[1] == "displacement":
#                     node.set_displacement(
#                         (float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8])))
#                 elif row[1] == "eulerangles":
#                     node.set_euler_angles((float(row[3]), float(row[4]), float(row[5])))
#         else:
#             pass
#
#     for row in material_information:
#         new_material = mt.Material(material_name=row[1],
#                                    unit_weight=float(row[2]),
#                                    youngs_modulus=float(row[3]),
#                                    poisson_ratio=float(row[4]),
#                                    thermal_expansion_coefficient=float(row[5]),
#                                    thermal_conductivity=float(row[6]))
#         data.update_material(new_material)
#
#     for row in section_information:
#         moment_of_inertia = np.array([[float(row[3]), float(row[4]), float(row[5])],
#                                       [float(row[6]), float(row[7]), float(row[8])],
#                                       [float(row[9]), float(row[10]), float(row[11])]])
#         new_section = sc.Section(section_name=row[1], area=float(row[2]), moment_of_inertia=moment_of_inertia)
#         data.update_section(new_section)
#
#     for row in element_information:
#
#         if row[0] == "brick":
#
#             if row[1].isdigit():
#                 material = \
#                 data.material_storage.loc[data.material_storage['MaterialName'] == row[10], 'Material'].values[0]
#                 node_positions = range(2, 10)
#                 nodes = [data.node_storage.loc[data.node_storage['NodeID'] == int(row[index]), 'Node'].values[0] for
#                          index
#                          in node_positions]
#                 new_element = el.ElementBrickEight(element_id=int(row[0]),
#                                                    connected_nodes=nodes,
#                                                    material_of_element=material)
#                 data.update_element(new_element)
#
#             elif row[1] == "boundaryforceonx":
#                 element = data.element_storage.loc[data.element_storage['ElementID'] == int(row[2]), 'Material'].values[
#                     0]
#                 element.set_boundary_force_on_x(np.array(
#                     [float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8])]))
#             elif row[1] == "boundaryforceony":
#                 element = data.element_storage.loc[data.element_storage['ElementID'] == int(row[2]), 'Material'].values[
#                     0]
#                 element.set_boundary_force_on_y(np.array(
#                     [float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8])]))
#             elif row[1] == "boundaryforceonz":
#                 element = data.element_storage.loc[data.element_storage['ElementID'] == int(row[2]), 'Material'].values[
#                     0]
#                 element.set_boundary_force_on_z(np.array(
#                     [float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8])]))
#             elif row[1] == "volumeforce":
#                 element = data.element_storage.loc[data.element_storage['ElementID'] == int(row[2]), 'Material'].values[
#                     0]
#                 element.set_volume_force(np.array([float(row[3]), float(row[4]), float(row[5])]))
#             elif row[1] == "tempreturechange":
#                 element = data.element_storage.loc[data.element_storage['ElementID'] == int(row[2]), 'Material'].values[
#                     0]
#                 element.set_tempreture_change(float(row[3]))
#
#         elif row[0] == "strut":
#
#             if row[1].isdigit():
#                 material = \
#                 data.material_storage.loc[data.material_storage['MaterialName'] == row[4], 'Material'].values[0]
#                 node_positions = range(2, 4)
#                 nodes = [data.node_storage.loc[data.node_storage['NodeID'] == int(row[index]), 'Node'].values[0]
#                          for index in node_positions]
#                 cross_section = \
#                 data.section_storage.loc[data.section_storage['SectionName'] == row[5], 'Section'].values[0]
#                 new_element = el.ElementStrutTwo(element_id=int(row[1]),
#                                                  connected_nodes=nodes,
#                                                  material_of_element=material,
#                                                  cross_section=cross_section,
#                                                  omega_angle=float(row[6]))
#                 data.update_element(new_element)
#             elif row[1] == "force":
#                 element = data.element_storage.loc[data.element_storage['ElementID'] == int(row[2]), 'Element'].values[
#                     0]
#                 element.set_distributed_force(np.array(np.array([float(row[3]), float(row[4]), float(row[5])])))
#             elif row[2] == "moment":
#                 element = data.element_storage.loc[data.element_storage['ElementID'] == int(row[2]), 'Element'].values[
#                     0]
#                 element.set_distributed_moment(np.array(np.array([float(row[3]), float(row[4]), float(row[5])])))
#         else:
#             pass
#
#     return data