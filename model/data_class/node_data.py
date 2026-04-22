import numpy as np
from dataclasses import dataclass


@dataclass
class NodeData:
    node_id: int
    coordinates: np.ndarray
    prescribed_displacement: np.ndarray
    external_force: np.ndarray
    
    @property
    def x(self):
        return self.coordinates[0]
    
    @property
    def y(self):
        return self.coordinates[1]
    
    @property
    def z(self):
        return self.coordinates[2]
