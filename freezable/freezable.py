
from functools import wraps
from typing import Any, Callable, Optional, TypeVar


_F = TypeVar('_F', bound=Callable)
# Type variable for a Callable. This is used instead of just Callable so that
# the function signature can be preserved.


class _FrozenStatus:
    """Data class that stores the frozen status of a Freezable object."""
    
    def __init__(self):
        """Create a _FrozenStatus object with a status of unfrozen."""
        self.frozen: bool = False


class FrozenError(RuntimeError):
    """Raised when an operation that could mutate a Freezable object
    is used when that object is frozen."""


class Freezable:
    """Freezable mixin class."""
    
    #
    # Frozen Status
    #
    @property
    def _Freezable__status(self) -> _FrozenStatus:
        """True if this object is frozen; False otherwise. This property is
        considered to be private; its name is pre-mangled."""
        return self.__dict__.setdefault('_Freezable__status', _FrozenStatus())
    
    #
    # Freezing Methods
    #
    
    def freeze(self) -> None:
        """Freeze this object. All methods/operations that could mutate this
        object are disabled."""
        self._Freezable__status.frozen = True

    def unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that could mutate this
        object are re-enabled."""
        self._Freezable__status.frozen = False

    def is_frozen(self) -> bool:
        """Check if this object is frozen."""
        return self._Freezable__status.frozen
        
    #
    # Special methods
    #
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        """Set an attribute. Raises a FrozenError if this object is frozen."""
        if self._Freezable__status.frozen:
            raise FrozenError('cannot set attributes while object is frozen')
        object.__setattr__(self, __name, __value)
    
    def __delattr__(self, __name: str) -> None:
        """Delete an attribute. Raises a FrozenError is this object is frozen."""
        if self._Freezable__status.frozen:
            raise FrozenError('cannot set attributes while object is frozen')
        object.__delattr__(self, __name)        


def disabled_when_frozen(method: _F) -> _F:
    """Instance method decorator to throw a ``FrozenError`` if the object is
    frozen. The class must subclass ``Freezable``.
    """
    
    @wraps(method)
    def wrapped(*args, **kwargs):
        self = args[0]
        if self._Freezable__status.frozen:
            if hasattr(method, '__name__'):
                raise FrozenError("cannot call method '%s' while object is "
                                  "frozen" % method.__name__)
            else:
                raise FrozenError("cannot call method while object is frozen")
        return method(*args, **kwargs)

    return wrapped  # type: ignore
