""" Calculate kernels of graphs. """

import numpy as np

from .kernel_functions import CT
from .exceptions import InvalidKernel
from .io import write_to_hdf5

__all__ = ["Kernel"]


class Kernel(object):
    """
    Calculate kernels of graphs.

    Args:
        G (nx.Graph): graph with which to calculate the kernel
    """
    def __init__(self, G):
        self.G = G

    def calculate(self, kernel_function):
        """
        Calculate the kernel of `G` using `kernel_function`.

        Args:
            kernel_function (str): name of the required kernel function
        """

        available_kernels = {
            "CT": CT,
        }

        self.kernel_function = available_kernels[kernel_function]

        kernel = self.kernel_function(self.G)
        eigenvalues = np.linalg.eigvals(kernel)
        mapping = {node: index for node, index in
                   zip(self.G.nodes, range(len(self.G.nodes)))}

        self.kernel = kernel
        self.eigenvalues = eigenvalues
        self.mapping = mapping

    def valid(self, tolerance=np.finfo(float).eps):
        """
        Checks whether the kernel is valid.

        A kernel is valid if it is a square, positive semi-definite matrix.

        Args:
            tolerance (float): machine epsilon tolerance
        """

        assert self.kernel.shape[0] == self.kernel.shape[1], \
            "Kernel is not square."

        self.tolerance = tolerance
        self.is_valid = False
        
        if _valid_eigenvalues(self.eigenvalues, self.tolerance) is True:
            self.is_valid = True
            return True

    def make_valid(self):
        """ Make the matrix a valid kernel by shifting its eigenvalues. """

        assert self.is_valid is False

        smallest_eigenvalue = np.real(self.eigenvalues).min()
        np.fill_diagonal(self.kernel,
                         self.kernel.diagonal() + abs(smallest_eigenvalue))

        self.eigenvalues = np.linalg.eigvals(self.kernel)

        self.valid()
        assert self.is_valid is True

    def normalize(self, overwrite=True):
        """
        Normalize the kernel by calculating the cosine of the matrix.

        Args:
            overwrite (bool): overwrite the kernel attribute with the
                              normalized matrix
        """

        if overwrite:
            self.kernel = _normalize(self.kernel)
        else:
            self.normalized_kernel = _normalize(self.kernel)

    def save(self, filename, save_mapping=True, compression=False):
        """
        Save the kernel to HDF5.

        Args:
            save_mapping (bool): include the node to matrix index mapping
            compression (bool): compress the HDF5 file
        """
        write_to_hdf5(kernel=self.kernel,
                      filepath=filename,
                      mapping=self.mapping if save_mapping is True else None,
                      compression=compression,
                      )


def _valid_eigenvalues(eigenvalues, tolerance=np.finfo(float).eps):
    """
    Check the validity of the kernel eigenvalues.

    Args:
        eigenvalues (list): kernel eigenvalues
        tolerance (float): machine epsilon tolerance
    """
    if np.all(np.real(eigenvalues) > -tolerance):
        return True
    else:
        raise InvalidKernel("Kernel is not positive semi-definite.")


def _normalize(kernel):
    """
    Normalize the kernel using the cosine of the matrix.

    Args:
        kernel (np.ndarray): kernel matrix
    """
    D = np.diag(1 / np.sqrt(np.diag(kernel)))
    normalized_kernel = D @ kernel @ D
    return normalized_kernel
