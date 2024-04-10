# ruff: noqa: S101
import pytest
from quandary.ast import BinaryOp
from quandary.nil import Nil, NilType


def test_singleton():
    n = NilType()

    assert n is Nil


@pytest.mark.parametrize("op", BinaryOp.oper.values())
def test_operators(op):
    assert op(1, Nil) is Nil
    assert op(Nil, 1) is Nil
