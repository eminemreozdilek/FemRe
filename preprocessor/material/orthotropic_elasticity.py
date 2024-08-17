import numpy as np


class OrthotropicElasticity(object):
    def __init__(self,
                 youngs_modulus_xx: float,
                 youngs_modulus_yy: float,
                 youngs_modulus_zz: float,
                 poissons_ratio_xy: float,
                 poissons_ratio_yz: float,
                 poissons_ratio_xz: float):
        self.__youngs_modulus_xx = youngs_modulus_xx
        self.__youngs_modulus_yy = youngs_modulus_yy
        self.__youngs_modulus_zz = youngs_modulus_zz
        self.__youngs_modulus = (self.__youngs_modulus_xx + self.__youngs_modulus_yy + self.__youngs_modulus_zz) / 3

        self.__poissons_ratio_xy = poissons_ratio_xy
        self.__poissons_ratio_yz = poissons_ratio_yz
        self.__poissons_ratio_xz = poissons_ratio_xz
        self.__poissons_ratio = (self.__poissons_ratio_xy + self.__poissons_ratio_yz + self.__poissons_ratio_xz) / 3

        self.__shear_modulus_xy = youngs_modulus_xx * youngs_modulus_yy / (
                youngs_modulus_xx + youngs_modulus_yy + 2 * youngs_modulus_yy * poissons_ratio_xy)
        self.__shear_modulus_yz = youngs_modulus_yy * youngs_modulus_zz / (
                youngs_modulus_yy + youngs_modulus_zz + 2 * youngs_modulus_zz * poissons_ratio_yz)
        self.__shear_modulus_xz = youngs_modulus_xx * youngs_modulus_zz / (
                youngs_modulus_xx + youngs_modulus_zz + 2 * youngs_modulus_zz * poissons_ratio_xz)
        self.__shear_modulus = (self.__shear_modulus_xy + self.__shear_modulus_yz + self.__shear_modulus_xz) / 3

        self.__bulk_modulus = (youngs_modulus_xx * youngs_modulus_yy * youngs_modulus_zz) ** (1 / 3) / 3 / (
                    1 - 2 * (poissons_ratio_xy * poissons_ratio_yz * poissons_ratio_xz) ** (1 / 3))
        self.__lame_modulus = self.__youngs_modulus * self.__poissons_ratio / (1 + self.__poissons_ratio) / (1 - 2 * self.__poissons_ratio)

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
