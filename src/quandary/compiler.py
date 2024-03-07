from functools import wraps

from parsimonious.nodes import NodeVisitor

from . import ast
from .grammar import grammar


def catch(method):
    """
    Decorator to catch any match/case falling through.
    """

    @wraps(method)
    def _inner(self, node, visited_children):
        result = method(self, node, visited_children)
        if result is None:
            raise ValueError(f"{method.__name__.upper()}: Failed to parse: {visited_children}")
        return result

    return _inner


class Compiler(NodeVisitor):
    grammar = grammar

    def generic_visit(self, node, visited_children):
        # Since we turn requisite whitespace into None, strip those nodes where
        # possible.
        return [c for c in visited_children if c is not None] or node

    @catch
    def visit_bool_expr(self, _, visited_children):
        """
        bool_expr = (bool_term _ "or" _ bool_term) / bool_term
        """
        match visited_children:
            case [[left, _, right]]:
                return ast.BinaryOp(left, "or", right)
            case [term]:
                return term

    @catch
    def visit_bool_term(self, _, visited_children):
        """
        bool_term = (bool_factor _ "and" _ bool_factor) / bool_factor
        """
        match visited_children:
            case [[left, _, right]]:
                return ast.BinaryOp(left, "and", right)
            case [factor]:
                return factor

    @catch
    def visit_bool_factor(self, _, visited_children):
        """
        bool_factor = ("(" bool_expr ")") / ("not" _ bool_factor) / comparison
        """
        match visited_children:
            case [[_, expr, _]]:
                return expr
            case [[_, factor]]:
                return ast.Not(factor)
            case [comparison]:
                return comparison

    # Comparisons

    @catch
    def visit_comparison(self, _, visited_children):
        """
        comparison = (sum _ comp_op _ sum) / sum
        """
        match visited_children:
            case [[left, op, right]]:
                return ast.BinaryOp(left, op, right)
            case [sum]:
                return sum

    @catch
    def visit_comp_op(self, node, _):
        """
        comp_op = "<" / "<=" / "=" / "<>" / ">=" / ">"
        """
        return node.text

    # Basic maths

    @catch
    def visit_sum(self, _, visited_children):
        """
        sum = (term _ sum_op _ sum) / term
        """
        match visited_children:
            case [[left, op, right]]:
                return ast.BinaryOp(left, op, right)
            case [term]:
                return term

    def visit_sum_op(self, node, _):
        """
        sum_op = "+" / "-"
        """
        return node.text

    @catch
    def visit_term(self, _, visited_children):
        """
        term = (factor _ prod_op _ term) / factor
        """
        match visited_children:
            case [[left, op, right]]:
                return ast.BinaryOp(left, op, right)
            case [factor]:
                return factor

    def visit_prod_op(self, node, _):
        """
        prod_op = "*" / "/"
        """
        return node.text

    def visit_factor(self, _, visited_children):
        """
        factor = function / string / boolean / lookup / number / factor
        """
        return visited_children[0]

    # Functions

    @catch
    def visit_arguments(self, _, visited_children):
        """
        arguments = (bool_expr "," _ arguments) / bool_expr
        """
        match visited_children:
            case [[expr, _, arguments]]:
                return (expr, *arguments)
            case [expr]:
                return (expr,)

    def visit_function(self, _, visited_children):
        """
        function = name "(" arguments ")"
        """
        name, _, args, _ = visited_children

        return ast.Function(name, args)

    # Basic value sources

    @catch
    def visit_lookup(self, _, visited_children):
        """
        lookup = (name "." name) / name
        """
        match visited_children:
            case [[root, _, key]]:
                return ast.Lookup(root, key)
            case [root]:
                return ast.Lookup(root)

    def visit_name(self, node, _):
        return node.text

    def visit_number(self, node, _):
        return ast.Number(node.text)

    def visit_boolean(self, node, _):
        return ast.Boolean(node.text)

    def visit_string(self, node, _):
        return ast.String(node.text[1:-1].replace(r"\"", '"'))

    def visit__(self, _, __):
        return None


compiler = Compiler()
