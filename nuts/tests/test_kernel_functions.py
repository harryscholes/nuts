import numpy as np
import networkx as nx

from ..kernel_functions import CT


def test_CT():
    G = nx.path_graph(range(2))
    kernel = CT(G)
    target = np.array([[0.25, -0.25], [-0.25, 0.25]])
    assert np.allclose(kernel, target)
