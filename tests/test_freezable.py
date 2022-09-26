import types
from unittest.mock import MagicMock

import pytest

from freezable import Freezable, FrozenError, enabled_when_unfrozen


class TestFreezable:
    "test Freezable"
    
    def test_defines_no_init(self):
        "test if Freezable defines no __init__"
        assert Freezable.__init__ is object.__init__
    
    def test_freezing(self):
        "test freezing and unfreezing with no subsuming involved"
        frz = Freezable()
        
        assert not frz.is_frozen()
        
        for _ in range(5):
            frz.freeze()
            assert frz.is_frozen()
            
            frz.unfreeze()
            assert not frz.is_frozen()
    
    def test_setattr_and_delattr(self):
        """test __setattr__ and __delattr__"""
        # both methods should raise FrozenError when frozen
        frz = Freezable()
        
        frz.__setattr__('a', 10)
        frz.__setattr__('a', 15)
        frz.__setattr__('b', 20)
        frz.__delattr__('b')
        
        for _ in range(5):
        
            frz.freeze()
            
            with pytest.raises(FrozenError): frz.__setattr__('a', 30)
            with pytest.raises(FrozenError): frz.__setattr__('b', 50)
            with pytest.raises(FrozenError): frz.__delattr__('a')
            with pytest.raises(FrozenError): frz.__delattr__('b')
            with pytest.raises(FrozenError): frz.__delattr__('z')
            
            frz.unfreeze()
            frz.__setattr__('a', 10)
            frz.__setattr__('a', 15)
            frz.__setattr__('b', 20)
            frz.__delattr__('b')
        

class TestDisabledWhenFrozen:
    "test enabled_when_unfrozen()"
    
    def test_disabling_when_frozen(self):
        "test disabling a method when the object is frozen"
        
        class Sub(Freezable):            
            @enabled_when_unfrozen
            def some_method(self):
                return 10
        
        frz = Sub()
        
        assert not frz.is_frozen()
        assert frz.some_method() == 10
        
        for _ in range(5):
            frz.freeze()
            assert frz.is_frozen()
            with pytest.raises(FrozenError):
                frz.some_method()
            
            frz.unfreeze()
            assert not frz.is_frozen()
            assert frz.some_method() == 10
    
    def test_calling_when_unfrozen(self):
        "test if the given method is called when unfrozen"
        
        class SomeFreezable(Freezable):
            pass
        
        # Test calls expecting a return value
        
        # args, kwargs, return_value
        cases = [
            ((Freezable(),),                {},               object()),
            ((SomeFreezable(),),            {},               object()),
            ((SomeFreezable(), 1, 2, 3, 4), {},               object()),
            ((SomeFreezable(), 1, 2, 3, 4), {'a': 2, 'b': 5}, object()),
        ]
        
        for args, kwargs, return_value in cases:
            m = MagicMock()
            m.return_value = return_value
            w = enabled_when_unfrozen(m)
            assert w(*args, **kwargs) == return_value
            m.assert_called_once_with(*args, **kwargs)
        
        # Check if a keyword argument named 'self' is also accepted
        
        def return_given(*args, **kwargs):
            return args, kwargs
        
        w = enabled_when_unfrozen(return_given)
        frz = SomeFreezable()
        self_arg = object()
        assert w(frz, self=self_arg) == ((frz, ), {'self': self_arg})
        
        
        # Test calls expecting an error to be raised
        
        class CustomError(RuntimeError):
            pass
        
        cases = [
            ((Freezable(),),                {},               CustomError),
            ((SomeFreezable(),),            {},               CustomError),
            ((SomeFreezable(), 1, 2, 3, 4), {},               CustomError),
            ((SomeFreezable(), 1, 2, 3, 4), {'a': 2, 'b': 5}, CustomError),
        ]
        for args, kwargs, exception_type in cases:
            m = MagicMock()
            m.side_effect = exception_type
            w = enabled_when_unfrozen(m)
            with pytest.raises(exception_type):
                w(*args, **kwargs)
            m.assert_called_once_with(*args, **kwargs)
    
    def test_is_instance_of_function_type(self):
        "test if the wrapped method is an instance of the user function type"
        # This test is required because only FunctionType objects (user-defined functions
        # using `def`) are transformed into instance methods in Python classes.
        # See the "Instance methods" subsection at
        # https://docs.python.org/3.6/reference/datamodel.html#the-standard-type-hierarchy
        # for more information.
        
        class SomeClass:
            def some_inst_method(self):
                pass
        
        some_lambda = lambda self: None
        
        class SomeCallableType:
            def __call__(self, *args, **kwargs):
                pass
        
        cases = [SomeClass.some_inst_method, some_lambda, SomeCallableType()]
        
        for callable_ in cases:
            w = enabled_when_unfrozen(callable_)
            assert isinstance(w, types.FunctionType)
            
    def test_wrapping(self):
        "test if the decorator correctly wraps the method"
        
        class SomeClass(Freezable):
            
            def unwrapped(self) -> int:
                "Sample documentation."
                return 10
        
        unwrapped = SomeClass.unwrapped
        unwrapped.__dict__['a'] = 5
        wrapped = enabled_when_unfrozen(unwrapped)
        
        assert wrapped.__module__      == unwrapped.__module__
        assert wrapped.__name__        == unwrapped.__name__
        assert wrapped.__qualname__    == unwrapped.__qualname__
        assert wrapped.__annotations__ == unwrapped.__annotations__
        assert wrapped.__doc__         == unwrapped.__doc__
        
        # wrapped.__dict__ without __wrapped__ item should equal
        # unwrapped.__dict__
        copy = dict(wrapped.__dict__)
        del copy['__wrapped__']
        assert copy                    == unwrapped.__dict__
