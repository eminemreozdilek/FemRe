import numpy as np
from dataclasses import dataclass


@dataclass
class NodeData:
    node_id: int
    coordinates: np.ndarray
    prescribed_displacement: np.ndarray
    external_force: np.ndarray
