from nose.tools import raises

from ..exceptions import NutsException, InvalidKernel


@raises(NutsException)
def test_raises_NutsException():
    raise NutsException


@raises(InvalidKernel)
def test_raises_InvalidKernel():
    raise InvalidKernel
