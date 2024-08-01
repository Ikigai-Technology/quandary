import pytest

from quandary.walker import NodeWalker


@pytest.mark.parametrize("src", [
    """(
        0.4 if foo.bar = "Baz",
        0.6 if foo.bar = "Qux",
        else 0.8
    )""",
])
def test_walker_smoke(src):
    walker = NodeWalker()

    walker.walk(src)
