# ruff: noqa: S101
from quandary import Scope, compiler


class Sentinel:
    pass


def test_fallback():
    scope = Scope(default=Sentinel)

    func = compiler.parse("a")

    result = func(scope)

    assert result is Sentinel
