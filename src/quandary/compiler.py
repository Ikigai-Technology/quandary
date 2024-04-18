from parsimonious.nodes import Node, NodeVisitor

from . import ast
from .grammar import grammar

def is_blank(node):
    """
    Helper to detect blank nodes
    """
    return isinstance(node, Node) and node.start == node.end


class Compiler(NodeVisitor):
    grammar = grammar

    def visit_condition_rule(self, node, visited_children):
        condition, _ , outcome = visited_children
        return condition, outcome 

    def visit_condition(self, node, visited_children):
        '''
        condition = "(" condition_rule ":" (condition_rule ":" )* expr ")"
        '''
        _, *expr, _, more, default, _ = visited_children
        
        if more and not is_blank(more):
            for new_expr, _ in more:
                expr = (*expr, new_expr)
        
        return ast.Condition(default, expr)

    def generic_visit(self, node, visited_children):
        # Since we turn whitespace into None, strip those nodes where possible.
        return [c for c in visited_children if c is not None] or node

    def visit_expr(self, _, visited_children):
        _, expr, _ = visited_children
        return expr

    def visit_logical_expr(self, _, visited_children):
        expr, more = visited_children

        if not is_blank(more):
            for op, right in more:
                expr = ast.BinaryOp(expr, op, right)

        return expr

    def visit_not_expr(self, _, visited_children):
        more, term = visited_children

        if not is_blank(more):
            term = ast.Not(term)

        return term

    def visit_comparison_expr(self, _, visited_children):
        expr, more = visited_children

        if not is_blank(more):
            for op, right in more:
                expr = ast.BinaryOp(expr, op, right)

        return expr

    def visit_sum_expr(self, _, visited_children):
        term, more = visited_children

        if not is_blank(more):
            for op, right in more:
                term = ast.BinaryOp(term, op, right)

        return term

    def visit_factor_expr(self, _, visited_children):
        term, more = visited_children

        if not is_blank(more):
            for op, right in more:
                term = ast.BinaryOp(term, op, right)

        return term

    def visit_power_expr(self, _, visited_children):
        term, more = visited_children

        if not is_blank(more):
            for op, right in more:
                term = ast.BinaryOp(term, op, right)

        return term

    def visit_term(self, _, visited_children):
        return visited_children[0]

    def visit_arguments(self, _, visited_children):
        arg, more = visited_children

        args = (arg,)
        if not is_blank(more):
            for _, arg in more:
                args = (*args, arg)

        return args

    def visit_function(self, _, visited_children):
        name, _, arguments, _ = visited_children

        if not is_blank(arguments):
            args = arguments[0]
        else:
            args = ()

        return ast.Function(name, args)

    def visit_parens(self, _, visited_children):
        _, _, expr, _, _ = visited_children

        return expr

    def visit_bool_operator(self, node, _):
        return node.text

    def visit_sum_operator(self, node, _):
        return node.text

    def visit_factor_operator(self, node, _):
        return node.text

    def visit_power_operator(self, node, _):
        return node.text

    def visit_comparison_operator(self, node, _):
        return node.text

    def visit_lookup(self, _, visited_children):
        args, more = visited_children
        args = [args]
        if not is_blank(more):
            for _, name in more:
                args.append(name)

        return ast.Lookup(*args)

    def visit_name(self, node, _):
        return node.text

    def visit_number(self, node, _):
        return ast.Number(node.text)

    def visit_boolean(self, node, _):
        return ast.Boolean(node.text)

    def visit_string(self, node, _):
        return ast.String(node.text[1:-1].replace(r"\"", '"'))

    def visit_ws(self, _, __):
        return None


compiler = Compiler()
