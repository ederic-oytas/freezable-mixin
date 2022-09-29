<a href="https://badge.fury.io/py/freezable"><img src="https://badge.fury.io/py/freezable.svg" alt="PyPI version" height="18"></a>
<a href='https://python-freezable.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/python-freezable/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://github.com/ederic-oytas/python-freezable/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/ederic-oytas/python-freezable"></a>

# Freezable: Dynamically Immutable Objects

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

See the [documentation][1] for more information on how to use this project.

## Links

[Documentation @ReadTheDocs][1]

[PyPI Link](https://pypi.org/project/freezable/)

## Installation

This package can be installed using Pip:
```
pip install freezable
```

[1]: https://python-freezable.readthedocs.io


## Bug Reports and Feature Requests

You can [report a bug or suggest a feature][1] on the Github repo.


[1]: https://github.com/ederic-oytas/python-freezable/issues/new/choose
