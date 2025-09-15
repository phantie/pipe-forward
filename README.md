# pipe-forward

A tiny functional composition utility for Python.

It allows you to create pipelines of functions using the `|` operator.

Like `|>` (pipe forward) operator in #F sharp.

---

## Why use this?

- Succinct function composition with `|` operator
- Type hint support
- Immutable
- Readable one-liners
- Explicit
- Predictable

## Usage

### Basic example

```python
from pipe_forward import P  # alias for StackPipe

fn = P(int) | float # parse to int, and then convert to float
result = fn("123") # call the composed fn
assert result == 123.0
```

### Composability

```python
from pipe_forward import P
# linter correctly recognizes it as P[object, int]

to_int = P(int) # convert to int
# linter correctly recognizes it as P[object, str]
to_str = to_int | str # convert to int, and then to str

assert to_int(42.0) == 42
assert to_str(42.0) == "42"
```

### StackPipe vs LoopPipe behavior

`StackPipe` and `LoopPipe` are provided, with `P` as a short alias for `StackPipe`. They inhibit equal behavior, but implemented differently.

```python
from pipe_forward import StackPipe
from pipe_forward import LoopPipe

stack = StackPipe(float) | str
loop = LoopPipe(float) | str

assert stack(10) == loop(10) == "10.0"
```

---

## Installation

```bash
pip install git+https://github.com/phantie/pipe-forward.git -U
```
