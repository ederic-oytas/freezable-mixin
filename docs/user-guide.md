
# User Guide

## Installation

You can install the package using Pip:

```
$ pip install freezable
```

---

## Basic Usage

### The `Freezable` Class

Freezable types are implemented by subclassing the ``Freezable`` mixin class:

```python
from freezable import Freezable

class SomeFreezable(Freezable):
    ...
```

**You do not need to call __init__ for this class;** you only need to subclass
it.

### `freeze`, `unfreeze`, and `is_frozen`

To freeze an freezable object, use the `freeze()` method; to unfreeze, use
the `unfreeze()` method. You can check if a freezable object is frozen using
the `is_frozen()` method.

```python
obj = SomeFreezable()

assert not obj.is_frozen()

obj.freeze()
assert obj.is_frozen()

obj.unfreeze()
assert not obj.is_frozen()
```

While an object is frozen, setting and deleting attributes of that object
is disabled; these operations raise a `FrozenError` while it is frozen.

```python
obj = SomeFreezable()
obj.freeze()

# Both of these operations will raise a FrozenError:
obj.attr = 5
del obj.attr
```

If you don't want this behavior, you can override the special methods in the
class body:
```python
__setattr__ = object.__setattr__
__delattr__ = object.__delattr__
```

The package also provides the `@enabled_when_unfrozen` instance method
decorator only enables a method if the object is unfrozen; when it is frozen,
it raises a `FrozenError`. Make sure to only use this decorator in a class
that subclasses `Freezable`.

```python
class SomeFreezable(Freezable):
    @enabled_when_unfrozen
    def some_mutating_method(self):
        ...
```
