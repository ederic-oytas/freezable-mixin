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
            # Mutating methods
            #
            
            # These methods use the @enabled_when_unfrozen decorator. This
            # prevents the object from being mutated while the object is
            # frozen.
            
            @enabled_when_unfrozen
            def push(self, x):
                self._data.append(x)
            
            @enabled_when_unfrozen
            def pop(self):
                return self._data.pop()
            
            #
            # Non-mutating methods
            #
            
            # These methods are non-mutating and can be used any time.
            
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
        """Freezes this object. All methods/operations that could mutate this
        object become disabled."""
        _object_setattr(self, '_Freezable__frozen', True)

    def unfreeze(self) -> None:
        """Unfreezes this object. All methods/operations that could mutate this
        object become re-enabled."""
        _object_delattr(self, '_Freezable__frozen')

    def is_frozen(self) -> bool:
        """Checks if this object is frozen.
        
        Returns:
            True if this object is frozen; False otherwise.
        """
        return self.__frozen
        
    #
    # Special methods
    #
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        """Sets an attribute.
        
        This raises a FrozenError if this object is frozen. You may override
        this behavior in a subclass if needed.
        """
        if self.is_frozen():
            raise FrozenError('cannot set attributes while object is frozen')
        object.__setattr__(self, __name, __value)
    
    def __delattr__(self, __name: str) -> None:
        """Deletes an attribute.
        
        This raises a FrozenError is this object is frozen. You may override
        this behavior in a subclass if needed.
        """
        if self.is_frozen():
            raise FrozenError('cannot delete attributes while object is frozen')
        object.__delattr__(self, __name)        


def enabled_when_unfrozen(method: _F) -> _F:
    """Decorates a instance method to raise an `FrozenError` if the instance
    is frozen.
    
    If the decorated instance method is run while the instance is frozen, a
    `FrozenError` raised and the inner method body is not executed.
    
    It is required that the class that owns the instance method subclasses
    the `Freezable` class.
    
    Example: Example: Decorating Mutating Methods on a Freezable Stack
        This is one example of using the decorator in a class. Here, the
        decorator is used on the `push` and `pop` methods. This is to
        prevent the instance from being mutated while frozen.
        
        ```python
        
        from freezable import Freezable, enabled_when_unfrozen
        
        class FreezableStack(Freezable):
            
            def __init__(self):
                self._data = []
            
            @enabled_when_unfrozen
            def push(self, x):
                self._data.append(x)
            
            @enabled_when_unfrozen
            def pop(self):
                return self._data.pop()
            
            def top(self):
                if not self._data:
                    return None
                return self._data[-1]
        ```
        
        Example usage of the freezable stack:
        ```python
        stk = FreezableStack()
        
        assert stk.top() == None
        stk.push(1)
        assert stk.top() == 1
        stk.push(2)
        assert stk.top() == 2
        
        stk.freeze()
        try:
            stk.push(3)  # this raises FrozenError because stk is frozen
        except FrozenError:
            pass
        
        assert stk.top() == 2  # stack was not modified
        stk.unfreeze()
        
        stk.push(3)  # now we can push an element
        assert stk.top() == 3
        ```
    
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
