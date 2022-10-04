
# `freezable`: Freezable types in Python

<a href="https://badge.fury.io/py/freezable"><img src="https://badge.fury.io/py/freezable.svg" alt="PyPI version" height="18"></a>
<a href="https://github.com/ederic-oytas/python-freezable/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ederic-oytas/python-freezable"></a>

> NOTICE: This project is in Alpha; you may encounter bugs.
  
Freezable is a package that allows you to implement "freezable" types in
Python, which can either be "frozen" or "unfrozen." When frozen, all operations
and methods that mutate the object are disabled.

Here is an example of a "freezable" stack and its usage:
```python
from freezable import Freezable, FrozenError, enabled_when_unfrozen

class FreezableStack(Freezable):
    
    def __init__(self):
        self._data = []  # data of the stack
    
    @enabled_when_unfrozen
    def push(self, x):  # pushes to the top of stack
        self._data.append(x)

    def top(self):  # returns top of stack, if any
        return self._data[-1] if self._data else None

# We can use the stack as normal.
stk = FreezableStack()
assert stk.top() is None
stk.push(1)
assert stk.top() == 1
stk.push(2)
assert stk.top() == 2

# Once we freeze it, all mutating methods/operations are disabled.
stk.freeze()
try:
    stk.push(3)  # error because stk is frozen
except FrozenError:
    pass
assert stk.top() == 2  # push did not happen

# We can unfreeze it to use the stack mutably again.
stk.unfreeze()
stk.push(3)
assert stk.top() == 3
```

This package can be useful in finding logical errors in which objects are
mutated when they are not supposed to.

To learn more about the package, check out the [User Guide](./user-guide.md).

## Links

[Repository @ GitHub][repo]

[PyPI Page][pypi]

## Installation

This package can be installed using Pip:
```
pip install freezable
```

## Bug Reports and Feature Requests

You can [report a bug or suggest a feature][issues] on the Github repo.

## Contributions

Contributions to this project are welcome. :)

See the [pull requests page on Github][pulls].

[repo]: https://github.com/ederic-oytas/python-freezable
[pypi]: https://pypi.org/project/freezable/
[issues]: https://github.com/ederic-oytas/python-freezable/issues/new/choose
[pulls]: https://github.com/ederic-oytas/python-freezable/pulls
