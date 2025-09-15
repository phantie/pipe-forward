import pytest
from pipe_forward._impl import StackPipe
from pipe_forward._impl import LoopPipe


@pytest.mark.parametrize("P", [StackPipe, LoopPipe])
def test_pipe_basic(P):
    pipe_forward = P(str)
    res = pipe_forward(1)
    assert res == "1"

    pipe_forward = pipe_forward | int
    res = pipe_forward(1)
    assert res == 1

    pipe_forward = pipe_forward | bytes
    res = pipe_forward(1)
    assert res == bytes(1)


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

    pipe_forward = P(str)
    res = pipe_forward(1)
    assert res == "1"

    pipe_forward = pipe_forward | P(int)
    res = pipe_forward(1)
    assert res == 1

def test_pipe_example_equal_behavior():
    from pipe_forward import StackPipe
    from pipe_forward import LoopPipe

    stack = StackPipe(float) | str
    loop = LoopPipe(float) | str

    assert stack(10) == loop(10) == "10.0"
