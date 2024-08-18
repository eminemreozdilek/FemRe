class Node:
    def __init__(node, id, X, Y, Z):
        node.id = id
        node.X, node.Y, node.Z = X, Y, Z  # Koordinatlar
        node.rest = [0, 0, 0]  # Mesnet Koşulu [0: serbest, 1:tutulu]
        node.force = [0, 0, 0]  # Tekil-Yük [Px, Py, Pz]
        node.disp = [0, 0, 0]  # Mesnet Çökmesi [delta_x, delta_y, delta_z]
        node.code = [-1, -1, -1]  # Serbestlikler (Kod) [dx, dy, dz]
        node.values = []

    def mean_value(node):
        return sum(node.values) / len(node.values)

    def ExternalForceVectorToContribute(node):
        return node.force

    def save_node_to_dataframe(self, node_storage):
        node_storage.loc[self.id] = {"NodeID": self.id,
                                     "Node": self, }
        return node_storage
