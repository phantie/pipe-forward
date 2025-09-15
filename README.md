# pipe-forward

A tiny functional composition utility for Python.

It allows you to create pipelines of functions using the `|` operator.

Like `|>` (pipe forward) operator in #F sharp, but different in how value is passed - it can be both in prefix and suffix and passed with `@` or with standard python function calling semantics

---

## Usage

### Basic example

```python
from pipe_forward import P  # alias for StackPipe


assert "123" @ (P(int) | float) == 123.0 # tranform "123" to int, then to float
                                         # quickly interpreted as written - direct flow

# inverted flow (thumbs down)
assert float(int("123"))
```

### Call with standard semantics

```python
from pipe_forward import P
fn = P(int) | float
assert (P(int) | float)("123") == fn("123") == 123.0
```

### Call with @

```python
from pipe_forward import P
fn = P(int) | float
assert "123" @ fn == fn @ "123" == 123.0 # use prexix or suffix notation
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

## Why use this?

- Succinct function composition with `|` operator
- Type hint support
- Immutable
- Readable one-liners
- Explicit

---

## Installation

```bash
pip install git+https://github.com/phantie/pipe-forward.git -U
```
