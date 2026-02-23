import numpy as np

def element_dof_ids(node_ids: np.ndarray) -> np.ndarray:
    node_ids = np.asarray(node_ids, dtype=np.int64)
    base = 3 * (node_ids - 1)
    return (base[:, None] + np.array([0, 1, 2], dtype=np.int64)[None, :]).ravel()

def bilinear_von_mises_stress(material, von_mises_strain: np.ndarray) -> np.ndarray:
    von_mises_strain = np.asarray(von_mises_strain, dtype=float)
    yield_strain = material.yield_strength / material.youngs_modulus
    elastic_part = np.minimum(von_mises_strain, yield_strain)
    plastic_part = np.maximum(von_mises_strain - yield_strain, 0.0)
    return material.youngs_modulus * elastic_part + material.tangent_modulus * plastic_part

def element_gauss_strain_stress_yield(finite_element, u_element: np.ndarray):
    B_list = finite_element.B_matrices()
    strains = np.vstack([B @ u_element for B in B_list])
    D = finite_element.material.constitutive_matrix
    stress_trial = strains @ D.T
    von_mises_strain = np.array([finite_element.von_mises_strain(e) for e in strains], dtype=float)
    yield_strain = finite_element.material.yield_strength / finite_element.material.youngs_modulus
    yielded = von_mises_strain > yield_strain
    target_von_mises_stress = bilinear_von_mises_stress(finite_element.material, von_mises_strain)

    p = (stress_trial[:, 0] + stress_trial[:, 1] + stress_trial[:, 2]) / 3.0
    dev = stress_trial.copy()
    dev[:, 0] -= p
    dev[:, 1] -= p
    dev[:, 2] -= p

    von_mises_trial = np.array([finite_element.von_mises_stress(s) for s in stress_trial], dtype=float)
    scale = np.ones_like(von_mises_trial)
    scale[yielded] = target_von_mises_stress[yielded] / np.maximum(von_mises_trial[yielded], 1e-30)

    stresses = dev * scale[:, None]
    stresses[:, 0] += p
    stresses[:, 1] += p
    stresses[:, 2] += p
    return strains, stresses, yielded

def model_element_fields(model, u: np.ndarray):
    u = np.asarray(u, dtype=float)
    element_ids = np.array(sorted(model.elements_by_id.keys()), dtype=int)
    n_elem = element_ids.size
    first_element = model.elements_by_id[int(element_ids[0])].finite_element
    n_gp = len(first_element.B_matrices())

    strains = np.zeros((n_elem, n_gp, 6), dtype=float)
    stresses = np.zeros((n_elem, n_gp, 6), dtype=float)
    yielded = np.zeros((n_elem, n_gp), dtype=bool)

    for e_i, eid in enumerate(element_ids):
        element_data = model.elements_by_id[int(eid)]
        dofs = element_dof_ids(element_data.node_ids)
        u_element = u[dofs]
        fe = element_data.finite_element
        eps, sig, yld = element_gauss_strain_stress_yield(fe, u_element)
        strains[e_i] = eps
        stresses[e_i] = sig
        yielded[e_i] = yld

    return element_ids, strains, stresses, yielded
