from freezable_mixin.freezable import _FreezableData


def test_freezable_data():
    
    # test initialization
    data = _FreezableData()
    assert data.frozen is False
    
    # test that setting attrs is normal
    data.frozen = True
    assert data.frozen is True
    data.frozen = False
    assert data.frozen is False
    

