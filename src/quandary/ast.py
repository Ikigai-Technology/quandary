import operator

from .exceptions import ExecutionError
from .nil import Nil


def trap(func):
    """Decorator for all eval() functions to raise ExecutionError"""

    def _eval(self, scope):
        try:
            return func(self, scope)
        except (TypeError, ValueError) as exc:
            raise ExecutionError(self) from exc

    return _eval


class Ast:
    def __call__(self, scope):
        return self.eval(scope)


class Lookup(Ast):
    def __init__(self, *args):
        self.args = args

    @trap
    def eval(self, scope):
        value = scope
        for key in self.args:
            try:
                value = value[key]
            except (KeyError, TypeError):
                return getattr(scope, "default", None)

        return value

    def __str__(self):
        return f"Lookup({self.args})"


class Unary(Ast):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.__class__.__name__}({self.value})"


class Number(Unary):
    @trap
    def eval(self, _):
        return float(self.value) if "." in self.value else int(self.value)


class Boolean(Unary):
    @trap
    def eval(self, _):
        return self.value == "TRUE"


class String(Unary):
    @trap
    def eval(self, _):
        return self.value


class List(Unary):
    @trap
    def eval(self, scope):
        return [arg.eval(scope) for arg in self.value]


class Not(Unary):
    @trap
    def eval(self, scope):
        return not self.value.eval(scope)


def and_(left, right):
    if left is Nil or right is Nil:
        return Nil
    return left and right


def or_(left, right):
    if left is Nil or right is Nil:
        return Nil
    return left or right


def in_(left, right):
    if left is Nil or right is Nil:
        return Nil
    return left in right


class BinaryOp(Ast):
    oper = {
        # Logic ops
        "and": and_,
        "or": or_,
        # Math Ops
        "^": operator.pow,
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        # Comparison Ops
        "<": operator.lt,
        "<=": operator.le,
        "=": operator.eq,
        "<>": operator.ne,
        ">=": operator.ge,
        ">": operator.gt,
        "in": in_,
    }

    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

    @trap
    def eval(self, scope):
        op = self.oper[self.op]
        right = self.right.eval(scope)
        left = self.left.eval(scope)

        return op(left, right)

    def __str__(self):
        return f"Op({self.left} {self.op} {self.right})"


class Condition(Ast):
    def __init__(self, default, rules):
        self.rules, self.default = rules, default

    @trap
    def eval(self, scope):
        for cond, result in self.rules:
            if cond.eval(scope):
                return result.eval(scope)
        return self.default.eval(scope)

    def __str__(self):
        return f"Condition({self.rules} {self.default})"


class Function(Ast):
    def __init__(self, name, args):
        self.name, self.args = name, args

    @trap
    def eval(self, scope):
        args = [arg.eval(scope) for arg in self.args]

        return scope.functions[self.name](*args)
