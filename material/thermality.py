class Thermality(object):
    def __init__(self, conductivity: float, expansion: float):
        self.__thermal_conductivity = conductivity
        self.__thermal_expansion_coefficent = expansion

    @property
    def thermal_conductivity(self):
        return self.__thermal_conductivity

    @property
    def thermal_expansion_coefficent(self):
        return self.__thermal_expansion_coefficent

    @thermal_conductivity.setter
    def thermal_conductivity(self, conductivity: float):
        self.__thermal_conductivity = conductivity

    @thermal_expansion_coefficent.setter
    def thermal_expansion_coefficent(self, expansion: float):
        self.__thermal_expansion_coefficent = expansion
