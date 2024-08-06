import numpy as np
import scipy.sparse as ss


def take_sparse(k, c):
    chooser = (np.isin(k.nonzero()[0], np.array(c)) * 1) * (np.isin(k.nonzero()[1], np.array(c)) * 1)

    row_indexer = ss.csr_matrix(chooser * k.nonzero()[0]).data
    col_indexer = ss.csr_matrix(chooser * k.nonzero()[1]).data
    k_data = np.ndarray.tolist(k[row_indexer, col_indexer])
    t = dict(zip(c, range(len(c))))

    row_placer = list(map(t.get, row_indexer))
    col_placer = list(map(t.get, col_indexer))

    return ss.csr_matrix((k_data[0], (row_placer, col_placer)))
