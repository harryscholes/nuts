""" Read and write kernels. """

import numpy as np
import tables

__all__ = ["write_to_hdf5", "load_from_hdf5"]


def write_to_hdf5(kernel, filepath, mapping=None, compression=False):
    assert isinstance(kernel, np.ndarray), 'Kernel must be an `np.array`'

    filters = tables.Filters(complib='zlib', complevel=5) \
        if compression else None

    with tables.open_file(filepath, 'a', filters=filters) as f:

        attributes = ['kernel', 'mapping']

        for attribute in attributes:
            try:
                n = getattr(f.root, attribute)
                n._f_remove()
            except AttributeError:
                pass

        f.create_array(f.root, 'kernel', kernel)

        if mapping:
            f.create_array(f.root, 'mapping', np.array(list(mapping.items())))


def load_from_hdf5(filepath):
    with tables.open_file(filepath) as f:
        kernel = getattr(f.root, 'kernel').read()

        if hasattr(f.root, 'mapping'):
            mapping_array = getattr(f.root, 'mapping').read()
            mapping = {protein.decode(): int(index.decode())
                       for (protein, index) in mapping_array}
            return kernel, mapping

        else:
            return kernel
