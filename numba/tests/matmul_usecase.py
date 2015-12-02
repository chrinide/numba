import sys

import numba.unittest_support as unittest


# The "@" operator only compiles on Python 3.5+.
has_matmul = sys.version_info >= (3, 5)

if has_matmul:
    code = """if 1:
    def matmul_usecase(x, y):
        return x @ y

    def imatmul_usecase(x, y):
        x @= y
        return x
    """
    co = compile(code, "<string>", "exec")
    ns = {}
    eval(co, globals(), ns)
    globals().update(ns)
    del code, co, ns

else:
    matmul_usecase = None
    imatmul_usecase = None

needs_matmul = unittest.skipUnless(
    has_matmul, "the matrix multiplication operator needs Python 3.5+")


class DumbMatrix(object):

    def __init__(self, value):
        self.value = value

    def __matmul__(self, other):
        if isinstance(other, DumbMatrix):
            return DumbMatrix(self.value * other.value)
        return NotImplemented

    def __imatmul__(self, other):
        if isinstance(other, DumbMatrix):
            self.value *= other.value
            return self
        return NotImplemented
