
from functools import wraps
from typing import Any, Callable, Optional, TypeVar


_F = TypeVar('_F', bound=Callable)
# Type variable for a Callable. This is used instead of just Callable so that
# the function signature can be preserved.


class FrozenError(RuntimeError):
    """Raised when an operation that could mutate a Freezable object
    is used when that object is frozen."""


class Freezable:
    """Freezable mixin class."""
    
    _Freezable__frozen_flag: bool = False
    
    #
    # Freezing Methods
    #
    
    def freeze(self) -> None:
        """Freeze this object. All methods/operations that could mutate this
        object are disabled."""
        object.__setattr__(self, '_Freezable__frozen_flag', True)

    def unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that could mutate this
        object are re-enabled."""
        object.__setattr__(self, '_Freezable__frozen_flag', False)

    def is_frozen(self) -> bool:
        """Check if this object is frozen."""
        return self._Freezable__frozen_flag
        
    #
    # Special methods
    #
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        """Set an attribute. Raises a FrozenError if this object is frozen."""
        if self.is_frozen():
            raise FrozenError('cannot set attributes while object is frozen')
        object.__setattr__(self, __name, __value)
    
    def __delattr__(self, __name: str) -> None:
        """Delete an attribute. Raises a FrozenError is this object is frozen."""
        if self.is_frozen():
            raise FrozenError('cannot set attributes while object is frozen')
        object.__delattr__(self, __name)        


def enabled_when_unfrozen(method: _F) -> _F:
    """Instance method decorator that raises a ``FrozenError`` if the object
    is frozen. The class must subclass ``Freezable``.
    """
    
    @wraps(method)
    def wrapped(*args, **kwargs):
        self = args[0]
        if self.is_frozen():
            if hasattr(method, '__name__'):
                raise FrozenError("cannot call method '%s' while object is "
                                  "frozen" % method.__name__)
            else:
                raise FrozenError("cannot call method while object is frozen")
        return method(*args, **kwargs)

    return wrapped  # type: ignore
