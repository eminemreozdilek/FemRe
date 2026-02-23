import numpy as np
from dataclasses import dataclass
from model.elements.finite_element import FiniteElement

@dataclass
class ElementData:
    element_id: int
    component_id: int
    node_ids: np.ndarray
    finite_element: FiniteElement
    spatial_dimension: int
