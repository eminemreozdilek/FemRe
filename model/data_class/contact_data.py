import numpy as np
from dataclasses import dataclass

@dataclass
class ContactData:
    parent_node_id_array: np.ndarray
    child_node_id_array: np.ndarray
    contact_constraint_array: np.ndarray
