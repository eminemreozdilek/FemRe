class Strut(object):
    def __init__(self, strut_id, start_node, end_node, material, radius):
        self.__strut_id = strut_id
        self.__start_node = start_node
        self.__end_node = end_node
        self.__material = material
        self.__radius = radius

    @property
    def strut_id(self):
        return self.__strut_id

    @property
    def start_node(self):
        return self.__start_node

    @property
    def end_node(self):
        return self.__end_node

    @property
    def material(self):
        return self.__material

    @property
    def radius(self):
        return self.__radius
