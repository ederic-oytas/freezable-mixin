
from functools import wraps
from typing import Callable, Optional, TypeVar


_F = TypeVar('_F', bound=Callable)
# Type variable for a Callable. This is used instead of just Callable so that
# the function signature can be preserved.


class FrozenError(RuntimeError):
    """Raised when an operation that could mutate a Freezable object
    is used when that object is frozen."""


class Freezable:
    """Freezable mixin class."""

    def __init__(self):
        """Initialize this Freezable object."""
        
        self._Freezable__frozen: bool
        object.__setattr__(self, '_Freezable__frozen', False)
        # True if this Freezable is frozen; False, otherwise.
        # This property is private. The name is pre-mangled to be consistent
        # object.__setattr__ calls.
    
    #
    # Freezing Methods
    #
    
    def freeze(self) -> None:
        """Freeze this object. All methods/operations that could mutate this
        object are disabled."""
        object.__setattr__(self, '_Freezable__frozen', True)

    def unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that could mutate this
        object are re-enabled."""
        object.__setattr__(self, '_Freezable__frozen', False)

    def is_frozen(self) -> bool:
        """Check if this object is frozen."""
        return self._Freezable__frozen


def disabled_when_frozen(method: _F) -> _F:
    """Instance method decorator to throw a ``FrozenError`` if the object is
    frozen. The class must subclass ``Freezable``.
    """
    
    @wraps(method)
    def wrapped(*args, **kwargs):
        self = args[0]
        if self._Freezable__frozen:
            if hasattr(method, '__name__'):
                raise FrozenError("cannot call method '%s' while object is "
                                  "frozen" % method.__name__)
            else:
                raise FrozenError("cannot call method while object is frozen")
        return method(*args, **kwargs)

    return wrapped  # type: ignore
