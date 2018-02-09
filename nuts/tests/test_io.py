import numpy as np
import tables

from ..io import write_to_hdf5, load_from_hdf5


def test_write_to_hdf5():
    target = np.arange(4)

    # save a kernel matrix
    fileobj = tables.open_file("test", "w", driver="H5FD_CORE",
                               driver_core_backing_store=0)
    assert isinstance(fileobj, tables.file.File)
    fileobj = write_to_hdf5(target, fileobj)
    loaded = getattr(fileobj.root, 'kernel').read()
    assert (target == loaded).all()
    fileobj.close()

    # save with compression
    fileobj = tables.open_file("test", "w", driver="H5FD_CORE",
                               driver_core_backing_store=0)
    assert isinstance(fileobj, tables.file.File)
    fileobj = write_to_hdf5(target, fileobj, compression=True)
    loaded = getattr(fileobj.root, 'kernel').read()
    assert (target == loaded).all()
    fileobj.close()

    # save with mapping dictionary
    fileobj = tables.open_file("test", "w", driver="H5FD_CORE",
                               driver_core_backing_store=0)
    assert isinstance(fileobj, tables.file.File)
    target = {"a": 0, "b": 1}
    fileobj = write_to_hdf5(np.arange(4), fileobj, mapping=target)
    loaded = getattr(fileobj.root, 'mapping').read()
    loaded = {k.decode(): int(v.decode()) for (k, v) in loaded}
    assert target == loaded
    fileobj.close()


def test_load_from_hdf5():
    target = np.arange(4)

    # load a kernel matrix
    fileobj = tables.open_file("test", "w", driver="H5FD_CORE",
                               driver_core_backing_store=0)
    assert isinstance(fileobj, tables.file.File)
    fileobj = write_to_hdf5(target, fileobj)
    loaded = load_from_hdf5(fileobj)
    assert (target == loaded).all()

    # load with mapping dictionary
    fileobj = tables.open_file("test", "w", driver="H5FD_CORE",
                               driver_core_backing_store=0)
    assert isinstance(fileobj, tables.file.File)
    target = {"a": 0, "b": 1}
    fileobj = write_to_hdf5(np.arange(4), fileobj, mapping=target)
    kernel, loaded = load_from_hdf5(fileobj)
    loaded = {k.decode(): int(v.decode()) for (k, v) in loaded}
    assert target == loaded
    fileobj.close()
