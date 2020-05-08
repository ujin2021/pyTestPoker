import pytest
from pokerOop import *

def test_PKCard_init():
    card = PKCard('AC')
    assert card[0] == 'A' and card[1] == 'C'

def test_PKCard_init_exception():
    for face in ['10S', 'BD', 'TA']:
        with pytest.raises(ValueError):
            PKCard(face)

def test_PKCard_repr():
    assert repr(PKCard('AC')) == 'AC'

@pytest.fixture
def all_faces():
    return [r+s for r in ranks for s in suits]

# def test_PKCard_value(all_faces):
#     for face in all_faces:
#         card, expected = PKCard(face), PKCard.value()

@pytest.fixture
def c9C():
    return PKCard('9C').value()

@pytest.fixture
def c9H():
    return PKCard('9H').value()

@pytest.fixture
def cTH():
    return PKCard('TH').value()

def test_PKCard_comp(c9C, c9H, cTH): # 위 function에서 return 된 값들이 parameter로 들어온다.
    assert c9C == c9C and c9C == c9H
    assert c9H < cTH and c9C < cTH
    assert c9C <= c9H <= cTH
    assert cTH > c9H and cTH > c9C
    # assert cTH >= c9H > c9C
    assert c9C != cTH and c9H != cTH

def test_PKCard_sort(all_faces):
    all_cards = [PKCard(c) for c in all_faces]
    import random
    random.shuffle(all_cards)
    all_cards.sort()
    assert {c.value() for c in all_cards} == {i+2 for s in suits for i in range(len(ranks))}