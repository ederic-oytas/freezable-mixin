
# `freezable`: Freezable types in Python

> NOTICE: This project is in Alpha; expect bugs! API is also subject to
  change.
  
Freezable is a package that allows you to implement "freezable" types in
Python. When an object is "frozen," it is marked as "immutable," and data
contained within the object cannot be changed.

Example Usage:
```python
from freezable import Freezable


class SomeFreezable(Freezable):
    ...
    
    
obj = SomeFreezable()
obj.freeze()
assert obj.is_frozen()

obj.unfreeze()
assert not obj.is_frozen()
```
