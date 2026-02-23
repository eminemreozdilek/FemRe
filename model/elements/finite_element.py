import numpy as np
from abc import ABC, abstractmethod

from model.material import BaseMaterial


class FiniteElement(ABC):
    """
    Base class for 3D small-strain finite elements.

    It supports both:
        - linear analysis via stiffness_matrix(), using material.constitutive_matrix
        - nonlinear analysis via tangent_stiffness_and_internal_force(), using
          material.initial_state() and material.constitutive_response().
    """

    def __init__(self, nodes: np.ndarray, material: BaseMaterial):
        self.nodes = np.array(nodes, dtype=float)
        self.material = material

    # ------------------------------------------------------------------
    # Linear API (unchanged)
    # ------------------------------------------------------------------
    @abstractmethod
    def stiffness_matrix(self):
        """Compute the (constant) element stiffness matrix for linear analysis."""
        pass

    @abstractmethod
    def compute_strain(self, displacements: np.ndarray, **kwargs):
        """Compute the strain vector for the element at a given point."""
        pass

    @abstractmethod
    def compute_stress(self, displacements: np.ndarray, **kwargs):
        """Compute the stress vector for the element at a given point."""
        pass

    @abstractmethod
    def compute_strain_energy(self, displacements: np.ndarray):
        """Compute the strain energy stored in the element."""
        pass

    @staticmethod
    @abstractmethod
    def von_mises_stress(stress: np.ndarray):
        """Compute the von Mises equivalent stress."""
        pass

    @staticmethod
    @abstractmethod
    def von_mises_strain(strain: np.ndarray):
        """Compute the von Mises equivalent strain."""
        pass

    # ------------------------------------------------------------------
    # Nonlinear API (new)
    # ------------------------------------------------------------------
    @abstractmethod
    def B_matrices(self):
        """
        Return a list of B matrices, one for each integration point.
        Each B has shape (6, n_dof_element).
        """
        pass

    @abstractmethod
    def integration_weights(self) -> np.ndarray:
        """
        Return a 1D array of 'dV' weights (Jacobian * Gauss weight)
        for each integration point, same length as B_matrices().
        """
        pass

    def num_integration_points(self) -> int:
        """Number of integration points for this element."""
        return len(self.B_matrices())

    def tangent_stiffness_and_internal_force(
        self,
        u_e: np.ndarray,
        state_list: list | None,
    ):
        """
        Generic tangent stiffness + internal force for small-strain material
        nonlinearity.

        Parameters
        ----------
        u_e : (n_dof_element,) array
            Element nodal displacement vector.
        state_list : list of dict or None
            State variables per integration point. If None or length mismatch,
            they are (re)initialized using material.initial_state().

        Returns
        -------
        Ke : (n_dof_element, n_dof_element) array
        f_int : (n_dof_element,) array
        new_states : list of dict
        """
        B_list = self.B_matrices()
        w = self.integration_weights()
        n_ip = len(B_list)

        if state_list is None or len(state_list) != n_ip:
            state_list = [self.material.initial_state() for _ in range(n_ip)]

        ndof_e = u_e.size
        Ke = np.zeros((ndof_e, ndof_e))
        f_int = np.zeros(ndof_e)
        new_states = []

        for i in range(n_ip):
            B = B_list[i]
            eps = B @ u_e
            state_i = state_list[i]

            # Uses your new nonlinear material interface
            sigma, D_t, new_state_i = self.material.constitutive_response(eps, state_i)
            new_states.append(new_state_i)

            dV = w[i]
            Ke += B.T @ D_t @ B * dV
            f_int += B.T @ sigma * dV

        return Ke, f_int, new_states
