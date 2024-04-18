from functools import wraps


def dumplist(l, idx="", indent=0):
    prefix = " " * (indent + len(str(idx)))
    if not isinstance(l, list):
        print(
            prefix,
            f"{idx}> ",
            l,
        )
    else:
        print(prefix, "[")
        for i, item in enumerate(l):
            dumplist(item, i, indent + 2)
        print(prefix, "]")


def debug(method):
    @wraps(method)
    def _inner(self, node, visited_children):
        print(method.__name__.upper(), node.expr.name, node.text)
        dumplist(visited_children)
        result = method(self, node, visited_children)
        print("<< ", result)
        return result

    return _inner