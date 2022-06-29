import unittest

from freezable_mixin.freezable import _FreezableData, Freezable, FrozenError


class TestFreezableData(unittest.TestCase):
    
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
    
    def test_init(self):
        "test initialization of FrozenError"
        
        err = FrozenError()
        self.assertTupleEqual(err.args, ())
        
        err = FrozenError('message')
        self.assertTupleEqual(err.args, ('message', ))
        
        err = FrozenError('message1', 'message2')
        self.assertTupleEqual(err.args, ('message1', 'message2'))


class TestFreezable(unittest.TestCase):
    
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
