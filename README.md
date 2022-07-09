# `freezable` - Freezable objects in Python

This Python package provides a mixin class to implement "freezable" objects.
When an object is frozen, the data contained within the object is marked as
immutable.

## Basic Usage

`freezable` provides the `Freezable` mixin class for user-defined objects:

```
from freezable import Freezable

class SomeFreezable(Freezable):
    ...
```

**You do not need to call __init__ for this class;** you only need to subclass
it, even in multiple inheritance.

To freeze an freezable object, use the `freeze()` method, and to unfreeze, use
the `unfreeze()` method. You can check if a freezable object is frozen using
the `is_frozen()` method.

```
obj = SomeFreezable()

assert not obj.is_frozen()

obj.freeze()
assert obj.is_frozen()

obj.unfreeze()
assert not obj.is_frozen()
```

While an object is frozen, setting and deleting attributes of that object
is disabled; these operations raise a `FrozenError`.

```
obj = SomeFreezable()
obj.freeze()

# Both of these operations will raise a FrozenError:
obj.attr = 5
del obj.attr
```

If you don't want this behavior, you can override the special methods in the
class body:
```
__setattr__ = object.__setattr__
__delattr__ = object.__delattr__
```

The package also provides the `@disabled_when_frozen` instance method decorator
which raises a `FrozenError` when the object is frozen. Make sure to only use
this decorator in a class that subclasses `Freezable`.

```
class SomeFreezable(Freezable):
    @disabled_when_frozen
    def some_mutating_method(self):
        ...
```
