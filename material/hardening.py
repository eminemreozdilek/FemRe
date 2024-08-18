import pandas as pd
import numpy as np


class Hardening:
    def __init__(self, material_properties: pd.DataFrame, hardening_type: str):
        self.__material_properties = material_properties
        self.__hardening_type = hardening_type

        if self.__hardening_type == "Bilinear":
            self.__calculate_bilinear()
        elif self.__hardening_type == "RambergOsgoon":
            self.__calculate_ramberg_osgoon()

    def __calculate_ramberg_osgoon(self):
        n = (np.log(
            (self.__material_properties["UltimateStrain"] - self.__material_properties["UltimateStress"] /
             self.__material_properties["YoungsModulus"]) / self.__material_properties["YieldStrain"])
             / np.log(self.__material_properties["UltimateStress"] / self.__material_properties["YieldStress"]))

        self.__stress_array = np.linspace(0, self.__material_properties["UltimateStress"], 1000)
        self.__strain__array = (self.__stress_array / self.__material_properties["YoungsModulus"]) + 0.002 * (
                self.__stress_array / self.__material_properties["YieldStress"]) ** n

        self.__secand_modulus_coefficent = self.__stress_array / self.__strain__array / self.__material_properties[
            "YoungsModulus"]

    def __calculate_bilinear(self):
        self.__stress_array = np.array(
            [0, self.__material_properties["YieldStress"], self.__material_properties["UltimateStress"]])
        self.__strain__array = np.array(
            [0, self.__material_properties["YieldStrain"], self.__material_properties["UltimateStrain"]])

        self.__secand_modulus_coefficent = self.__stress_array / self.__strain__array / self.__material_properties[
            "YoungsModulus"]



