import unittest

from freezable.freezable import Freezable, FrozenError, disabled_when_frozen


class TestFrozenError(unittest.TestCase):
    "test FrozenError"
    
    def test_init(self):
        "test initialization of FrozenError"
        
        err = FrozenError()
        self.assertTupleEqual(err.args, ())
        
        err = FrozenError('message')
        self.assertTupleEqual(err.args, ('message', ))
        
        err = FrozenError('message1', 'message2')
        self.assertTupleEqual(err.args, ('message1', 'message2'))


class TestFreezable(unittest.TestCase):
    "test Freezable"
    
    def test_init(self):
        "test initialization"
        frz = Freezable()
        self.assertFalse(frz._Freezable__frozen)

    def test_freezing(self):
        "test freezing methods: .freeze(), .unfreeze(), and ._is_frozen()"
        frz = Freezable()
        
        self.assertFalse(frz.is_frozen())
        
        for _ in range(5):
            frz.freeze()
            self.assertTrue(frz.is_frozen())
            
            frz.unfreeze()
            self.assertFalse(frz.is_frozen())


class TestDisabledWhenFrozen(unittest.TestCase):
    "test disabled_when_frozen()"
    
    def test_error_raising(self):
        
        class Sub(Freezable):            
            @disabled_when_frozen
            def some_method(self):
                return 10
        
        frz = Sub()
        
        self.assertFalse(frz.is_frozen())
        self.assertEqual(frz.some_method(), 10)
        
        for _ in range(5):
            frz.freeze()
            self.assertTrue(frz.is_frozen())
            self.assertRaises(FrozenError, frz.some_method)
            
            frz.unfreeze()
            self.assertFalse(frz.is_frozen())
            self.assertEqual(frz.some_method(), 10)
            
    def test_wrapping(self):
        "test if the decorator correctly wraps the method"
        
        class SomeClass(Freezable):
            
            def unwrapped(self) -> int:
                "Sample documentation."
                return 10
        
        unwrapped = SomeClass.unwrapped
        unwrapped.__dict__['a'] = 5
        wrapped = disabled_when_frozen(unwrapped)
        
        self.assertEqual(wrapped.__module__,      unwrapped.__module__)
        self.assertEqual(wrapped.__name__,        unwrapped.__name__)
        self.assertEqual(wrapped.__qualname__,    unwrapped.__qualname__)
        self.assertEqual(wrapped.__annotations__, unwrapped.__annotations__)
        self.assertEqual(wrapped.__doc__,         unwrapped.__doc__)
        self.assertDictEqual(wrapped.__dict__,    wrapped.__dict__)
