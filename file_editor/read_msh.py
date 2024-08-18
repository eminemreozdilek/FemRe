import pandas as pd
import applications.application_static.model_storage as st


def read_msh(filename: str):
    reader = ""
    nodes = []
    tetrahedral_elements = []
    hexagonal_elements = []
    data_storage = st.Storage()
    t_count = 0

    with open(filename, "r") as f:
        for line in f.readlines():
            if line == "$Nodes\n":
                reader = "node"
            elif line == "$Elements\n":
                reader = "element"

            if reader == "node":
                nodal_data = line.split(" ")
                if len(nodal_data) == 4:
                    data = [int(nodal_data[0]), float(nodal_data[1]), float(nodal_data[2]), float(nodal_data[3])]
                    nodes.append(data)
            elif reader == "element":
                element_data = line.split(" ")
                try:
                    if element_data[1] == "4":
                        data = []

                        if len(element_data) == 9:
                            for i in range(9):
                                data.append(int(element_data[i]))
                            tetrahedral_elements.append(data)
                    if element_data[1] == "5":
                        data = []

                        if len(element_data) == 12:
                            for i in range(9):
                                data.append(int(element_data[i]))
                            hexagonal_elements.append(data)
                except:
                    pass

    nodes = pd.DataFrame(nodes, columns=['NodeID',
                                         'X',
                                         'Y',
                                         'Z'])

    tetrahedral_elements = pd.DataFrame(tetrahedral_elements, columns=['ElementID',
                                                                       'ElementType',
                                                                       'NumberOfTag',
                                                                       'PhysicalEntity',
                                                                       'ElementaryEntity',
                                                                       'Node1',
                                                                       'Node2',
                                                                       'Node3',
                                                                       'Node4'])

    hexagonal_elements = pd.DataFrame(hexagonal_elements, columns=['ElementID',
                                                                   'ElementType',
                                                                   'NumberOfTag',
                                                                   'PhysicalEntity',
                                                                   'ElementaryEntity',
                                                                   'Node1',
                                                                   'Node2',
                                                                   'Node3',
                                                                   'Node4',
                                                                   'Node5',
                                                                   'Node6',
                                                                   'Node7',
                                                                   'Node8'])

    data_storage.update_node(nodes)
    data_storage.update_tetrahedral_element(tetrahedral_elements)
    data_storage.update_hexagonal_element(hexagonal_elements)

    return data_storage
