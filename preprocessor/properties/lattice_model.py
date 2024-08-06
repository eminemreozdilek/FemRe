import numpy as np

from preprocessor.properties import material


class LatticeModel:
    def __init__(self):
        self.__model_resolution = 1
        self.__node_lookup_table = {}
        self.__strut_lookup_table = {}
        self.__material_lookup_table = {}
        self.__voxel_array = np.zeros((self.__model_resolution, self.__model_resolution, self.__model_resolution))
        self.__geometry_size = (10, 10, 10)
        self.__standart_thickness = None

    def set_tables(self, node_lookup_table, strut_lookup_table, material_lookup_table):
        self.__node_lookup_table = node_lookup_table
        self.__strut_lookup_table = strut_lookup_table
        self.__material_lookup_table = material_lookup_table

    def set_resolution(self, resolution: int):
        self.__model_resolution = resolution

    def set_geometry_size(self, geometry_size):
        self.__geometry_size = geometry_size

    def set_standart_thickness(self, thickness: float):
        self.__standart_thickness = thickness

    def generate_voxel(self):
        size = 1 / self.__model_resolution
        matrix_coordinates = np.nonzero(
            np.ones((self.__model_resolution, self.__model_resolution, self.__model_resolution)))
        matrix_coordinates = np.vstack((matrix_coordinates[0], matrix_coordinates[1], matrix_coordinates[2]))
        matrix_coordinates = matrix_coordinates.transpose()
        matrix_coordinates = np.add(matrix_coordinates, 0.5) * size

        nodes = self.__node_lookup_table
        struts = self.__strut_lookup_table
        materials = self.__material_lookup_table

        material_voxels = {}
        for key in range(len(materials)):
            material_voxels[key + 1] = np.zeros(
                (self.__model_resolution, self.__model_resolution, self.__model_resolution))

        for strut_key in struts:
            material_code = struts[strut_key].material.material_id

            first_node_coords = struts[strut_key].start_node.get_coordinate_array()
            second_node_coords = struts[strut_key].end_node.get_coordinate_array()

            b = np.sqrt(np.sum(np.square(first_node_coords - second_node_coords)))
            b = np.tile(b, (matrix_coordinates.shape[0],))
            first_node_coords = np.tile(first_node_coords, (matrix_coordinates.shape[0], 1))
            second_node_coords = np.tile(second_node_coords, (matrix_coordinates.shape[0], 1))

            delta_first = matrix_coordinates - first_node_coords
            delta_last = matrix_coordinates - second_node_coords
            distance_first_node = np.sqrt(np.sum(np.square(delta_first), axis=1))
            distance_second_node = np.sqrt(np.sum(np.square(delta_last), axis=1))

            a = np.sqrt(np.sum(np.square(first_node_coords - matrix_coordinates), axis=1))
            c = np.sqrt(np.sum(np.square(second_node_coords - matrix_coordinates), axis=1))

            cos_alpha = np.divide(np.square(a) + np.square(b) - np.square(c), 2 * a * b)
            cos_beta = np.divide(np.square(c) + np.square(b) - np.square(a), 2 * c * b)
            l_alpha = a * cos_alpha
            l_beta = c * cos_beta
            over_alpha = l_alpha > b
            over_beta = l_beta > b
            clears = np.logical_and(np.logical_not(over_alpha), np.logical_not(over_beta))
            distance_over_a = 1 * over_alpha * a
            distance_over_b = 1 * over_beta * c
            distance_clears = 1 * clears * a * np.sqrt(1 - np.square(cos_alpha))

            distance = distance_over_a + distance_over_b + distance_clears

            if self.__standart_thickness is None:
                radius = struts[strut_key].radius
            else:
                radius = self.__standart_thickness / 2

            self.__voxel_array = np.logical_or(distance < radius,
                                               np.isclose(distance, radius, atol=1.0e-10)).astype(int)
            material_voxels[material_code] = np.maximum(material_voxels[material_code], self.__voxel_array.reshape(
                (self.__model_resolution, self.__model_resolution, self.__model_resolution)))

            self.__voxel_array = np.logical_or(distance_first_node < radius,
                                               np.isclose(distance, radius, atol=1.0e-10)).astype(int)
            material_voxels[material_code] = np.maximum(material_voxels[material_code], self.__voxel_array.reshape(
                (self.__model_resolution, self.__model_resolution, self.__model_resolution)))

            self.__voxel_array = np.logical_or(distance_second_node < radius,
                                               np.isclose(distance, radius, atol=1.0e-10)).astype(int)
            material_voxels[material_code] = np.maximum(material_voxels[material_code], self.__voxel_array.reshape(
                (self.__model_resolution, self.__model_resolution, self.__model_resolution)))

        self.__voxel_array = np.zeros((self.__model_resolution, self.__model_resolution, self.__model_resolution))
        for key in material_voxels:
            self.__voxel_array = np.maximum(self.__voxel_array, material_voxels[key])

    def calculate_new_material(self, contained_materials):
        modulus_of_elasticity = 0
        poissons_ratio = 0
        thermal_conductivity = 0

        for index in contained_materials:
            material_id = tuple([index])
            modulus_of_elasticity += self.__material_lookup_table[material_id].modulus_of_elasticity
            poissons_ratio += self.__material_lookup_table[material_id].poissons_ratio
            thermal_conductivity += self.__material_lookup_table[material_id].thermal_conductivity
            modulus_of_elasticity = modulus_of_elasticity / len(contained_materials)
            poissons_ratio = poissons_ratio / len(contained_materials)
            thermal_conductivity = thermal_conductivity / len(contained_materials)

        self.__material_lookup_table[contained_materials] = material.Material(len(self.__material_lookup_table) + 1,
                                                                              modulus_of_elasticity, poissons_ratio,
                                                                              thermal_conductivity)

    @property
    def characterize(self):
        lambdas = []
        mus = []
        thermals = []
        for index in self.__material_lookup_table:
            material_id = self.__material_lookup_table[index]
            lambdas.append(
                self.get_lames_first_parameter(material_id.modulus_of_elasticity, material_id.poissons_ratio))
            mus.append(self.get_lames_second_parameter(material_id.modulus_of_elasticity, material_id.poissons_ratio))
            thermals.append(material_id.thermal_conductivity)
        return lambdas, mus, thermals

    @property
    def volume_fraction(self):
        return np.count_nonzero(self.__voxel_array) / self.__voxel_array.size

    @property
    def voxel_array(self):
        return self.__voxel_array

    @property
    def materials(self):
        return self.__material_lookup_table

    @property
    def struts(self):
        return self.__strut_lookup_table

    @property
    def nodes(self):
        return self.__node_lookup_table

    @property
    def geometry_size(self):
        return self.__geometry_size

    @property
    def active_lattice_model(self):
        return self.__

    def get_lames_first_parameter(self, youngs_modulus, poissons_ratio):
        return youngs_modulus * poissons_ratio / ((1 + poissons_ratio) * (1 - 2 * poissons_ratio))

    def get_lames_second_parameter(self, youngs_modulus, poissons_ratio):
        return youngs_modulus / (2 * (1 + poissons_ratio))
