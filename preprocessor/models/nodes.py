import numpy as np
import pandas as pd


class Nodes(object):
    def __init__(self):
        self.__data = pd.DataFrame({'NodeID': [],
                                    'X': [],
                                    'Y': [],
                                    'Z': [],
                                    "RestX": [],
                                    "RestY": [],
                                    "RestZ": [],
                                    "RestThetaX": [],
                                    "RestThetaY": [],
                                    "RestThetaZ": [],
                                    "ForceX": [],
                                    "ForceY": [],
                                    "ForceZ": [],
                                    "MomentX": [],
                                    "MomentY": [],
                                    "MomentZ": [],
                                    "DisplacementX": [],
                                    "DisplacementY": [],
                                    "DisplacementZ": [],
                                    "DisplacementThetaX": [],
                                    "DisplacementThetaY": [],
                                    "DisplacementThetaZ": [],
                                    "CodeX": [],
                                    "CodeY": [],
                                    "CodeZ": [],
                                    "CodeThetaX": [],
                                    "CodeTheta": [],
                                    "CodeThetaZ": [],
                                    "EulerAngleZ": [],
                                    "EulerAngleY": [],
                                    "EulerAngleX": [],
                                    "ResultDisplacementX": [],
                                    "ResultDisplacementY": [],
                                    "ResultDisplacementZ": [],
                                    "ResultDisplacementThetaX": [],
                                    "ResultDisplacementThetaY": [],
                                    "ResultDisplacementThetaZ": [],
                                    "ResultForceX": [],
                                    "ResultForceY": [],
                                    "ResultForceZ": [],
                                    "ResultMomentX": [],
                                    "ResultMomentY": [],
                                    "ResultMomentZ": [],
                                    })

    @property
    def data(self):
        return self.__data

    def set_data(self, node_dataframe: pd.DataFrame):
        self.__data = node_dataframe

    def add_rest_x(self, node_id: np.array, clean_rests: bool = False):
        mask = self.__data['NodeID'].isin(node_id)
        if clean_rests:
            self.__data.loc[mask, 'RestX'] = 0
        else:
            self.__data.loc[mask, 'RestX'] = 1

    def add_rest_y(self, node_id: np.array, clean_rests: bool = False):
        mask = self.__data['NodeID'].isin(node_id)
        if clean_rests:
            self.__data.loc[mask, 'RestY'] = 0
        else:
            self.__data.loc[mask, 'RestY'] = 1

    def add_rest_z(self, node_id: np.array, clean_rests: bool = False):
        mask = self.__data['NodeID'].isin(node_id)
        if clean_rests:
            self.__data.loc[mask, 'RestZ'] = 0
        else:
            self.__data.loc[mask, 'RestZ'] = 1

    def add_displacement_x(self, node_id: np.array, displacement: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'DisplacementX'] = displacement

    def remove_displacement_x(self, node_id: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'DisplacementX'] = 0

    def add_displacement_y(self, node_id: np.array, displacement: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'DisplacementY'] = displacement

    def remove_displacement_y(self, node_id: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'DisplacementY'] = 0

    def add_displacement_z(self, node_id: np.array, displacement: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'DisplacementZ'] = displacement

    def remove_displacement_z(self, node_id: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'DisplacementZ'] = 0

    def add_force_x(self, node_id: np.array, force: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'ForceX'] = force

    def remove_force_x(self, node_id: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'ForceX'] = 0

    def add_force_y(self, node_id: np.array, force: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'ForceY'] = force

    def remove_force_y(self, node_id: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'ForceY'] = 0

    def add_force_z(self, node_id: np.array, force: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'ForceZ'] = force

    def remove_force_z(self, node_id: np.array):
        mask = self.__data['NodeID'].isin(node_id)
        self.__data.loc[mask, 'ForceZ'] = 0

    def get_node_id_by_coordinates_x_as_plane(self, coordinate: float, tolerance: float = 1.0e-5):
        mask = self.__data["X"].between(coordinate - tolerance, coordinate + tolerance)
        return self.__data.loc[mask, 'NodeID'].values

    def get_node_id_by_coordinates_y_as_plane(self, coordinate: float, tolerance: float = 1.0e-5):
        mask = self.__data["Y"].between(coordinate - tolerance, coordinate + tolerance)
        return self.__data.loc[mask, 'NodeID'].values

    def get_node_id_by_coordinates_z_as_plane(self, coordinate: float, tolerance: float = 1.0e-5):
        mask = self.__data["Z"].between(coordinate - tolerance, coordinate + tolerance)
        return self.__data.loc[mask, 'NodeID'].values

    def get_node_id_by_coordinates_x_as_line(self, coordinate_y: float, coordinate_z: float,
                                             tolerance: float = 1.0e-5):
        mask1 = self.__data["Y"].between(coordinate_y - tolerance, coordinate_y + tolerance)
        mask2 = self.__data["Z"].between(coordinate_z - tolerance, coordinate_z + tolerance)
        mask = mask1 & mask2
        return self.__data.loc[mask, 'NodeID'].values

    def get_node_id_by_coordinates_y_as_line(self, coordinate_x: float, coordinate_z: float,
                                             tolerance: float = 1.0e-5):
        mask1 = self.__data["X"].between(coordinate_x - tolerance, coordinate_x + tolerance)
        mask2 = self.__data["Z"].between(coordinate_z - tolerance, coordinate_z + tolerance)
        mask = mask1 & mask2
        return self.__data.loc[mask, 'NodeID'].values

    def get_node_id_by_coordinates_z_as_line(self, coordinate_x: float, coordinate_y: float,
                                             tolerance: float = 1.0e-5):
        mask1 = self.__data["X"].between(coordinate_x - tolerance, coordinate_x + tolerance)
        mask2 = self.__data["Y"].between(coordinate_y - tolerance, coordinate_y + tolerance)
        mask = mask1 & mask2
        return self.__data.loc[mask, 'NodeID'].values

    def get_node_id_from_volume(self, min_coordinates: tuple, max_coordinates: tuple):
        mask1 = self.__data["X"].between(min_coordinates[0], max_coordinates[0])
        mask2 = self.__data["Y"].between(min_coordinates[1], max_coordinates[1])
        mask3 = self.__data["Z"].between(min_coordinates[2], max_coordinates[2])
        mask = mask1 & mask2
        mask = mask & mask3
        return self.__data.loc[mask, "NodeID"].values


class NodeSolid:
    def __init__(self, node_id: int, coordinates: tuple):
        self.__node_id = node_id
        self.__coordinates = np.array(coordinates)
        self.__rest = np.array([0, 0, 0])
        self.__forces = np.array([0, 0, 0])
        self.__displacements = np.array([0, 0, 0])
        self.__code = [-1, -1, -1]
        self.__values = []
        self.__result_displacements = None
        self.__result_forces = None

    def __str__(self):
        return "Node Solid - " + str(self.__node_id) + " at " + str(self.__coordinates)

    def __repr__(self):
        return "Node Solid - " + str(self.__node_id) + " at " + str(self.__coordinates)

    def __int__(self):
        return self.__node_id

    def save_node_to_dataframe(self, node_storage):
        node_storage.loc[self.__node_id] = {"NodeID": self.__node_id,
                                            "Node": self, }
        return node_storage

    @property
    def export_name(self):
        return "nodesolid"

    @property
    def mean_value(self):
        return sum(self.__values) / len(self.__values)

    @property
    def node_id(self):
        return self.__node_id

    @property
    def coordinates(self):
        return self.__coordinates

    @property
    def rest(self):
        return self.__rest

    @property
    def force(self):
        return self.__forces

    @property
    def displacement(self):
        return self.__displacements

    @property
    def code(self):
        return self.__code

    @property
    def forces(self):
        return self.__forces

    @property
    def result_displacements(self):
        return self.__result_displacements

    @property
    def result_forces(self):
        return self.__result_forces

    def set_result_displacements(self, vector: tuple):
        self.__result_displacements = np.array(vector)

    def set_result_forces(self, vector: tuple):
        self.__result_forces = np.array(vector)

    def set_coordinates(self, coordinates: tuple):
        self.__coordinates = np.array(coordinates)

    def set_rest(self, vector: tuple):
        self.__rest = np.array(vector)

    def set_force(self, vector: tuple):
        self.__forces = np.array(vector)

    def set_displacement(self, vector: tuple):
        self.__displacements = np.array(vector)

    def ExternalForceVectorToContribute(self):
        return self.force
