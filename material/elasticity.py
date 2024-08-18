import pandas as pd
import numpy as np


class Elasticity(object):
    def __init__(self):
        self.__data = pd.DataFrame({"YoungsModulus": [],
                                    "ShearModulus": [],
                                    "BulkModulus": [],
                                    "PoissonsRatio": []})
        self.__material_matrix = np.ones((6, 6))

    def create_from_e_nu(self, youngs_modulus, poissons_ratio):
        shear_modulus = youngs_modulus / 2 / (1 + poissons_ratio)
        bulk_modulus = youngs_modulus / 3 / (1 - 2 * poissons_ratio)
        lame_modulus = youngs_modulus * poissons_ratio / (1 + poissons_ratio) / (1 - 2 * poissons_ratio)

        self.__material_matrix = (lame_modulus * np.array([[1, 1, 1, 0, 0, 0],
                                                           [1, 1, 1, 0, 0, 0],
                                                           [1, 1, 1, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0],
                                                           [0, 0, 0, 0, 0, 0], ])
                                  + shear_modulus * np.array([[2, 0, 0, 0, 0, 0],
                                                              [0, 2, 0, 0, 0, 0],
                                                              [0, 0, 2, 0, 0, 0],
                                                              [0, 0, 0, 1, 0, 0],
                                                              [0, 0, 0, 0, 1, 0],
                                                              [0, 0, 0, 0, 0, 1], ]))

        self.__data = pd.DataFrame({"YoungsModulus": [youngs_modulus],
                                    "ShearModulus": [shear_modulus],
                                    "BulkModulus": [bulk_modulus],
                                    "PoissonsRatio": [poissons_ratio]})

    @property
    def material_matrix(self):
        return self.__material_matrix

    @property
    def data(self):
        return self.__data
