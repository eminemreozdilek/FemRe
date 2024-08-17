import pandas as pd

from preprocessor.material.isotropic_elasticity import IsotropicElasticity
from preprocessor.material.orthotropic_elasticity import OrthotropicElasticity


class Material(object):
    def __init__(self, material_name: str = "Material"):
        self.__material_name = material_name

        self.__density = 1.0
        self.__volume_fraction = 1.0
        self.__core_material_mixture = {material_name: 1.0}

        self.__elasticity_model = None
        self.__hardening_model = None

    def define_isotropic_elasticity(self,
                                    youngs_modulus: float,
                                    poissons_ratio: float):
        self.__elasticity_model = IsotropicElasticity(youngs_modulus,
                                                      poissons_ratio)

    def define_orthotropic_model(self,
                                 youngs_modulus_xx,
                                 youngs_modulus_yy,
                                 youngs_modulus_zz,
                                 poisson_ratio_xy,
                                 poisson_ratio_yz,
                                 poisson_ratio_xz):
        self.__elasticity_model = OrthotropicElasticity(youngs_modulus_xx,
                                                        youngs_modulus_yy,
                                                        youngs_modulus_zz,
                                                        poisson_ratio_xy,
                                                        poisson_ratio_yz,
                                                        poisson_ratio_xz)

    def define_hardening_model(self):
        pass
