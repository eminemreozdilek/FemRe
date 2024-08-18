import pandas as pd
import numpy as np


class ElementBrickEight(object):
    def __init__(self):
        self.__data = pd.DataFrame({'ElementID': [],
                                    'ElementType': [],
                                    'NumberOfTag': [],
                                    'PhysicalEntity': [],
                                    'ElementaryEntity': [],
                                    'Node1': [],
                                    'Node2': [],
                                    'Node3': [],
                                    'Node4': [],
                                    'Node5': [],
                                    'Node6': [],
                                    'Node7': [],
                                    'Node8': [],
                                    "Material": [],
                                    "BoundaryForceX1": [],
                                    "BoundaryForceX2": [],
                                    "BoundaryForceX3": [],
                                    "BoundaryForceX4": [],
                                    "BoundaryForceX5": [],
                                    "BoundaryForceX6": [],
                                    "BoundaryForceY1": [],
                                    "BoundaryForceY2": [],
                                    "BoundaryForceY3": [],
                                    "BoundaryForceY4": [],
                                    "BoundaryForceY5": [],
                                    "BoundaryForceY6": [],
                                    "BoundaryForceZ1": [],
                                    "BoundaryForceZ2": [],
                                    "BoundaryForceZ3": [],
                                    "BoundaryForceZ4": [],
                                    "BoundaryForceZ5": [],
                                    "BoundaryForceZ6": [],
                                    "VolumeForceX": [],
                                    "VolumeForceY": [],
                                    "VolumeForceZ": [],
                                    "TemperatureChange": [],
                                    "StressX": [],
                                    "StressY": [],
                                    "StressZ": [],
                                    "ShearXY": [],
                                    "ShearYZ": [],
                                    "ShearXZ": [],
                                    "StrainX": [],
                                    "StrainY": [],
                                    "StrainZ": [],
                                    "StrainXY": [],
                                    "StrainYZ": [],
                                    "StrainXZ": [],
                                    "VonMissesStress": [],
                                    "VonMissesStrain": [],
                                    "VonMissesEnergy": []
                                    })

    @property
    def data(self):
        return self.__data

    def set_data(self, element_dataframe: pd.DataFrame):
        self.__data = element_dataframe


class ElementTetraFour(object):
    def __init__(self):
        self.__data = pd.DataFrame({'ElementID': [],
                                    'ElementType': [],
                                    'NumberOfTag': [],
                                    'PhysicalEntity': [],
                                    'ElementaryEntity': [],
                                    'Node1': [],
                                    'Node2': [],
                                    'Node3': [],
                                    'Node4': [],
                                    "Material": [],
                                    "BoundaryForceX1": [],
                                    "BoundaryForceX2": [],
                                    "BoundaryForceX3": [],
                                    "BoundaryForceX4": [],
                                    "BoundaryForceY1": [],
                                    "BoundaryForceY2": [],
                                    "BoundaryForceY3": [],
                                    "BoundaryForceY4": [],
                                    "BoundaryForceZ1": [],
                                    "BoundaryForceZ2": [],
                                    "BoundaryForceZ3": [],
                                    "BoundaryForceZ4": [],
                                    "VolumeForceX": [],
                                    "VolumeForceY": [],
                                    "VolumeForceZ": [],
                                    "TemperatureChange": [],
                                    "StressX": [],
                                    "StressY": [],
                                    "StressZ": [],
                                    "ShearXY": [],
                                    "ShearYZ": [],
                                    "ShearXZ": [],
                                    "StrainX": [],
                                    "StrainY": [],
                                    "StrainZ": [],
                                    "StrainXY": [],
                                    "StrainYZ": [],
                                    "StrainXZ": [],
                                    "VonMissesStress": [],
                                    "VonMissesStrain": [],
                                    "VonMissesEnergy": [],
                                    })

    @property
    def data(self):
        return self.__data

    def set_data(self, element_dataframe: pd.DataFrame):
        self.__data = element_dataframe
