

from typing import Any


class _FreezableData:
    """Holds the data for the Freezable mixin."""

    def __init__(self):
        
        self.frozen: bool = False
        # True if the Freezable object is frozen; False otherwise.


class FrozenError(RuntimeError):
    """Raised when an operation that could mutate a Freezable object
    is used when that object is frozen."""


class Freezable:
    """Freezable mixin class."""

    def __init__(self):
        """Initialize this Freezable object."""
        
        self.__data: _FreezableData = _FreezableData()
        # Where the Freezable data is stored
    
    #
    # Freezing Methods
    #
    
    def _freeze(self) -> None:
        """Freeze this object. All methods/operations that could mutate this
        object are disabled."""
        self.__data.frozen = True

    def _unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that could mutate this
        object are re-enabled."""
        self.__data.frozen = False

    def _is_frozen(self) -> bool:
        """Check if this object is frozen."""
        return self.__data.frozen
    
    #
    # Special method
    #

    def __setattr__(self, __name: str, __value: Any) -> None:
        """Set an attribute of this object. Raises a FrozenError if this object is
        frozen."""
        if self.__data.frozen:
            raise FrozenError("cannot set attributes while object is frozen")
        object.__setattr__(self, __name, __value)
