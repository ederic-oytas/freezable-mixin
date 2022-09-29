
# `freezable`: Freezable types in Python

<a href="https://badge.fury.io/py/freezable"><img src="https://badge.fury.io/py/freezable.svg" alt="PyPI version" height="18"></a>
<a href="https://github.com/ederic-oytas/python-freezable/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ederic-oytas/python-freezable"></a>

> NOTICE: This project is in Alpha; expect bugs! API is also subject to
  change.
  
Freezable is a package that allows you to implement "freezable" types in
Python, which can either be "frozen" or "unfrozen." When frozen, all operations
and methods that mutate the object are disabled.

Here is one example:
```python
from freezable import Freezable, FrozenError, enabled_when_unfrozen

class FreezableStack(Freezable):
    
    def __init__(self):
        self._data = []
    
    @enabled_when_unfrozen
    def push(self, x):
        self._data.append(x)

    def top(self):
        return self._data[-1] if self._data else None

stk = FreezableStack()
assert stk.top() is None

stk.push(1)
assert stk.top() == 1
stk.push(2)
assert stk.top() == 2

stk.freeze()

try:
    stk.push(3)  # error because stk is frozen
except FrozenError:
    pass

assert stk.top() == 2  # operation did not proceed

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
