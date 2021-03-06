""" Calculate kernels of graphs. """

import numpy as np
import networkx as nx
import tables
import os

from .kernel_functions import CT, RWR
from .exceptions import InvalidKernel
from .io import write_to_hdf5, read_from_hdf5

__all__ = ["Kernel"]


class Kernel(object):
    """
    Calculate kernels of graphs.
    """
    def __init__(self, **kwargs):
        pass

    def graph(self, G):
        """
        Load a graph into nuts.

        Args:
            G (nx.Graph): graph with which to calculate the kernel
        """
        assert isinstance(G, nx.Graph), "`G` must be nx.Graph"
        self.G = G

    def calculate(self, kernel_function):
        """
        Calculate the kernel of `G` using `kernel_function`.

        Args:
            kernel_function (str): name of the required kernel function
        """

        available_kernels = {
            "CT": CT,
            "RWR": RWR,
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

        try:
            if _valid_eigenvalues(self.eigenvalues, self.tolerance) is True:
                self.is_valid = True
                return True

        except InvalidKernel:
            return False

    def make_valid(self):
        """ Make the matrix a valid kernel by shifting its eigenvalues. """

        assert not self.is_valid

        smallest_eigenvalue = np.real(self.eigenvalues).min()
        np.fill_diagonal(self.kernel,
                         self.kernel.diagonal() + abs(smallest_eigenvalue))

        self.eigenvalues = np.linalg.eigvals(self.kernel)

        self.valid()
        assert self.is_valid

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

    def write(self, filename, save_mapping=True, compression=False):
        """
        Save the kernel to HDF5.

        Args:
            save_mapping (bool): include the node to matrix index mapping
            compression (bool): compress the HDF5 file
        """
        with tables.open_file(filename, "a") as fileobj:

            write_to_hdf5(kernel=self.kernel,
                          fileobj=fileobj,
                          mapping=self.mapping if save_mapping is True else None,
                          compression=compression,
                          )

    def read(self, filepath):
        """
        Read a kernel into nuts.

        Args:
            filepath (str): filepath to kernel HDF5 file
        """
        assert os.path.isfile(filepath), \
            "Kernel HDF5 file does not exist at `filepath`"

        with tables.open_file(filepath, "r") as fileobj:
            contents = read_from_hdf5(fileobj)

        self.kernel = contents[0]

        if len(contents) == 2:
            self.mapping = contents[1]

        return contents


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
