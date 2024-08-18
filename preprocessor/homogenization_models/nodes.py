import numpy as np


class Node(object):
    def __init__(self, node_id, x, y, z):
        self.__node_id = node_id
        self.__x = x
        self.__y = y
        self.__z = z

    def get_coordinate_array(self):
        return np.array([self.__x, self.__y, self.__z])

    @property
    def node_id(self):
        return self.__node_id

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z


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
                                            "NodeType": str(self),
                                            "Node": self,
                                            "X": self.__coordinates[0],
                                            "Y": self.__coordinates[1],
                                            "Z": self.__coordinates[2]}
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


class NodeStrut:
    def __init__(self, node_id: int, coordinates: tuple):
        self.__node_id = node_id
        self.__coordinates = np.array(coordinates)
        self.__rest = np.zeros(6, )
        self.__displacements = np.zeros((6,))
        self.__code = [-1] * 6  # Serbestlikler (Kod) [dx, dy, dz, tx, ty, tz]
        self.__euler_angles = np.zeros((3,))  # Lokal eksen Euler açıları [betaZ, beyaY, betaX]
        self.__moments = np.zeros((3,))
        self.__forces = np.zeros((3,))
        self.__result_displacements = None
        self.__result_forces = None

    def __str__(self):
        return "Node Strut - " + str(self.__node_id) + " at " + str(self.__coordinates)

    def __repr__(self):
        return "Node Solid - " + str(self.__node_id) + " at " + str(self.__coordinates)

    def __int__(self):
        return self.__node_id

    def save_node_to_dataframe(self, node_storage):
        node_storage.loc[self.__node_id] = {"NodeID": self.__node_id,
                                            "NodeType": str(self),
                                            "Node": self,
                                            "X": self.__coordinates[0],
                                            "Y": self.__coordinates[1],
                                            "Z": self.__coordinates[2]}
        return node_storage

    def calculate_transformation_matrix(self):  # ZYX Euler dönüşüm matrisi
        euler_angles = np.pi / 180 * np.array(self.__euler_angles)
        cx, cy, cz = np.cos(euler_angles)
        sx, sy, sz = np.sin(euler_angles)
        return np.asarray([[cy * cz, cz * sx * sy - cx * sz, sx * sz + cx * cz * sy],
                           [cy * sz, cx * cz + sx * sy * sz, cx * sy * sz - cz * sx],
                           [-sy, cy * sx, cx * cy]])

    @property
    def export_name(self):
        return "nodestrtut"

    @property
    def force(self):  # Sistem denklemine katkı yapacak .force vektörü hesaplanıyor.
        transformation_matrix = np.linalg.inv(self.calculate_transformation_matrix())
        p = transformation_matrix @ self.__forces
        m = transformation_matrix @ self.__moments
        return np.array([*p, *m])

    @property
    def displacement(self):
        return np.array(self.__displacements)

    @property
    def euler_angles(self):
        return self.__euler_angles

    @property
    def rest(self):
        return self.__rest

    @property
    def node_id(self):
        return self.__node_id

    @property
    def coordinates(self):
        return self.__coordinates

    @property
    def code(self):
        return self.__code

    @property
    def result_displacements(self):
        return self.__result_displacements

    @property
    def result_forces(self):
        return self.__result_forces

    @property
    def x(self):
        return self.__coordinates[0]

    @property
    def y(self):
        return self.__coordinates[1]

    @property
    def z(self):
        return self.__coordinates[2]

    def set_result_displacements(self, vector: tuple):
        self.__result_displacements = np.array(vector)

    def set_result_forces(self, vector: tuple):
        self.__result_forces = np.array(vector)

    def set_displacement(self, vector: tuple):
        self.__displacements = np.array(vector)

    def set_rest(self, vector: tuple):
        self.__rest = np.array(vector)

    def set_euler_angles(self, vector: tuple):
        self.__euler_angles = np.array(vector)

    def set_force(self, vector: tuple):
        self.__forces = np.array(vector)

    def set_moment(self, vector: tuple):
        self.__moments = np.array(vector)