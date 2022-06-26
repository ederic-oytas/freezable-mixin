import unittest

from freezable_mixin.freezable import _FreezableData


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
        

