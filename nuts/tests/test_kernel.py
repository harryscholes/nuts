import numpy as np
from nose.tools import assert_raises

from ..kernel import _valid_eigenvalues, _normalize
from ..exceptions import InvalidKernel


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
