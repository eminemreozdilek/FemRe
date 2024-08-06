from preprocessor.models import (nodes, elements)
from preprocessor.properties import material


def read_input_file(file_name: str, standart_radius=None):
    input_file = open(file_name, "r")
    lines = input_file.readlines()

    node_lookup_table = {}
    strut_lookup_table = {}
    material_lookup_table = {}

    data = [x.split() for x in lines]

    for line in data:
        if len(line) > 0:
            if (line[0]).lower() == "node":
                node_lookup_table[int(line[1])] = nodes.Node(int(line[1]), float(line[2]), float(line[3]),
                                                            float(line[4]))
            if (line[0]).lower() == "mat":
                if len(line) == 5:
                    new_material = material.Material(int(line[1]), float(line[2]), float(line[3]), float(line[4]))
                else:
                    new_material = material.NonLinearMaterial(int(line[1]), float(line[2]), float(line[3]),
                                                              float(line[4]),
                                                              float(line[5]), float(line[6]), float(line[7]),
                                                              float(line[8]))
                material_lookup_table[new_material.contains] = new_material
    for line in data:
        if len(line) > 0:
            if (line[0]).lower() == "strut":
                if standart_radius is None:
                    strut_lookup_table[int(line[1])] = elements.Strut(int(line[1]),
                                                                   node_lookup_table[int(line[2])],
                                                                   node_lookup_table[int(line[3])],
                                                                   material_lookup_table[
                                                                       tuple([int(line[4])])],
                                                                   float(line[5]))
                else:
                    strut_lookup_table[int(line[1])] = elements.Strut(int(line[1]),
                                                                   node_lookup_table[int(line[2])],
                                                                   node_lookup_table[int(line[3])],
                                                                   material_lookup_table[
                                                                       tuple([int(line[4])])],
                                                                   standart_radius)

    input_file.close()

    return node_lookup_table, strut_lookup_table, material_lookup_table
