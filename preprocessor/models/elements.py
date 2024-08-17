import numpy as np
import preprocessor.properties.material as mtrl
import preprocessor.properties.section as sct


class Strut(object):
    def __init__(self, strut_id, start_node, end_node, material, radius):
        self.__strut_id = strut_id
        self.__start_node = start_node
        self.__end_node = end_node
        self.__material = material
        self.__radius = radius

    @property
    def strut_id(self):
        return self.__strut_id

    @property
    def start_node(self):
        return self.__start_node

    @property
    def end_node(self):
        return self.__end_node

    @property
    def material(self):
        return self.__material

    @property
    def radius(self):
        return self.__radius


class ElementBrickEight:
    def __init__(self, element_id: int, connected_nodes: list, material_of_element: mtrl.Material):
        self.__element_id = element_id
        self.__connected_nodes = connected_nodes  # Bağlantı haritası [DN1 ... DN8]
        self.__material = material_of_element
        self.__boundary_force_on_x = np.zeros((6,))  # Sınır-Yüzey X [q1x, q2x, q3x, q4x, q5x, q6x]
        self.__boundary_force_on_y = np.zeros((6,))  # Sınır-Yüzey Y [q1y, q2y, q3y, q4y, q5y, q6y]
        self.__boundary_force_on_z = np.zeros((6,))  # Sınır-Yüzey Z [q1z, q2z, q3z, q4z, q5z, q6z]
        self.__volume_force = np.zeros((3,))  # Hacim Kuvvetleri [bx, by, bz]
        self.__temperature_change = 0  # Uniform sıcaklık değişimi (delta_T)

        self.__stiffness_matrix = None
        self.__thermal_force_vector = None
        self.__boundary_force_vector = None
        self.__volume_force_vector = None

        self.__nodal_coordinate_matrix = np.array([node.coordinates for node in self.__connected_nodes]).transpose()
        self.__master_points = [[-1, -1, -1],
                                [1, -1, -1],
                                [1, 1, -1],
                                [-1, 1, -1],
                                [-1, -1, 1],
                                [1, -1, 1],
                                [1, 1, 1],
                                [-1, 1, 1]]

    def __str__(self):
        nodes = ""
        for node in self.__connected_nodes:
            nodes = nodes + str(node.node_id) + ", "
        return "Element BrickEight - " + str(self.__element_id) + " between nodes: " + nodes[:-2]

    def __repr__(self):
        nodes = ""
        for node in self.__connected_nodes:
            nodes = nodes + str(node.node_id) + ", "
        return "Element BrickEight - " + str(self.__element_id) + " between nodes: " + nodes[:-2]

    def __int__(self):
        return self.__element_id

    def __calculate_jacobian_matrix(self, r, s, t):
        return self.__nodal_coordinate_matrix @ self.__calculate_df_dr(r, s, t)

    def __calculate_determinant_of_jacobian_matrix(self, r, s, t):
        return np.abs(np.linalg.det(self.__calculate_jacobian_matrix(r, s, t)))

    def __calculate_beta_matrix(self, r, s, t):
        df_dx = self.__calculate_df_dr(r, s, t) @ np.linalg.inv(self.__calculate_jacobian_matrix(r, s, t))
        beta_matrix = np.zeros((6, 24))
        beta_matrix[0, 0:8] = df_dx[:, 0]
        beta_matrix[1, 8:16] = df_dx[:, 1]
        beta_matrix[2, 16:24] = df_dx[:, 2]
        beta_matrix[3, 8:16] = df_dx[:, 2]
        beta_matrix[3, 16:24] = df_dx[:, 1]
        beta_matrix[4, 0:8] = df_dx[:, 2]
        beta_matrix[4, 16:24] = df_dx[:, 0]
        beta_matrix[5, 0:8] = df_dx[:, 1]
        beta_matrix[5, 8:16] = df_dx[:, 0]
        return beta_matrix

    def __calculate_stiffness_matrix(self):
        total = 0
        p = [-1 / 3 ** 0.5, 1 / 3 ** 0.5]
        w = [1, 1]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    beta_matrix = self.__calculate_beta_matrix(p[i], p[j], p[k])
                    jacobian_det = self.__calculate_determinant_of_jacobian_matrix(p[i], p[j], p[k])
                    dk = beta_matrix.T @ self.__material.constitutive_matrix @ beta_matrix * jacobian_det
                    total += (w[i] * w[j] * w[k]) * dk
        self.__stiffness_matrix = total

    def __calculate_volume_force_vector(self):
        total = 0
        p = [-1 / 3 ** 0.5, 1 / 3 ** 0.5]
        w = [1, 1]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    bx, by, bz = self.__volume_force
                    if bx == 0 and by == 0 and bz == 0:
                        db = np.zeros(24)
                    else:
                        shape_function_vector = self.__calculate_shape_functions(p[i], p[j], p[k])
                        shape_function_vector = np.concatenate(
                            (shape_function_vector, shape_function_vector, shape_function_vector))
                        db = self.__calculate_determinant_of_jacobian_matrix(p[i], p[j],
                                                                             p[k]) * shape_function_vector * (
                                     [bx] * 8 + [by] * 8 + [bz] * 8)
                    total += (w[i] * w[j] * w[k]) * db
        self.__volume_force_vector = total

    def __calculate_boundary_force_vector(self):
        total = 0
        p = [-1 / 3 ** 0.5, 1 / 3 ** 0.5]
        w = [1, 1]
        for i in range(2):
            for j in range(2):
                rb = [-1, 1, p[i], p[i], p[i], p[i]]
                sb = [p[i], p[i], -1, 1, p[j], p[j]]
                tb = [p[j], p[j], p[j], p[j], -1, 1]
                for k in range(6):
                    qx = self.__boundary_force_on_x[k]
                    qy = self.__boundary_force_on_y[k]
                    qz = self.__boundary_force_on_z[k]
                    if qx == 0 and qy == 0 and qz == 0:
                        ds = np.zeros(24)
                    else:
                        shape_function_vector = self.__calculate_shape_functions(rb[k], sb[k], tb[k])
                        jacobian_matrix = self.__calculate_jacobian_matrix(rb[k], sb[k], tb[k])
                        jacobian = 0
                        if k in [0, 1]:
                            jacobian = ((jacobian_matrix[0, 2] * jacobian_matrix[1, 1] - jacobian_matrix[0, 1] *
                                         jacobian_matrix[
                                             1, 2]) ** 2 +
                                        (jacobian_matrix[0, 2] * jacobian_matrix[2, 1] - jacobian_matrix[0, 1] *
                                         jacobian_matrix[
                                             2, 2]) ** 2 +
                                        (jacobian_matrix[1, 2] * jacobian_matrix[2, 1] - jacobian_matrix[1, 1] *
                                         jacobian_matrix[
                                             2, 2]) ** 2) ** 0.5
                        if k in [2, 3]:
                            jacobian = ((jacobian_matrix[0, 2] * jacobian_matrix[1, 0] - jacobian_matrix[0, 0] *
                                         jacobian_matrix[
                                             1, 2]) ** 2 +
                                        (jacobian_matrix[0, 2] * jacobian_matrix[2, 0] - jacobian_matrix[0, 0] *
                                         jacobian_matrix[
                                             2, 2]) ** 2 +
                                        (jacobian_matrix[1, 2] * jacobian_matrix[2, 0] - jacobian_matrix[1, 0] *
                                         jacobian_matrix[
                                             2, 2]) ** 2) ** 0.5
                        if k in [4, 5]:
                            jacobian = ((jacobian_matrix[0, 1] * jacobian_matrix[1, 0] - jacobian_matrix[0, 0] *
                                         jacobian_matrix[
                                             1, 1]) ** 2 +
                                        (jacobian_matrix[0, 1] * jacobian_matrix[2, 0] - jacobian_matrix[0, 0] *
                                         jacobian_matrix[
                                             2, 1]) ** 2 +
                                        (jacobian_matrix[1, 1] * jacobian_matrix[2, 0] - jacobian_matrix[1, 0] *
                                         jacobian_matrix[
                                             2, 1]) ** 2) ** 0.5
                        ds = jacobian * np.concatenate(
                            (shape_function_vector * qx, shape_function_vector * qy, shape_function_vector * qz))

                    total += w[i] * w[j] * ds
        self.__boundary_force_vector = total

    def __calculate_thermal_force_vector(self):
        total = 0
        p = [-1 / 3 ** 0.5, 1 / 3 ** 0.5]
        w = [1, 1]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    alpha = self.__material.thermal_expansion
                    deltaT = self.__temperature_change
                    if alpha == 0 or deltaT == 0:
                        dt = np.zeros(24)
                    else:
                        ALPHA = np.asarray([alpha, alpha, alpha, 0, 0, 0])
                        C = self.__material.constitutive_matrix
                        B = self.__calculate_beta_matrix(p[i], p[j], p[k])
                        J = self.__calculate_determinant_of_jacobian_matrix(p[i], p[j], p[k])
                        dt = B.T @ C @ ALPHA * deltaT * J
                    total += (w[i] * w[j] * w[k]) * dt
        self.__thermal_force_vector = total

    def save_element_to_dataframe(self, element_storage):
        element_storage.loc[self.__element_id] = {"ElementID": self.__element_id,
                                                  "ElementType": str(self),
                                                  "Element": self,
                                                  "Material": self.__material}
        return element_storage

    def set_solution(self, u_system):
        self.__u = u_system[self.code]

    def __calculate_shape_functions(self, r, s, t):
        return 0.125 * np.asarray([(1 + ri * r) * (1 + si * s) * (1 + ti * t)
                                   for ri, si, ti in self.__master_points])

    def __calculate_df_dr(self, r, s, t):
        return 0.125 * np.asarray([[(ri) * (1 + si * s) * (1 + ti * t), (1 + ri * r) * (si) * (1 + ti * t),
                                    (1 + ri * r) * (1 + si * s) * (ti)] for ri, si, ti in self.__master_points])

    def set_boundary_force_on_x(self, vector: np.ndarray):
        self.__boundary_force_on_x = vector

    def set_boundary_force_on_y(self, vector: np.ndarray):
        self.__boundary_force_on_y = vector

    def set_boundary_force_on_z(self, vector: np.ndarray):
        self.__boundary_force_on_z = vector

    def set_volume_force(self, vector: np.ndarray):
        self.__volume_force = vector

    def set_temperature_change(self, temperature: float):
        self.__temperature_change = temperature

    @property
    def export_name(self):
        return "brick"

    @property
    def material(self):
        return self.__material

    @property
    def code(self):
        return [n.code[0] for n in self.__connected_nodes] + [n.code[1] for n in self.__connected_nodes] + \
            [n.code[2] for n in self.__connected_nodes]

    @property
    def element_id(self):
        return self.__element_id

    @property
    def connected_nodes(self):
        return self.__connected_nodes

    @property
    def boundary_force_on_x(self):
        return self.__boundary_force_on_x

    @property
    def boundary_force_on_y(self):
        return self.__boundary_force_on_y

    @property
    def boundary_force_on_z(self):
        return self.__boundary_force_on_z

    @property
    def volume_force(self):
        return self.__volume_force

    @property
    def tempreture_change(self):
        return self.__temperature_change

    @property
    def stiffness_matrix(self):
        if self.__stiffness_matrix is None:
            self.__calculate_stiffness_matrix()
        return self.__stiffness_matrix

    @property
    def rhs_vector(self):
        if self.__boundary_force_vector is None:
            self.__calculate_boundary_force_vector()
        if self.__volume_force_vector is None:
            self.__calculate_volume_force_vector()
        if self.__thermal_force_vector is None:
            self.__calculate_thermal_force_vector()

        return self.__boundary_force_vector + self.__volume_force_vector + self.__thermal_force_vector


class ElementStrutTwo:
    def __init__(self, element_id, connected_nodes, material_of_element: mtrl.Material, cross_section: sct.Section,
                 omega_angle=0):
        self.__element_id = element_id
        self.__connected_nodes = connected_nodes
        self.__material = material_of_element  # Malzeme
        self.__cross_section = cross_section  # Kesit
        self.__omega_angle = np.pi / 180 * omega_angle
        self.__distributed_load = [0] * 6

        self.__length_vector = self.__connected_nodes[1].coordinates - self.__connected_nodes[0].coordinates
        self.__length = (self.__length_vector[0] ** 2 + self.__length_vector[1] ** 2 + self.__length_vector[
            2] ** 2) ** 0.5

        self.__transform_matrix = None
        self.__boundary_force_vector = None
        self.__weight_vector = None
        self.__stiffness_matrix = None

    def __str__(self):
        return "Element StrutTwo - " + str(self.__element_id) + " between nodes:" + str(
            self.__connected_nodes[0].node_id) + "-" + str(self.__connected_nodes[1].node_id)

    def __repr__(self):
        return "Element StrutTwo - " + str(self.__element_id) + " between nodes:" + str(
            self.__connected_nodes[0].node_id) + "-" + str(self.__connected_nodes[1].node_id)

    def __int__(self):
        return self.__element_id

    def save_element_to_dataframe(self, element_storage):
        element_storage.loc[self.__element_id] = {"ElementID": self.__element_id,
                                                  "ElementType": str(self),
                                                  "Element": self,
                                                  "Material": self.__material}
        return element_storage

    def __calculate_transform_matrix(self):
        transform_omega = np.asarray([[1, 0, 0],
                                      [0, np.cos(self.__omega_angle), np.sin(self.__omega_angle)],
                                      [0, -np.sin(self.__omega_angle), np.cos(self.__omega_angle)]])

        nx, ny, nz = self.__length_vector[0] / self.__length, self.__length_vector[1] / self.__length, \
                     self.__length_vector[2] / self.__length

        if np.abs(1 - nz ** 2) < 0.001:
            trans_from_alpha = np.asarray([[nx, ny, nz],
                                           [1, 0, 0],
                                           [0, nz, -ny]])
        else:
            a = 1 / (1 - nz ** 2)
            trans_from_alpha = np.asarray([[nx, ny, nz],
                                           [-a * nx * nz, -a * ny * nz, 1],
                                           [a * ny, -a * nx, 0]])

        n1, n2 = self.__connected_nodes
        transfrom_beta_1 = n1.calculate_transformation_matrix()
        transfrom_beta_2 = n2.calculate_transformation_matrix()

        self.__transform_matrix = np.identity(12)
        self.__transform_matrix[0:3, 0:3] = transform_omega @ trans_from_alpha @ transfrom_beta_1
        self.__transform_matrix[3:6, 3:6] = transform_omega @ trans_from_alpha @ transfrom_beta_1
        self.__transform_matrix[6:9, 6:9] = transform_omega @ trans_from_alpha @ transfrom_beta_2
        self.__transform_matrix[9:12, 9:12] = transform_omega @ trans_from_alpha @ transfrom_beta_2

    def __calculate_stiffness_matrix(self):
        E = self.__material.youngs_modulus
        G = self.__material.shear_modulus

        A = self.__cross_section.area
        Ix = self.__cross_section.i_xx
        Iy = self.__cross_section.i_yy
        Iz = self.__cross_section.i_zz
        Iyz = self.__cross_section.i_yz

        EA, GIx, EIy, EIz, EIyz = E * A, G * Ix, E * Iy, E * Iz, E * Iyz
        L = self.__length

        L2, L3 = L ** 2, L ** 3
        ku = EA / L
        ktx = GIx / L
        k1z, k1y, k1yz = 2 * EIz / L, 2 * EIy / L, 2 * EIyz / L
        k2z, k2y, k2yz = 6 * EIz / L2, 6 * EIy / L2, 6 * EIyz / L2
        k3z, k3y, k3yz = 12 * EIz / L3, 12 * EIy / L3, 12 * EIyz / L3
        k_local = np.array([

            [ku, 0, 0, 0, 0, 0, -ku, 0, 0, 0, 0, 0],
            [0, k3z, k3yz, 0, -k2yz, k2z, 0, -k3z, -k3yz, 0, -k2yz, k2z],
            [0, k3yz, k3y, 0, -k2y, k2yz, 0, -k3yz, -k3y, 0, -k2y, k2yz],
            [0, 0, 0, ktx, 0, 0, 0, 0, 0, -ktx, 0, 0],
            [0, -k2yz, -k2y, 0, 2 * k1y, -2 * k1yz, 0, k2yz, k2y, 0, k1y, -k1yz],
            [0, k2z, k2yz, 0, -2 * k1yz, 2 * k1z, 0, -k2z, -k2yz, 0, -k1yz, k1z],
            [-ku, 0, 0, 0, 0, 0, ku, 0, 0, 0, 0, 0],
            [0, -k3z, -k3yz, 0, k2yz, -k2z, 0, k3z, k3yz, 0, k2yz, -k2z],
            [0, -k3yz, -k3y, 0, k2y, -k2yz, 0, k3yz, k3y, 0, k2y, -k2yz],
            [0, 0, 0, -ktx, 0, 0, 0, 0, 0, ktx, 0, 0],
            [0, -k2yz, -k2y, 0, k1y, -k1yz, 0, k2yz, k2y, 0, 2 * k1y, -2 * k1yz],
            [0, k2z, k2yz, 0, -k1yz, k1z, 0, -k2z, -k2yz, 0, -2 * k1yz, 2 * k1z]])

        self.__stiffness_matrix = np.linalg.inv(self.transform_matrix) @ k_local @ self.transform_matrix

    def __calculate_boundary_force_vector(self):
        qx, qy, qz, mx, my, mz = self.__distributed_load
        q_local = [0.5 * qx * self.__length,
                   0.5 * qy * self.__length - mz,
                   0.5 * qz * self.__length + my,
                   0.5 * mx * self.__length,
                   -qz * self.__length ** 2 / 12,
                   qy * self.__length ** 2 / 12,
                   0.5 * qx * self.__length,
                   0.5 * qy * self.__length + mz,
                   0.5 * qz * self.__length - my,
                   0.5 * mx * self.__length,
                   qz * self.__length ** 2 / 12,
                   -qy * self.__length ** 2 / 12]
        self.__boundary_force_vector = np.linalg.inv(self.transform_matrix) @ q_local

    def __calculate_weight_vector(self):
        gravity_load = - self.__material.unit_weight * self.__cross_section.area
        mx = 0.0
        gravity_local = [0,
                         0.5 * gravity_load * self.__length,
                         0.,
                         0.5 * mx * self.__length,
                         0,
                         gravity_load * self.__length ** 2 / 12,
                         0,
                         0.5 * gravity_load * self.__length,
                         0.,
                         0.5 * mx * self.__length, 0,
                         -gravity_load * self.__length ** 2 / 12]
        self.__weight_vector = np.linalg.inv(self.transform_matrix) @ gravity_local

    @property
    def export_name(self):
        return "strut"

    @property
    def stiffness_matrix(self):
        if self.__stiffness_matrix is None:
            self.__calculate_stiffness_matrix()
        return self.__stiffness_matrix

    @property
    def code(self):  # Kod-Vektörü [u1,v1,w1,t1x,t1y,t1z,u2,v2,w2,t2x,t2y,t2z]
        n1, n2 = self.__connected_nodes
        return n1.code + n2.code

    @property
    def rhs_vector(self):
        if self.__boundary_force_vector is None:
            self.__calculate_boundary_force_vector()
        if self.__material.unit_weight == 0.0:
            return self.__boundary_force_vector
        else:
            if self.__weight_vector is None:
                self.__calculate_weight_vector()
            return self.__weight_vector + self.__boundary_force_vector

    @property
    def distributed_force(self):
        return self.__distributed_load[0:3]

    @property
    def distributed_moment(self):
        return self.__distributed_load[3:6]

    @property
    def transform_matrix(self):
        if self.__transform_matrix is None:
            self.__calculate_transform_matrix()
        return self.__transform_matrix

    @property
    def connected_nodes(self):
        return self.__connected_nodes

    def set_distributed_force(self, distributed_load: np.ndarray):
        self.__distributed_load[0:3] = distributed_load

    def set_distributed_moment(self, distributed_load: np.ndarray):
        self.__distributed_load[3:6] = distributed_load
