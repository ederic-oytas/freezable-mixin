"""
Module for the Freezable class and related functions and classes.
"""

from functools import wraps
from typing import Any, Callable, Optional, TypeVar


_F = TypeVar('_F', bound=Callable)
"""Type variable for a Callable. This is used instead of just Callable so that
the function signature can be preserved."""

_object_setattr = object.__setattr__
_object_delattr = object.__delattr__


class FrozenError(RuntimeError):
    """Raised when an operation that could mutate a Freezable object
    is used when that object is frozen."""


class Freezable:
    """A mixin class that allows instances to marked as "frozen" or "unfrozen."
    
    When an instance is "frozen," it is treated as an *immutable* object.
    While it is frozen, all mutating operations/methods are disabled.
    
    This class can be used both in cases of single and multiple inheritance.
    
    There is no need to call `super().__init__()` when initializing instances
    of subclasses of this class.
    
    Example: Example: Freezable Stack
        Here is an example of a freezable stack data structure:
        ```python
        from freezable import Freezable, enabled_when_unfrozen
        
        class FreezableStack(Freezable):
            
            def __init__(self):
                self._data = []
            
            #
            # Mutable operations
            #
            
            # These operations are disabled using the @enabled_when_unfrozen
            # decorator when the object is frozen because it would mutate the
            # object.
            
            @enabled_when_unfrozen
            def push(self, x):
                self._data.append(x)
            
            @enabled_when_unfrozen
            def pop(self):
                return self._data.pop()
            
            #
            # Immutable operations
            #
            
            def is_empty(self):
                return not bool(self._data)
            
            def top(self):
                return self._data[-1] if self._data else None
        ```
    """
    
    __frozen: bool = False
    """True if this object is marked as 'frozen'; false otherwise."""
    
    #
    # Freezing-related Methods
    #
    
    def freeze(self) -> None:
        """Freeze this object. All methods/operations that could mutate this
        object become disabled."""
        _object_setattr(self, '_Freezable__frozen', True)

    def unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that could mutate this
        object become re-enabled."""
        _object_delattr(self, '_Freezable__frozen')

    def is_frozen(self) -> bool:
        """Check if this object is frozen.
        
        Returns:
            True if this object is frozen; False otherwise.
        """
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
    is frozen. The class that owns the method must subclass ``Freezable``.
    
    Args:
        method: Instance method to wrap. The class that owns this method
            must subclass ``Freezable``. (Note: Type `_F` is a type variable
            that is bounded by `Callable`.)
    
    Raises:
        FrozenError: When this method is called while the instace is frozen.
    
    Returns:
        A wrapped instance method thar raises ``FrozenError`` if the object
            is frozen. (Note: Type `_F` is a type variable that is bounded by
            `Callable`.)
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
