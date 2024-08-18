import numpy as np
import pandas as pd

class Material(object):
    def __init__(self,
                 material_id: int,
                 youngs_modulus: float,
                 poissons_ratio: float = 0.0,
                 thermal_conductivity: float = 0.0,
                 thermal_expansion_coefficent: float = 0.0,
                 unit_weight: float = 0.0,
                 name=""):
        self.__name = name
        self.__material_id = material_id
        self.__youngs_modulus = youngs_modulus
        self.__poissons_ratio = poissons_ratio
        self.__thermal_conductivity = thermal_conductivity
        self.__thermal_expansion_coefficent = thermal_expansion_coefficent
        self.__unit_weight = unit_weight

    @property
    def material_id(self):
        return self.__material_id

    @property
    def youngs_modulus(self):
        return self.__youngs_modulus

    @property
    def poissons_ratio(self):
        return self.__poissons_ratio

    @property
    def thermal_conductivity(self):
        return self.__thermal_conductivity

    @property
    def thermal_expansion_coefficent(self):
        return self.__thermal_expansion_coefficent

    @property
    def unit_weight(self):
        return self.__unit_weight

    @property
    def compliance_matrix(self):
        p = self.__poissons_ratio
        return self.__youngs_modulus / ((1 + p) * (1 - 2 * p)) * np.asarray([[1 - p, p, p, 0, 0, 0],
                                                                             [p, 1 - p, p, 0, 0, 0],
                                                                             [p, p, 1 - p, 0, 0, 0],
                                                                             [0, 0, 0, 0.5 - p, 0, 0],
                                                                             [0, 0, 0, 0, 0.5 - p, 0],
                                                                             [0, 0, 0, 0, 0, 0.5 - p]])

    def get_lame_parameters(self):
        return self.__youngs_modulus * self.__poissons_ratio / (
                (1 + self.__poissons_ratio) * (1 - 2 * self.__poissons_ratio)), self.__youngs_modulus / (
                       2 * (1 + self.__poissons_ratio))


class NonLinearMaterial(Material):
    def __init__(self, material_id,
                 modulus_of_elasticity,
                 poissons_ratio,
                 yield_strength,
                 tensile_strength,
                 yield_strain=0.002,
                 tensile_strain=0.30,
                 thermal_conductivity=1.0,
                 thermal_expansion_coefficent=0.0,
                 unit_weight=0.0,
                 name=""):
        super().__init__(material_id, modulus_of_elasticity, poissons_ratio, thermal_conductivity)
        self.__name = name
        self.__material_id = material_id
        self.__modulus_of_elasticity = modulus_of_elasticity
        self.__poissons_ratio = poissons_ratio
        self.__thermal_conductivity = thermal_conductivity
        self.__contained_materials = tuple([self.__material_id])
        self.__yield_strength = yield_strength
        self.__tensile_strength = tensile_strength
        self.__yield_strain = yield_strain
        self.__tensile_strain = tensile_strain
        self.__thermal_expansion_coefficent = thermal_expansion_coefficent
        self.__unit_weight = unit_weight

        self.__calculate_ramberg_osgoon()

    def __calculate_ramberg_osgoon(self):
        n = (np.log(
            (self.__tensile_strain - self.__tensile_strength / self.__modulus_of_elasticity) / self.__yield_strain)
             / np.log(self.__tensile_strength / self.__yield_strength))
        self.__stress_array = np.linspace(0, self.__tensile_strength, 1000)

        self.__ramberg_osgoon_strain = (self.__stress_array / self.__modulus_of_elasticity) + 0.002 * (
                self.__stress_array / self.__yield_strength) ** n
        self.__engineering_energy = self.__ramberg_osgoon_strain * self.__stress_array / 2

    def calculate_engineering_stress_and_strain_multiplayers(self, linear_strain):
        calculated_energy = np.square(linear_strain) * self.__modulus_of_elasticity / 2
        engineering_stress = np.interp(calculated_energy, self.__engineering_energy, self.__stress_array)
        engineering_strain = np.interp(calculated_energy, self.__engineering_energy, self.__ramberg_osgoon_strain)

        engineering_stress_coefficient = engineering_stress / (linear_strain * self.__modulus_of_elasticity)
        engineering_strain_coefficient = engineering_strain / linear_strain
        return engineering_stress_coefficient, engineering_strain_coefficient

    def plot_ramberg_osgoon_curve(self):
        specific_points = [(self.__tensile_strain, self.__tensile_strength),
                           (self.__yield_strain, self.__yield_strength)]

        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()

        ax1.scatter(*zip(*specific_points), color='red')

        for point in specific_points:
            ax1.annotate(f'({point[0]}, {point[1]})', xy=point)
        ax1.plot(self.__ramberg_osgoon_strain, self.__stress_array, label='Curve')
        ax1.plot(self.__stress_array / self.__modulus_of_elasticity, self.__stress_array, label='Youngs Modulus')

        ax2.plot(self.__ramberg_osgoon_strain,
                 self.__modulus_of_elasticity * np.ones(self.__ramberg_osgoon_strain.shape),
                 label='Youngs Modulus')
        ax2.plot(self.__ramberg_osgoon_strain, self.__stress_array / self.__ramberg_osgoon_strain,
                 label='Secant Modulus')

        ax1.set_xlabel('Strain [mm/mm]')
        ax1.set_ylabel('Stress [MPa]')
        ax1.set_title('Stress Strain Curve')
        ax1.legend()
        ax2.set_xlabel('Strain [mm/mm]')
        ax2.set_ylabel('Modulus [MPa]')
        ax2.set_title('Comparison of Modulus')
        ax2.legend()

        ax1.grid(True)
        ax2.grid(True)

        return fig1, fig2

    @property
    def yield_strength(self):
        return self.__yield_strength

    @property
    def tensile_strength(self):
        return self.__tensile_strength

    @property
    def yield_strain(self):
        return self.__yield_strain

    @property
    def tensile_strain(self):
        return self.__tensile_strain

    @property
    def ramberg_osgoon_values(self):
        return pd.DataFrame(
            {"Stresses": np.round(self.__stress_array, 3),
             "Strains [%]": np.round(self.__ramberg_osgoon_strain * 100, 3),
             "Secant Moduluses": np.round(self.__stress_array / self.__ramberg_osgoon_strain, 0)})

    @property
    def material_id(self):
        return self.__material_id

    @property
    def name(self):
        return self.__name

    @property
    def modulus_of_elasticity(self):
        return self.__modulus_of_elasticity

    @property
    def poissons_ratio(self):
        return self.__poissons_ratio

    @property
    def thermal_conductivity(self):
        return self.__thermal_conductivity

    @property
    def contains(self):
        return self.__contained_materials

    def set_contains(self, contained_materials):
        self.__contained_materials = contained_materials
        return self

    def get_lame_parameters(self, strains=0.001):
        secant_coefficient, _ = self.calculate_engineering_stress_and_strain_multiplayers(strains)
        return self.__modulus_of_elasticity * self.__poissons_ratio / ((1 + self.__poissons_ratio) * (
                1 - 2 * self.__poissons_ratio)) * secant_coefficient, self.__modulus_of_elasticity / (
                       2 * (1 + self.__poissons_ratio)) * secant_coefficient
