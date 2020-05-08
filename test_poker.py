import pytest
from poker import *

def test_PKCard_init_exception():
    for face in ['10S', 'BD', 'TA']:
        with pytest.raises(ValueError):
            PKCard(face)

def test_PKCard_repr():
    assert repr(PKCard('AC')) == 'AC'

