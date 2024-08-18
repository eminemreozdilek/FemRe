import pandas as pd
import numpy as np

import preprocessor.models.nodes as nd
import preprocessor.models.elements as elmnt

import preprocessor.mathematical_models.nodes as mnd
import preprocessor.mathematical_models.elements as mel

import material as mtrl

STANDARTMATERIAL = mtrl.Material(1,
                                 200000,
                                 0.3,
                                 0.0,
                                 0.0,
                                 7860,
                                 "Steel")


class Storage:
    def __init__(self):
        self.__node_storage = nd.Nodes()

        self.__element_brick_eight_storage = elmnt.ElementBrickEight()
        self.__element_tetra_four_storage = elmnt.ElementTetraFour()

        self.reset_mathematical_model()

    def update_node(self, node: pd.DataFrame):
        for column_name in self.__node_storage.data.columns:
            if column_name not in node.columns:
                if "Code" in column_name:
                    node[column_name] = -1 * np.ones(len(node))
                else:
                    node[column_name] = np.zeros(len(node))

        self.__node_storage.set_data(node)

    def update_hexagonal_element(self, element: pd.DataFrame):
        for column_name in self.__element_brick_eight_storage.data.columns:
            if column_name not in element.columns:
                element[column_name] = np.zeros(len(element))

        self.__element_brick_eight_storage.set_data(element)

    def update_tetrahedral_element(self, element: pd.DataFrame):
        for column_name in self.__element_tetra_four_storage.data.columns:
            if column_name not in element.columns:
                element[column_name] = np.zeros(len(element))

        self.__element_tetra_four_storage.set_data(element)

    def generate_mathematical_model(self):
        self.reset_mathematical_model()

        for index, row in self.__node_storage.data.iterrows():
            new_node = mnd.Node(row["NodeID"], row["X"], row["Y"], row["Z"])
            # new_node.set_rest((row["RestX"], row["RestY"], row["RestZ"]))
            # new_node.set_force((row["ForceX"], row["ForceY"], row["ForceZ"]))
            # new_node.set_displacement((row["DisplacementX"], row["DisplacementY"], row["DisplacementZ"]))
            new_node.rest = (row["RestX"], row["RestY"], row["RestZ"])
            new_node.force = [row["ForceX"], row["ForceY"], row["ForceZ"]]
            new_node.disp = [row["DisplacementX"], row["DisplacementY"], row["DisplacementZ"]]

            self.__mechanical_nodes = new_node.save_node_to_dataframe(self.__mechanical_nodes)

        for index, row in self.__element_brick_eight_storage.data.iterrows():
            nodes_of_new_element = row[
                ["Node1", "Node2", "Node3", "Node4", "Node5", "Node6", "Node7", "Node8"]].values
            mask = self.__mechanical_nodes['NodeID'].isin(nodes_of_new_element)
            nodes_of_new_element = self.__mechanical_nodes.loc[mask, 'Node'].values

            new_element = mel.BrickElement(row["ElementID"], nodes_of_new_element, STANDARTMATERIAL)
            # new_element.set_volume_force(np.array([row["VolumeForceX"], row["VolumeForceY"], row["VolumeForceZ"]]))
            new_element.volumeForce = [row["VolumeForceX"], row["VolumeForceY"], row["VolumeForceZ"]]
            # new_element.set_boundary_force_on_x(np.array(
            #     [row["BoundaryForceX1"], row["BoundaryForceX2"], row["BoundaryForceX3"],
            #      row["BoundaryForceX4"], row["BoundaryForceX5"], row["BoundaryForceX6"]]))
            new_element.boundaryForceX = [row["BoundaryForceX1"], row["BoundaryForceX2"], row["BoundaryForceX3"],
                                          row["BoundaryForceX4"], row["BoundaryForceX5"], row["BoundaryForceX6"]]
            new_element.boundaryForceX = [row["BoundaryForceY1"], row["BoundaryForceY2"], row["BoundaryForceY3"],
                                          row["BoundaryForceY4"], row["BoundaryForceY5"], row["BoundaryForceY6"]]
            new_element.boundaryForceX = [row["BoundaryForceZ1"], row["BoundaryForceZ2"], row["BoundaryForceZ3"],
                                          row["BoundaryForceZ4"], row["BoundaryForceZ5"], row["BoundaryForceZ6"]]

            new_element.tem = row["TemperatureChange"]

            self.__mechanical_elements = new_element.save_element_to_dataframe(self.__mechanical_elements)

        for index, row in self.__element_tetra_four_storage.data.iterrows():
            nodes_of_new_element = row[
                ["Node1", "Node2", "Node3", "Node4"]].values
            mask = self.__mechanical_nodes['NodeID'].isin(nodes_of_new_element)
            nodes_of_new_element = self.__mechanical_nodes.loc[mask, 'Node'].values

            new_element = mel.TetraElement(row["ElementID"], nodes_of_new_element, STANDARTMATERIAL)
            new_element.volumeForce = [row["VolumeForceX"], row["VolumeForceY"], row["VolumeForceZ"]]
            new_element.boundaryForceX = [row["BoundaryForceX1"], row["BoundaryForceX2"], row["BoundaryForceX3"],
                                          row["BoundaryForceX4"]]
            new_element.boundaryForceY = [row["BoundaryForceY1"], row["BoundaryForceY2"], row["BoundaryForceY3"],
                                          row["BoundaryForceY4"]]
            new_element.boundaryForceZ = [row["BoundaryForceZ1"], row["BoundaryForceZ2"], row["BoundaryForceZ3"],
                                          row["BoundaryForceZ4"]]
            new_element.temperatureChange = row["TemperatureChange"]

            self.__mechanical_elements = new_element.save_element_to_dataframe(self.__mechanical_elements)

    def reset_mathematical_model(self):
        self.__mechanical_nodes = pd.DataFrame({"NodeID": [],
                                                "Node": [], })

        self.__mechanical_elements = pd.DataFrame({"ElementID": [],
                                                   "Element": [], })

        self.__material_storage = pd.DataFrame({"MaterialName": [1],
                                                "Material": [mtrl.Material(1,
                                                                           200000,
                                                                           0.3,
                                                                           0.0,
                                                                           0.0,
                                                                           7860,
                                                                           "Steel")]})

    def save_mechanical_results(self, us: np.array, ps: np.array):
        data = self.__node_storage.data
        displacements = []
        forces = []
        for nodes in self.__mechanical_nodes['Node']:
            codes = nodes.code
            # nodes.set_result_displacements(tuple(us[codes].tolist()))
            # nodes.set_result_forces(tuple(ps[codes].tolist()))
            displacements.append(us[codes])
            forces.append(ps[codes])

        displacements = np.array(displacements).transpose()
        forces = np.array(forces).transpose()

        data['ResultDisplacementX'] = displacements[0]
        data['ResultDisplacementY'] = displacements[1]
        data['ResultDisplacementZ'] = displacements[2]
        data['ResultForceX'] = forces[0]
        data['ResultForceY'] = forces[1]
        data['ResultForceZ'] = forces[2]

        tetra_data = self.__element_tetra_four_storage.data
        hexa_data = self.__element_brick_eight_storage.data
        for elements in self.__mechanical_elements['Element']:
            elements.set_solution(us)
            stress_array = elements.stress_array()
            strain_array = elements.strain_array()
            von_misses_strain = elements.von_misses_strain()
            von_misses_stress = elements.von_misses_stress()
            von_misses_energy = elements.von_misses_energy()

            if "Element TetraFour" in str(elements):
                tetra_data['StressX'] = stress_array[0]
                tetra_data['StressY'] = stress_array[1]
                tetra_data['StressZ'] = stress_array[2]
                tetra_data['ShearXY'] = stress_array[3]
                tetra_data['ShearYZ'] = stress_array[4]
                tetra_data['ShearXZ'] = stress_array[5]
                tetra_data['StrainX'] = strain_array[0]
                tetra_data['StrainY'] = strain_array[1]
                tetra_data['StrainZ'] = strain_array[2]
                tetra_data['StrainXY'] = strain_array[3]
                tetra_data['StrainYZ'] = strain_array[4]
                tetra_data['StrainXZ'] = strain_array[5]
                tetra_data['VonMissesStress'] = von_misses_stress
                tetra_data['VonMissesStrain'] = von_misses_strain
                tetra_data['VonMissesEnergy'] = von_misses_energy

            elif "Element BrickEight" in str(elements):
                hexa_data['StressX'] = stress_array[0]
                hexa_data['StressY'] = stress_array[1]
                hexa_data['StressZ'] = stress_array[2]
                hexa_data['ShearXY'] = stress_array[3]
                hexa_data['ShearYZ'] = stress_array[4]
                hexa_data['ShearXZ'] = stress_array[5]
                hexa_data['StrainX'] = strain_array[0]
                hexa_data['StrainY'] = strain_array[1]
                hexa_data['StrainZ'] = strain_array[2]
                hexa_data['StrainXY'] = strain_array[3]
                hexa_data['StrainYZ'] = strain_array[4]
                hexa_data['StrainXZ'] = strain_array[5]
                hexa_data['VonMissesStress'] = von_misses_stress
                hexa_data['VonMissesStrain'] = von_misses_strain
                hexa_data['VonMissesEnergy'] = von_misses_energy

        self.__node_storage.set_data(data)
        self.__element_tetra_four_storage.set_data(tetra_data)
        self.__element_brick_eight_storage.set_data(hexa_data)

    def set_new_nodal_data(self, nodal_data):
        self.__node_storage.set_data(nodal_data)

    @property
    def mechanical_nodes(self):
        return self.__mechanical_nodes

    @property
    def mechanical_elements(self):
        return self.__mechanical_elements

    @property
    def material_storage(self):
        return self.__material_storage

    @property
    def node_storage(self):
        return self.__node_storage

    @property
    def element_brick_eight_storage(self):
        return self.__element_brick_eight_storage

    @property
    def element_tetra_four_storage(self):
        return self.__element_tetra_four_storage

    @property
    def material_storage(self):
        return self.__material_storage

    @property
    def nodes_and_elements_dictionary_for_solver(self):
        nodes = dict(zip(self.__mechanical_nodes['NodeID'], self.__mechanical_nodes['Node']))
        elements = dict(zip(self.__mechanical_elements['ElementID'], self.__mechanical_elements['Element']))
        return nodes, elements

# def update_material(self, material: mtrl.Material):
#     self.__material_storage = material.save_material_to_dataframe(self.__material_storage)
#
# def add_node_results(self, us, ps):
#     displacements = []
#     forces = []
#
#     for nodes in self.__node_storage['Node']:
#         codes = nodes.code
#         nodes.set_result_displacements(tuple(us[codes].tolist()))
#         nodes.set_result_forces(tuple(ps[codes].tolist()))
#         displacements.append(us[codes])
#         forces.append(ps[codes])
#
#     self.__node_storage['Displacement'] = displacements
#     self.__node_storage['Force'] = forces
#
# def remove_element(self, element_id: int):
#     self.__element_storage[self.__element_storage['ElementID'] != element_id].reset_index(drop=True)
#
# def remove_node(self, node_id: int):
#     self.__node_storage[self.__node_storage['NodeID'] != node_id].reset_index(drop=True)
#
# def remove_section(self, section_name: str):
#     self.__section_storage[self.__section_storage['SectionName'] != section_name].reset_index(drop=True)
#
# def remove_material(self, material_name: str):
#     self.__material_storage[self.__material_storage['MaterialName'] != material_name].reset_index(drop=True)
