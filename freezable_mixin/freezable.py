

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
        
        self._Freezable__data: _FreezableData
        object.__setattr__(self, '_Freezable__data', _FreezableData())
        # Data for the Freezable mixin. This attribute is considered to be
        # private. The name is already mangled so that the type checker will
        # be okay with functions outside of the class accessing this attribute.
    
    #
    # Freezing Methods
    #
    
    def _freeze(self) -> None:
        """Freeze this object. All methods/operations that could mutate this
        object are disabled."""
        self._Freezable__data.frozen = True

    def _unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that could mutate this
        object are re-enabled."""
        self._Freezable__data.frozen = False

    def _is_frozen(self) -> bool:
        """Check if this object is frozen."""
        return self._Freezable__data.frozen
