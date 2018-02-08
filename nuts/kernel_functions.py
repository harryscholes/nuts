""" Kernel functions. """

import numpy as np
import networkx as nx


def CT(G):
    """
    Commute time kernel function.

    Ref: Fouss (2007)
    """
    L = nx.laplacian_matrix(G, nodelist=sorted(G.nodes)).toarray() \
        .astype('float')
    K = np.linalg.pinv(L)
    return K
