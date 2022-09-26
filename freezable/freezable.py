
from functools import wraps
from typing import Any, Callable, Optional, TypeVar


_F = TypeVar('_F', bound=Callable)
# Type variable for a Callable. This is used instead of just Callable so that
# the function signature can be preserved.

_object_setattr = object.__setattr__
"""Variable set to object.__setattr__"""


class FrozenError(RuntimeError):
    """Raised when an operation that could mutate a Freezable object
    is used when that object is frozen."""


class Freezable:
    """Freezable mixin class."""
    
    __frozen: bool = False
    """True if this object is marked as 'frozen'; false otherwise."""
    
    #
    # Freezing Methods
    #
    
    def freeze(self) -> None:
        """Freeze this object. All methods/operations that could mutate this
        object are disabled."""
        _object_setattr(self, '_Freezable__frozen', True)

    def unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that could mutate this
        object are re-enabled."""
        _object_setattr(self, '_Freezable__frozen', False)

    def is_frozen(self) -> bool:
        """Check if this object is frozen."""
        return self.__frozen
        
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
                raise FrozenError(f"cannot call method '{method.__name__}' "
                                   "while object is frozen")
            else:
                raise FrozenError("cannot call method while object is frozen")
        return method(*args, **kwargs)

    return wrapped  # type: ignore
