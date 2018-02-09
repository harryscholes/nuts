import numpy as np
import networkx as nx
from nose.tools import assert_raises

from ..kernel import _valid_eigenvalues, _normalize, Kernel
from ..exceptions import InvalidKernel


class test_Kernel():
    def __init__(self):
        G = nx.path_graph(range(2))
        k = Kernel(G)
        self.k = k
        self.k.calculate("CT")

    def test_valid(self):
        # all positive
        self.k.eigenvalues = [1, 2]
        assert self.k.valid() is True

        # all negative
        self.k.eigenvalues = [-1, -2]
        assert_raises(InvalidKernel, self.k.valid)

        # mixture of positive and negative
        self.k.eigenvalues = [1, -2]
        assert_raises(InvalidKernel, self.k.valid)

        # negative value equal to the default tolerance
        self.k.eigenvalues = [1, -np.finfo(float).eps]
        assert_raises(InvalidKernel, self.k.valid)

        # custom tolerance values
        self.k.eigenvalues = [1, 2]
        assert self.k.valid(tolerance=0.1)
        self.k.eigenvalues = [-0.3, -0.1]
        assert_raises(InvalidKernel, self.k.valid, tolerance=0.2)


def test_valid():
    # all positive
    assert _valid_eigenvalues([1, 2]) is True

    # all negative
    assert_raises(InvalidKernel, _valid_eigenvalues, [-1, -2])

    # mixture of positive and negative
    assert_raises(InvalidKernel, _valid_eigenvalues, [1, -2])

    # negative value equal to the default tolerance
    assert_raises(InvalidKernel, _valid_eigenvalues, [1, -np.finfo(float).eps])

    # custom tolerance values
    assert _valid_eigenvalues([1, 2], tolerance=0.1) is True
    assert_raises(InvalidKernel, _valid_eigenvalues, [-0.3, -0.1], tolerance=0.2)


def test_normalize():
    kernel = np.array([[1, 3], [3, 4]])
    calculated = _normalize(kernel)
    target = np.array([[1., 1.5], [1.5, 1.]])

    # check shape of the matrix
    assert calculated.shape == calculated.shape

    # check diagonal values are all 1
    assert np.all(np.diag(calculated) == 1.)

    # check calculated == target
    assert (calculated == target).all()
