import numpy as np


class IsotropicElasticity(object):
    def __init__(self, youngs_modulus: float, poissons_ratio: float):
        self.__youngs_modulus = youngs_modulus
        self.__poissons_ratio = poissons_ratio

        self.__shear_modulus = youngs_modulus / 2 / (1 + poissons_ratio)
        self.__bulk_modulus = youngs_modulus / 3 / (1 - 2 * poissons_ratio)
        self.__lame_modulus = youngs_modulus * poissons_ratio / (1 + poissons_ratio) / (1 - 2 * poissons_ratio)

        self.__elasticity_matrix = (self.__lame_modulus
                                    * np.array([[1, 1, 1, 0, 0, 0],
                                                [1, 1, 1, 0, 0, 0],
                                                [1, 1, 1, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0],
                                                [0, 0, 0, 0, 0, 0], ])
                                    + self.__shear_modulus
                                    * np.array([[2, 0, 0, 0, 0, 0],
                                                [0, 2, 0, 0, 0, 0],
                                                [0, 0, 2, 0, 0, 0],
                                                [0, 0, 0, 1, 0, 0],
                                                [0, 0, 0, 0, 1, 0],
                                                [0, 0, 0, 0, 0, 1], ]))

    @property
    def youngs_modulus(self):
        return self.__youngs_modulus

    @property
    def poissons_ratio(self):
        return self.__poissons_ratio

    @property
    def shear_modulus(self):
        return self.__shear_modulus

    @property
    def bulk_modulus(self):
        return self.__bulk_modulus

    @property
    def lame_modulus(self):
        return self.__lame_modulus

    @property
    def elasticity_matrix(self):
        return self.__elasticity_matrix
