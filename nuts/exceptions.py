""" Custom exceptions. """

class NutsException(Exception):
    """ Base class for exceptions in Nuts. """


class InvalidKernel(NutsException):
    """ Exception for invalid kernels. """
