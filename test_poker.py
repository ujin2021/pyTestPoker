import pytest
from pokerOop import *
# pytest -v test_poker
# pytest -v -s test_poker (-s : 캡쳐하지말고 다 보여줘라)
# pytest -v --cov=. 했을 때 100%가 되도록!

"""
def test_is_straight(faces, expected) ---ok
def test_is_flush(faces,expected) ---ok
def test_is_find_a_kind(faces, expected) ---ok
def test_is_find_a_kind_None(faces, expected) ---ok
def test_eval(faces, expected) ---ok
def test_who_wins() ---ok
"""

# Test Data
non_flush_suit = 'CHSDS'
flush_suit = 'SSSSS'
test_cases = { # dictionary
    # Ordering : high-to-low poker hand rankings
    # hight ranking to low ranking
    # high card to low card for tie-breaking in the same ranking
    Ranking.STRAIGHT_FLUSH: (
        tuple(zip('AKQJT', flush_suit)),
        tuple(zip('KQJT9', flush_suit)),
        tuple(zip('5432A', flush_suit)),
    ),
    Ranking.FOUR_OF_A_KIND: (
        tuple(zip('TTTTQ', non_flush_suit)),
        tuple(zip('9999A', non_flush_suit)),
        tuple(zip('99998', non_flush_suit)),
        tuple(zip('79999', non_flush_suit)),
        tuple(zip('88688', non_flush_suit)),
        tuple(zip('25555', non_flush_suit)),
    ),
    Ranking.FULL_HOUSE: (
        tuple(zip('88877', non_flush_suit)),
        tuple(zip('88866', non_flush_suit)),
        tuple(zip('55888', non_flush_suit)),
        tuple(zip('44555', non_flush_suit)),
        tuple(zip('22299', non_flush_suit)),
        tuple(zip('22233', non_flush_suit)),
    ),
    Ranking.FLUSH: (
        tuple(zip('AJT98', flush_suit)),
        tuple(zip('AJT97', flush_suit)),
        tuple(zip('AJT85', flush_suit)),
        tuple(zip('AJ987', flush_suit)),
        tuple(zip('J9876', flush_suit)),
    ),
    Ranking.STRAIGHT: (
        tuple(zip('AKQJT', non_flush_suit)),
        tuple(zip('KQJT9', non_flush_suit)),
        tuple(zip('5432A', non_flush_suit)),
    ),
    Ranking.THREE_OF_A_KIND: (
        tuple(zip('888A9', non_flush_suit)),
        tuple(zip('888A7', non_flush_suit)),
        tuple(zip('77765', non_flush_suit)),
        tuple(zip('32555', non_flush_suit)),
    ),
    Ranking.TWO_PAIRS: (
        tuple(zip('AA998', non_flush_suit)),
        tuple(zip('AA997', non_flush_suit)),
        tuple(zip('AA778', non_flush_suit)),
        tuple(zip('JJTTK', non_flush_suit)),
        tuple(zip('66552', non_flush_suit)),
        tuple(zip('44553', non_flush_suit)),
        tuple(zip('32244', non_flush_suit)),
    ),
    Ranking.ONE_PAIR: (
        tuple(zip('88AT9', non_flush_suit)),
        tuple(zip('88AT7', non_flush_suit)),
        tuple(zip('77AKQ', non_flush_suit)),
        tuple(zip('65733', non_flush_suit)),
        tuple(zip('23542', non_flush_suit)),
    ),
    Ranking.HIGH_CARD: (
        tuple(zip('AJT98', non_flush_suit)),
        tuple(zip('AJT97', non_flush_suit)),
        tuple(zip('QJT97', non_flush_suit)),
    ),
}


def cases(*rankings):
    """get the test cases for rankings. all rankings if empty rankings"""
    if not rankings: # empty rankings
        rankings = test_cases.keys()
    return [([r+s for r, s in case], ranking) for ranking in rankings for case in test_cases[ranking]] 
    #ranking이 여러개라면(==rankings), rankings에서 ranking을 하나씩 뽑아서 해당되는 test_case들을 return한다.

def test_illegalCard(): # rank가 1인 카드를 넣었을 때
    with pytest.raises(ValueError):
        Hands([PKCard('1S'), PKCard('2S'), PKCard('3H'), PKCard('4H'), PKCard('5C')])

def test_notFiveCards(): # 5장보다 적은 카드를 넣었을 때
    with pytest.raises(ValueError):
        Hands([PKCard('2S'), PKCard('3H'), PKCard('4H'), PKCard('5C')])

def test_Deck():
    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle()
    c = deck[0]
    print('A deck of', c.__class__.__name__)
    print(deck)
    # testing __getitem__ method
    print(deck[-5:])

    while len(deck) >= 10:
        my_hand = []
        your_hand = []
        for i in range(5):
            for hand in (my_hand, your_hand):
                card = deck.pop()
                hand.append(card)
        my_hand.sort(reverse=True)
        your_hand.sort(reverse=True)
        print(my_hand, '>', your_hand, '?', my_hand > your_hand)


@pytest.mark.parametrize("faces, expected", cases(Ranking.STRAIGHT))
def test_is_straight(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.is_straight()
    if(result[1] == '5'): # [A, 5, 4, 3, 2]인 경우 => sort시 A=14로 인식하므로 리스트를 다시정렬해줌.
        for i in range(len(hand.cards)-1):
            temp = hand.cards[i + 1]
            hand.cards[i + 1] = hand.cards[i]
            hand.cards[i] = temp
    assert Ranking[result[0]] == expected # straight이면 ['STRAIGHT', 'hightest_card']를 반환하므로
    #assert hand.cards == hand_org

@pytest.mark.parametrize("faces, expected", cases(Ranking.FLUSH))
def test_is_flush(faces,expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.is_flush()
    assert result is not None # flush가 아닐경우 None반환, flush일 경우 list반환
    assert hand.cards == hand_org

@pytest.mark.parametrize("faces, expected", cases(Ranking.FOUR_OF_A_KIND, Ranking.THREE_OF_A_KIND, Ranking.TWO_PAIRS, Ranking.ONE_PAIR))
def test_is_find_a_kind(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    hand = Hands([PKCard(c)for c in faces])
    result = hand.find_a_kind()
    assert Ranking[result[0]] == expected
    #assert hand.cards == hand_org # return을 다른방식으로 해줬기 때문에 검사 안함.

@pytest.mark.parametrize("faces, expected", cases(Ranking.HIGH_CARD))
def test_is_find_a_kind_None(faces, expected):
    hand_org = [PKCard(c) for c in faces]
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.find_a_kind()
    assert Ranking[result[0]] == expected
    assert hand.cards == hand_org # high card찾을 때

@pytest.mark.parametrize("faces, expected", cases())
def test_eval(faces, expected):
    random.shuffle(faces)
    hand = Hands([PKCard(c) for c in faces])
    result = hand.tell_hand_ranking()
    assert Ranking[result[0]] == expected

def test_tie_break():
    hand_cases = [Hands([PKCard(i) for i in faces]) for faces, ranking in cases()] # 전체 test_case
    hand_cases_test = [Hands([PKCard(i) for i in faces]) for faces, ranking in cases()] # 전체 test_case
    count = 0
    count_reversed = 0
    for i in range(len(hand_cases_test)-1): # test list끼리 tie break 시킨다.
        result = hand_cases_test[i].tie_break(hand_cases_test[i+1])
        if(result == True):
            count += 1
    for i in range(len(hand_cases_test)-1): # 반대로도 체크
        result = hand_cases_test[i+1].tie_break(hand_cases_test[i])
        if(result == False):
            count_reversed += 1
    assert count == count_reversed # 비교한 갯수랑 같으면 통과
    print('\nHigh to low order:')
    for i, hand in enumerate(hand_cases):
        print(i, hand.cards, hand.tell_hand_ranking()[1], Ranking[hand.tell_hand_ranking()[0]])