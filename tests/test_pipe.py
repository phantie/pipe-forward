import pytest
from pipe_forward import StackPipe
from pipe_forward import LoopPipe


@pytest.mark.parametrize("P", [StackPipe, LoopPipe])
def test_pipe_basic(P):
    p = P(str)
    res = p(1)
    assert res == "1"

    p = p | int
    res = p(1)
    assert res == 1

    p = p | bytes
    res = p(1)
    assert res == bytes(1)


@pytest.mark.parametrize("P", [StackPipe, LoopPipe])
def test_example_basic(P):
    from pipe_forward import P  # alias for StackPipe

    assert "123" @ (P(int) | float) == 123.0  # tranform "123" to int, then to float


@pytest.mark.parametrize("P", [StackPipe, LoopPipe])
def test_example_standard_call_semantics(P):
    from pipe_forward import P

    fn = P(int) | float
    assert (P(int) | float)("123") == fn("123") == 123.0


@pytest.mark.parametrize("P", [StackPipe, LoopPipe])
def test_example_prefix_suffix_notations(P):
    from pipe_forward import P

    fn = P(int) | float
    assert "123" @ fn == fn @ "123" == 123.0  # use prexix or suffix notation


@pytest.mark.parametrize("P", [StackPipe, LoopPipe])
def test_example_one_liner(P):
    from operator import itemgetter

    value = {
        "Alexander": {"age": 25},
        "Vladimir": {"age": 25},
    }

    assert (P(itemgetter("Alexander")) | itemgetter("age") | str)(value) == "25"


@pytest.mark.parametrize("P", [StackPipe, LoopPipe])
def test_example_compose(P):
    from pipe_forward import P

    to_int = P(int)  # linter correctly recognizes it as P[object, int]
    to_str = to_int | str  # linter recognizes it as P[object, str]

    assert to_int(42.0) == 42
    assert to_str(42.0) == "42"


def test_typehints_stack_pipe():
    from pipe_forward import P

    to_int = P(int)  # linter correctly recognizes it as P[object, int]
    to_str = to_int | str  # linter recognizes it as P[object, str]

    assert to_int(42.0) == 42
    assert to_str(42.0) == "42"


def test_pipe_with_pipe():
    from pipe_forward import P

    p = P(str)
    res = p(1)
    assert res == "1"

    p = p | P(int)
    res = p(1)
    assert res == 1


def test_pipe_example_equal_behavior():
    from pipe_forward import StackPipe
    from pipe_forward import LoopPipe

    stack = StackPipe(float) | str
    loop = LoopPipe(float) | str

    assert stack(10) == loop(10) == "10.0"


def test_operator():
    from pipe_forward import P

    to_int = P(int)  # linter correctly recognizes it as P[object, int]
    to_str = to_int | str  # linter recognizes it as P[object, str]

    assert to_int @ 42.0 == 42
    assert 42.0 @ to_int == 42
    assert to_str @ 42.0 == "42"
    assert 42.0 @ (to_int | str) == "42"
