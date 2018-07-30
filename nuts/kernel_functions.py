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


def RWR(G, a=0.01):
    """
    Random walk with restart similarity matrix function (Pan, 2006)

    NB does not produce a kernel as the matrix is not symmetric

    # Arguments
        a: float, probability of restart
    """
    A = nx.adjacency_matrix(G, nodelist=sorted(G.nodes)).toarray() \
        .astype('float')
    D = np.diag(A.sum(axis=0))
    K = D @ np.linalg.inv(D - a * A)
    return K
