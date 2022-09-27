
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

---

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

---

### Freezing Disables Setting and Deleting Attributes

While an object is frozen, setting and deleting attributes of that object
is disabled; these operations raise a `FrozenError` while it is frozen.

```python
obj = SomeFreezable()
obj.freeze()

# Both of these operations will raise a FrozenError:
obj.attr = 5
del obj.attr
```

Note that this introduces some overhead to every attribute set and delete.

If you don't want this behavior (for performance or some other reason), you can
override the `__setattr__` and `__delattr__` methods with the ones from
`object` in the class body:
```python
__setattr__ = object.__setattr__
__delattr__ = object.__delattr__
```

---

### `@enabled_when_unfrozen`

The package also provides the `@enabled_when_unfrozen` instance method
decorator. This decorator only enables a method if the instance is unfrozen.
When it is frozen, it raises a `FrozenError`.

```python
class SomeFreezable(Freezable):
    @enabled_when_unfrozen
    def some_mutating_method(self):
        ...

frz = SomeFreezable()

assert not frz.is_frozen()
frz.some_mutating_method()  # Does not raise an error

frz.freeze()
assert frz.is_frozen()
frz.some_mutating_method()  # Raises `FrozenError`

```
