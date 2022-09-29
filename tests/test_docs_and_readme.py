"""Tests for code snippets found in the README.md and the docs."""


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
