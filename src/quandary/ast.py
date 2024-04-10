import operator


class Ast:
    def __call__(self, scope):
        return self.eval(scope)


class Lookup(Ast):
    def __init__(self, *args):
        self.args = args

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
    def eval(self, _):
        return float(self.value) if "." in self.value else int(self.value)


class Boolean(Unary):
    def eval(self, _):
        return self.value == "TRUE"


class String(Unary):
    def eval(self, _):
        return self.value


class Not(Unary):
    def eval(self, scope):
        return not self.value.eval(scope)


class BinaryOp(Ast):
    oper = {
        # Logic ops
        "and": lambda left, right: left and right,
        "or": lambda left, right: left or right,
        # Math Ops
        "**": operator.pow,
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
    }

    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

    def eval(self, scope):
        op = self.oper[self.op]
        left = self.left.eval(scope)
        right = self.right.eval(scope)

        return op(left, right)

    def __str__(self):
        return f"Op({self.left} {self.op} {self.right})"


class Function(Ast):
    def __init__(self, name, args):
        self.name, self.args = name, args

    def eval(self, scope):
        args = [arg.eval(scope) for arg in self.args]

        return scope.functions[self.name](*args)
