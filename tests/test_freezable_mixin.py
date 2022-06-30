import unittest

from freezable_mixin.freezable import _FreezableData, Freezable, FrozenError, disabled_when_frozen


class TestFreezableData(unittest.TestCase):
    "test _FreezableData"
    
    def test_freezable_data(self):
        "test initialization and setting"
        
        # test initialization
        data = _FreezableData()
        self.assertFalse(data.frozen)
        
        # test that setting attrs is normal
        data.frozen = True
        self.assertTrue(data.frozen)
        data.frozen = False
        self.assertFalse(data.frozen)


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
        data = frz._Freezable__data
        
        self.assertIsInstance(data, _FreezableData)

    def test_freezing(self):
        "test freezing methods: .freeze(), .unfreeze(), and ._is_frozen()"
        frz = Freezable()
        data = frz._Freezable__data
        
        self.assertFalse(data.frozen)
        self.assertFalse(frz._is_frozen())
        
        for _ in range(5):
            frz._freeze()
            self.assertTrue(data.frozen)
            self.assertTrue(frz._is_frozen())
            
            frz._unfreeze()
            self.assertFalse(data.frozen)
            self.assertFalse(frz._is_frozen())


class TestDisabledWhenFrozen(unittest.TestCase):
    "test disabled_when_frozen()"
    
    def test_error_raising(self):
        
        class Sub(Freezable):            
            @disabled_when_frozen
            def some_method(self):
                return 10
        
        frz = Sub()
        
        self.assertFalse(frz._is_frozen())
        self.assertEqual(frz.some_method(), 10)
        
        for _ in range(5):
            frz._freeze()
            self.assertTrue(frz._is_frozen())
            self.assertRaisesRegexp(
                FrozenError, "cannot call method 'some_method' while object is "
                            "frozen",
                frz.some_method,
            )
            
            frz._unfreeze()
            self.assertFalse(frz._is_frozen())
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
