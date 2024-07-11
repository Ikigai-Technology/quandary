from . import ast, compiler


class NodeWalker:
    """
    Complied expression node walker

    walker = Walker()
    walker.walk(string | code)

    Sub-class and add methods for `handle_{NodeName}`
    """

    def walk(self, code):
        if not isinstance(code, ast.Ast):
            code = compiler.parse(code)
        self.visit(code)

    def visit(self, node):  # noqa: C901 too complex
        if isinstance(node, ast.Lookup):
            pass
        elif isinstance(node, ast.List):
            for item in node.value:
                self.visit(item)
        elif isinstance(node, ast.Unary):
            if isinstance(node.value, ast.Ast):
                self.visit(node.value)
        elif isinstance(node, ast.BinaryOp):
            self.visit(node.left)
            self.visit(node.right)
        elif isinstance(node, ast.Condition):
            for rule in node.rules:
                self.visit(rule)
            self.visit(node.default)
        elif isinstance(node, ast.Function):
            for arg in node.args:
                self.visit(arg)
        else:
            raise TypeError(f"Unknown node type: {node}")

        handler = getattr(self, f"handle_{node.__class__.__name__}", self.handle_generic)
        handler(node)

    def handle_generic(self, node):
        pass
