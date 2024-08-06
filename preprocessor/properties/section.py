import numpy as np


class Section:
    def __init__(self, section_name: str, area: float, moment_of_inertia: np.ndarray):
        self.__section_name = section_name
        self.__area = area
        self.__moment_of_inertia = moment_of_inertia

    def __str__(self):
        return "Section - " + self.__section_name

    def __repr__(self):
        return "Section - " + self.__section_name

    def save_section_to_dataframe(self, section_storage):
        section_storage.loc[self.__section_name] = {"SectionName": self.__section_name,
                                                    "Section": self}
        return section_storage

    @property
    def area(self):
        return self.__area

    @property
    def moment_of_inertia(self):
        return self.__moment_of_inertia

    @property
    def section_name(self):
        return self.__section_name

    @property
    def i_xx(self):
        return self.__moment_of_inertia[0, 0]

    @property
    def i_yy(self):
        return self.__moment_of_inertia[1, 1]

    @property
    def i_zz(self):
        return self.__moment_of_inertia[2, 2]

    @property
    def i_yz(self):
        return self.__moment_of_inertia[1, 2]
