class SingletonMeta(type):
    instance = None

    def __call__(cls):
        if SingletonMeta.instance is None:
            SingletonMeta.instance = super().__call__()
        return SingletonMeta.instance


class NilType(metaclass=SingletonMeta):
    """
    A None-like object that safely interacts with anything.

    Implements all methods which may be invoked by Ast.
    """

    # Logical

    def __not__(self):
        return self

    # Mathematical

    def __pow__(self, other):
        return self

    def __rpow__(self, other):
        return self

    def __add__(self, other):
        return self

    def __radd__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __rsub__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __rmul__(self, other):
        return self

    def __truediv__(self, other):
        return self

    def __rtruediv__(self, other):
        return self

    # Comparisons

    def __lt__(self, other):
        return self

    def __le__(self, other):
        return self

    def __eq__(self, other):
        return self

    def __ne__(self, other):
        return self

    def __ge__(self, other):
        return self

    def __gt__(self, other):
        return self

    # Mapping

    def __getitem__(self, key, **kwargs):
        if "default" in kwargs:
            return kwargs["default"]

        return self


Nil = NilType()
