
# User Guide

## Installation

You can install the package using Pip:

```
$ pip install freezable
```

---

## Basic Usage

This package introduces the idea of a "freezable" type; instances of such
can be "frozen" or "unfrozen." When frozen, the freezable instance is marked
as *immutable*. Semantically, the object should not and must not be changed.

---

### The `Freezable` Class

Freezable types are implemented by subclassing the ``Freezable`` class:

```python
from freezable import Freezable

class SomeFreezable(Freezable):
    ...
```

**You do not need to call __init__ for this class;** you only need to subclass
it. The subclass is also allowed to inherit from other classes other than
`Freezable` as well.

---

### `freeze`, `unfreeze`, and `is_frozen`

A freezable instance starts off as unfrozen. To freeze a freezable object,
use the `freeze()` method. To unfreeze, use the `unfreeze()` method. You can
check if a freezable object is frozen using the `is_frozen()` method.

```python
from freezable import Freezable

class SomeFreezable(Freezable):
    ...

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

<!--pytest-codeblocks:cont-->
```python
obj = SomeFreezable()
obj.freeze()
```

<!--pytest.mark.skip(reason="this raises FrozenError")-->
```python
# Both of these operations will raise a FrozenError:
obj.attr = 5
del obj.attr
```

This behavior helps ensure the guarantee that the object remains immutable
while it is frozen. Note that this introduces some overhead to every attribute
set and delete.

If you don't want this behavior (for performance or some other reason), you can
override the `__setattr__` and `__delattr__` methods in the class body:
<!--pytest.mark.skip(reason="this is to be run in a class")-->
```python
__setattr__ = object.__setattr__
__delattr__ = object.__delattr__
```

---

### `@enabled_when_unfrozen`

Your class may have methods that mutate the instance itself. If any of
these mutating methods are called while the object is frozen, they may succeed
and break the frozen guarantee of the class.

For mutating methods, the package provides the `@enabled_when_unfrozen` instance
method decorator. This decorator enables a method only if the instance is
unfrozen. When it is frozen, it raises a `FrozenError`.

```python
from freezable import Freezable, enabled_when_unfrozen

class SomeFreezable(Freezable):
    @enabled_when_unfrozen
    def some_mutating_method(self):
        ...

frz = SomeFreezable()

assert not frz.is_frozen()
frz.some_mutating_method()  # Does not raise an error when instance is unfrozen

frz.freeze()
assert frz.is_frozen()
#frz.some_mutating_method()  # Raises `FrozenError` because instance is frozen
```

---

## Further Reading

This is the end of the user guide. For further information, use the links
below or the links on the sidebar to the left.

- Take a look at the [Reference](./reference.md).
- See planned features in the [Roadmap](./roadmap.md).
- [Report a bug or suggest a feature][issues] at the Github repo.
- Contribute with a [pull request][pulls].

[issues]: https://github.com/ederic-oytas/python-freezable/issues/new/choose
[pulls]: https://github.com/ederic-oytas/python-freezable/pulls
