import unittest

from freezable_mixin.freezable import _FreezableData, Freezable, FrozenError


class TestFreezableData(unittest.TestCase):
    
    def test_freezable_data(self):
        
        # test initialization
        data = _FreezableData()
        self.assertFalse(data.frozen)
        
        # test that setting attrs is normal
        data.frozen = True
        self.assertTrue(data.frozen)
        data.frozen = False
        self.assertFalse(data.frozen)


class TestFrozenError(unittest.TestCase):
    
    def test_creation(self):
        
        err = FrozenError()
        self.assertTupleEqual(err.args, ())
        
        err = FrozenError('message')
        self.assertTupleEqual(err.args, ('message', ))
        
        err = FrozenError('message1', 'message2')
        self.assertTupleEqual(err.args, ('message1', 'message2'))



