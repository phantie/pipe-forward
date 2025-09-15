from __future__ import annotations
from typing import Callable, TypeVar, Generic

__all__ = ["P", "StackPipe", "LoopPipe"]

# Input type
T = TypeVar("T")
# Output types
O = TypeVar("O")
X = TypeVar("X")


class P(Generic[T, X]):
    """
    A functional pipeline that composes functions using recursion.

    Each `|` creates a new `P` wrapping the previous pipeline.

    Example:
        >>> from pipe import P
        >>> pipe = P(str) | int | float
        >>> pipe(123)
        123.0
        >>> result = pipe @ 123
        >>> result
        123.0
        >>> result = 123 @ pipe
        >>> result
        123.0
    """

    def __init__(self, fn: Callable[[T], X]):
        self.fn = fn

    def __or__(self, other: Callable[[X], O]) -> P[T, O]:
        """Return a new pipeline by composing this pipe with another function."""
        fn = lambda x: other(self.fn(x))
        return P(fn)

    def __call__(self, arg: T) -> X:
        """Apply the pipeline to an argument."""
        return self.fn(arg)

    def __matmul__(self, arg: T) -> X:
        """
        Apply the pipeline to an argument using the `@` operator.

        Example:
            >>> pipe = P(str) | int | float
            >>> result = pipe @ 123
            >>> result
            123.0
        """
        return self(arg)  # Just call the pipeline

    def __rmatmul__(self, arg: T) -> X:
        """
        Apply the pipeline to the left-hand argument using the `@` operator.

        Example:
            >>> pipe = P(str) | int | float
            >>> result = 123 @ pipe
            >>> result
            123.0
        """
        return self(arg)  # Same behavior


# Alias
StackPipe = P


class LoopPipe(Generic[T, X]):
    """
    A functional pipeline that stores a list of functions
    and applies them sequentially in a loop.

    Example:
        >>> from pipe import LoopPipe
        >>> pipe = LoopPipe(str) | int | float
        >>> pipe(123)
        123.0
        >>> result = pipe @ 123
        >>> result
        123.0
        >>> result = 123 @ pipe
        >>> result
        123.0
    """

    def __init__(self, fn: Callable[[T], X]):
        self.fns = [fn]

    def __or__(self, other: Callable[[X], O]) -> LoopPipe[T, O]:
        """Return a new pipeline by appending a function to the sequence."""
        fns = [*self.fns, other]
        pipe = LoopPipe(...)
        pipe.fns = fns
        return pipe

    def __call__(self, arg: T) -> O:
        """Apply the pipeline to an argument."""
        res = arg
        for fn in self.fns:
            res = fn(res)
        return res

    def __matmul__(self, arg: T) -> O:
        """
        Apply the pipeline to an argument using the `@` operator.

        Example:
            >>> pipe = LoopPipe(str) | int | float
            >>> result = pipe @ 123
            >>> result
            123.0
        """
        return self(arg)  # Just call the pipeline

    def __rmatmul__(self, arg: T) -> O:
        """
        Apply the pipeline to the left-hand argument using the `@` operator.

        Example:
            >>> pipe = LoopPipe(str) | int | float
            >>> result = 123 @ pipe
            >>> result
            123.0
        """
        return self(arg)  # Same behavior
