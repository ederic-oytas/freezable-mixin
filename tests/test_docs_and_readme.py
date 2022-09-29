"""Tests for code snippets found in the README.md and the docs."""

import pytest

from freezable import FrozenError
from freezable.freezable import Freezable


def test_readme_and_index_example():
    """Test the example found in docs/index.md and README.md"""
    
    ######################################
    
    from freezable import Freezable, FrozenError, enabled_when_unfrozen

    class FreezableStack(Freezable):
        
        def __init__(self):
            self._data = []
        
        @enabled_when_unfrozen
        def push(self, x):
            self._data.append(x)

        def top(self):
            return self._data[-1] if self._data else None

    stk = FreezableStack()
    assert stk.top() is None

    stk.push(1)
    assert stk.top() == 1
    stk.push(2)
    assert stk.top() == 2

    stk.freeze()

    try:
        stk.push(3)  # error because stk is frozen
    except FrozenError:
        pass

    assert stk.top() == 2  # operation did not proceed

    stk.unfreeze()
    stk.push(3)
    assert stk.top() == 3
    
    ######################################


class TestUserGuide:
    """Test examples found in docs/user"""
    
    def test_section_the_freezable_class(self):
        """Test the example in this section"""
        
        ######################################
        
        from freezable import Freezable

        class SomeFreezable(Freezable):
            ...
        
        ######################################
        
        assert issubclass(SomeFreezable, Freezable)

    def test_section_freeze_unfreeze_and_is_frozen(self):
        """Test the example in this section"""
        
        ######################################
        
        from freezable import Freezable

        class SomeFreezable(Freezable):
            ...

        obj = SomeFreezable()

        assert not obj.is_frozen()

        obj.freeze()
        assert obj.is_frozen()

        obj.unfreeze()
        assert not obj.is_frozen()
        
        ######################################
        
    def test_section_freezing_disables__example_1(self):
        """Test the two examples in this section"""
        
        # Example 1 continues from the example in previous section
        ######################################
        from freezable import Freezable

        class SomeFreezable(Freezable):
            ...

        obj = SomeFreezable()

        assert not obj.is_frozen()

        obj.freeze()
        assert obj.is_frozen()

        obj.unfreeze()
        assert not obj.is_frozen()
        
        ######################################

        # Example 1
        ######################################

        obj = SomeFreezable()
        obj.freeze()

        # Both of these operations will raise a FrozenError:
        #obj.attr = 5
        #del obj.attr
        
        ######################################
        
        # We test those two statements
        with pytest.raises(FrozenError):
            obj.attr = 5
        with pytest.raises(FrozenError):
            del obj.attr
        
    def test_section_freezing_disables_example_2(self):
        """Test the code of overriding the special methods in the class body"""
        
        class SomeFreezable(Freezable):
            __setattr__ = object.__setattr__
            __delattr__ = object.__delattr__
        
        obj = SomeFreezable()
        obj.freeze()
        
        # These two statements should not raise any error        
        obj.a = 5
        del obj.a
        
    def test_section_enabled_when_frozen(self):
        """Test the example in this section"""
        
        ######################################
        from freezable import Freezable, enabled_when_unfrozen

        class SomeFreezable(Freezable):
            @enabled_when_unfrozen
            def some_mutating_method(self):
                ...

        frz = SomeFreezable()

        assert not frz.is_frozen()
        frz.some_mutating_method()  # Does not raise an error

        frz.freeze()
        assert frz.is_frozen()
        #frz.some_mutating_method()  # Raises `FrozenError`
        #######################################

        # test the last statement
        with pytest.raises(FrozenError):
            frz.some_mutating_method()
