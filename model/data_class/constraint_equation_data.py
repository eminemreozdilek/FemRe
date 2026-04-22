from dataclasses import dataclass

import numpy as np


@dataclass
class ConstraintEquationData:
    constraint_eq_id: int
    dof_indices: np.ndarray
    coefficients: np.ndarray
    equation_constant: float
