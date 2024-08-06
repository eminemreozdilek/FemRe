import pandas as pd
import preprocessor.models.nodes as nd
import preprocessor.models.elements as elmnt
import preprocessor.properties.section as sct
import preprocessor.properties.material as mtrl


class Storage:
    def __init__(self):
        self.__node_storage = pd.DataFrame({"NodeID": [],
                                            "NodeType": [],
                                            "Node": [],
                                            "X": [],
                                            "Y": [],
                                            "Z": [],
                                            "Force": [],
                                            "Displacement": []})

        self.__element_storage = pd.DataFrame({"ElementID": [],
                                               "ElementType": [],
                                               "Element": [],
                                               "Material": []})

        self.__material_storage = pd.DataFrame({"MaterialName": [],
                                                "Material": []})

        self.__section_storage = pd.DataFrame({"SectionName": [],
                                               "Section": []})

    @property
    def node_storage(self):
        return self.__node_storage

    @property
    def element_storage(self):
        return self.__element_storage

    @property
    def material_storage(self):
        return self.__material_storage

    @property
    def section_storage(self):
        return self.__section_storage

    @property
    def nodes_and_elements_dictionary_for_solver(self):
        nodes = dict(zip(self.__node_storage['NodeID'], self.__node_storage['Node']))
        elements = dict(zip(self.__element_storage['ElementID'], self.__element_storage['Element']))
        return nodes, elements

    def update_node(self, node):
        self.__node_storage = node.save_node_to_dataframe(self.__node_storage)

    def update_element(self, element):
        self.__element_storage = element.save_element_to_dataframe(self.__element_storage)

    def update_material(self, material: mtrl.Material):
        self.__material_storage = material.save_material_to_dataframe(self.__material_storage)

    def update_section(self, section: sct.Section):
        self.__section_storage = section.save_section_to_dataframe(self.__section_storage)

    def add_node_results(self, us, ps):
        displacements = []
        forces = []

        for nodes in self.__node_storage['Node']:
            codes = nodes.code
            nodes.set_result_displacements(tuple(us[codes].tolist()))
            nodes.set_result_forces(tuple(ps[codes].tolist()))
            displacements.append(us[codes])
            forces.append(ps[codes])

        self.__node_storage['Displacement'] = displacements
        self.__node_storage['Force'] = forces

    def remove_element(self, element_id: int):
        self.__element_storage[self.__element_storage['ElementID'] != element_id].reset_index(drop=True)

    def remove_node(self, node_id: int):
        self.__node_storage[self.__node_storage['NodeID'] != node_id].reset_index(drop=True)

    def remove_section(self, section_name: str):
        self.__section_storage[self.__section_storage['SectionName'] != section_name].reset_index(drop=True)

    def remove_material(self, material_name: str):
        self.__material_storage[self.__material_storage['MaterialName'] != material_name].reset_index(drop=True)
