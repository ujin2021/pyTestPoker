# Constants
suits = 'CDHS'
ranks = '23456789TJQKA'
hand_ranking = {'High card' : 0, 'One pair' : 1, 'Two pair' : 2, "Three of a kind" : 3, "Straight" : 4, "Flush" : 5, "Full house" : 6, "Four of a kind" : 7, "Straight flush" : 8}
'''
class Card : abstract class
class PKCard : imprement method value() -> return value of rank
class Deck : make list of card by input class
class Hands : find hand ranking and check who is winner. Each method return [hand_ranking_name, list_of_rank]
'''
from abc import ABCMeta, abstractmethod
import random
import sys

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards"""
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        #print("Card card type:", type(self.card)) #str

    def __repr__(self):
        return self.card

    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()

class PKCard(Card):
    """Card for Poker game : 정수를 return하는 value() method를 implementation"""
    def value(self):
        return ranks.index(self.card[0]) + 2

    def __getitem__(self, index):
        return self.card[index]

class Deck:
    def __init__(self, cls):
        """Create a deck of 'cls' card class"""
        self.deck_list = [cls(r+s) for r in ranks for s in suits]

    def shuffle(self):
        return random.shuffle(self.deck_list)

    def pop(self):
        del self.deck_list[-1]
        return self.deck_list[-1]

    def __str__(self):
        return f'{self.deck_list}'

    def __len__(self):
        return len(self.deck_list)

    def __getitem__(self, index):
        return self.deck_list[index]

class Hands:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = sorted(cards, reverse=True)

        def __eq__(self, other): return self.value() == other
        def __ne__(self, other): return self.value() != other

    def is_flush(self, cards):
        #all card have same suit
        suit_set = set()
        for i in range(5):
            suit_set.add(cards[i][1]) #card's suit set
        if (len(suit_set) == 1):
            return [x[0] for x in cards] #card rank list
        else:
            return None

    def is_straight(self, cards):
        #five cards of sequential rank
        for i in range(0, 4):
            check = [PKCard.value(card) for card in cards]
            if (check == [14, 5, 4, 3, 2]): #baby straight
                return ['Straight', cards[1][0]]
            elif (check[i] - 1 == check[i+1]): # check if rank if decreasing
                continue
            else:
                return None

        return ['Straight', cards[0][0]] #제일 큰 수를 가진 카드의 rank

    def classify_by_rank(self, cards):
        result = dict() #{rank:[suit1, suit2], ...}

        for i in range(5):
            if (cards[i][0] in result):
                temp_list = [] #initialize temp list
                if (type(result[cards[i][0]]) == list): #rank당 suit여러개
                    temp_list.extend(result[cards[i][0]])
                else:
                    temp_list.append(result[cards[i][0]]) #rank당 suit 한개
                temp_list.append(cards[i][1])
                result[cards[i][0]] = temp_list
            else:
                result[cards[i][0]] = cards[i][1]

        return result

    def find_a_kind(self, cards):
        self.cards_by_ranks = self.classify_by_rank(cards)
        rank_keys = list(self.cards_by_ranks.keys()) #list of rank
        rank_values = list(self.cards_by_ranks.values()) #list of suit

        if (len(rank_keys) == 2):  # full house or four of a kind
            if (type(rank_values[0]) == list and type(rank_values[1]) == list): #full house
                if(len(rank_values[0]) == 3):
                    temp = [rank_keys[0], rank_keys[1]]
                else:
                    temp = [rank_keys[1], rank_keys[0]]
                result = ["Full house", temp]
            else: #four of a kind
                if(type(rank_values[0]) == list):
                    temp = [rank_keys[0], rank_keys[1]]
                else:
                    temp = [rank_keys[1], rank_keys[0]]
                result = ["Four of a kind", temp]
        elif (len(rank_keys) == 3):  # three of a kind, two pair
            count = 0
            temp = []
            for i in range(3):
                if (type(rank_values[i]) == list):
                    temp.insert(0,rank_keys[i])
                    count += 1
                else:
                    temp.append(rank_keys[i])
            if (count == 1): #three of a kind
                result = ["Three of a kind", temp]
            else: #two pair
                if(ranks.index(temp[0]) < ranks.index(temp[1])): #sort pair card rank
                    tmp = temp[0]
                    temp[0] = temp[1]
                    temp[1] = tmp
                    result = ["Two pair", temp]
        elif(len(rank_keys) == 4): #one pair
            temp = []
            for i in range(4):
                if(type(rank_values[i]) == list):
                    temp.insert(0, rank_keys[i])
                else:
                    temp.append(rank_keys[i])
            result = ["One pair", temp]
        else: #len(rank_keys) == 5 -> straight or high card
            if(rank_keys == ['A', '5', '4', '3', '2']):
                result = 0 #Straight
            else:
                result = ["High card", rank_keys] #high card, return rank list

        return result

    def tell_hand_ranking(self):
        isFlush = self.is_flush(self.cards) #'None' or rank list
        isStraight = self.is_straight(self.cards) #None' or highest rank
        findAkind = self.find_a_kind(self.cards) #None' or result list
        #flush랑 pair카드 동시에 x, straight랑 pair카드 동시에 x (High card일땐 가능)
        if (type(isFlush) != list and type(isStraight) != list and type(findAkind) == list):
            return findAkind
        elif (type(isFlush) == list and type(isStraight) != list):
            return ['Flush', isFlush]
        elif (type(isFlush) == list and type(isStraight) == list):
            return ["Straight flush", isStraight[1]]
        elif (type(isFlush) != list and type(isStraight) == list):
            return ["Straight", isStraight[1]]

    def tie_break(self, other):
        card1_hand_raking = self.tell_hand_ranking() #[hand ranking name, card]
        card2_hand_ranking = other.tell_hand_ranking()

        if (hand_ranking[card1_hand_raking[0]] > hand_ranking[card2_hand_ranking[0]]):
            return True
        elif (hand_ranking[card1_hand_raking[0]] < hand_ranking[card2_hand_ranking[0]]):
            return False
        else:  # same hand_ranking
            if (hand_ranking[card1_hand_raking[0]] == 0):  # high card
                for i in range(5):
                    if (ranks.index(card1_hand_raking[1][i]) > ranks.index(card2_hand_ranking[1][i])):
                        return True
                    elif (ranks.index(card1_hand_raking[1][i]) < ranks.index(card2_hand_ranking[1][i])):
                        return False

            elif (hand_ranking[card1_hand_raking[0]] == 1):  # one pair
                if (ranks.index(card1_hand_raking[1][0]) > ranks.index(card2_hand_ranking[1][0])):
                    return True
                elif (ranks.index(card1_hand_raking[1][0]) < ranks.index(card2_hand_ranking[1][0])):
                    return False
                for i in range(1, 4):
                    if (ranks.index(card1_hand_raking[1][i]) > ranks.index(card2_hand_ranking[1][i])):
                        return True
                    elif (ranks.index(card1_hand_raking[1][i]) < ranks.index(card2_hand_ranking[1][i])):
                        return False

            elif (hand_ranking[card1_hand_raking[0]] == 2):  # two pair
                if (ranks.index(card1_hand_raking[1][0]) > ranks.index(card2_hand_ranking[1][0])):
                    return True
                elif (ranks.index(card1_hand_raking[1][0]) < ranks.index(card2_hand_ranking[1][0])):
                    return False
                else:  # first pair card same
                    if (ranks.index(card1_hand_raking[1][1]) > ranks.index(card2_hand_ranking[1][1])):
                        return True
                    elif (ranks.index(card1_hand_raking[1][1]) < ranks.index(card2_hand_ranking[1][1])):
                        return False
                    else:
                        if (ranks.index(card1_hand_raking[1][2]) > ranks.index(card2_hand_ranking[1][2])):
                            return True
                        elif (ranks.index(card1_hand_raking[1][2]) < ranks.index(card2_hand_ranking[1][2])):
                            return False

            elif (hand_ranking[card1_hand_raking[0]] == 3):  # three of a kind
                if (ranks.index(card1_hand_raking[1][0]) > ranks.index(card2_hand_ranking[1][0])):
                    return True
                elif (ranks.index(card1_hand_raking[1][0]) < ranks.index(card2_hand_ranking[1][0])):
                    return False
                else:
                    for i in range(1, 3):
                        if (ranks.index(card1_hand_raking[1][i]) > ranks.index(card2_hand_ranking[1][i])):
                            return True
                        elif (ranks.index(card1_hand_raking[1][i]) < ranks.index(card2_hand_ranking[1][i])):
                            return False

            elif (hand_ranking[card1_hand_raking[0]] == 4):  # straight
                if (ranks.index(card1_hand_raking[1]) < ranks.index(card2_hand_ranking[1])):
                    return False
                return True

            elif (hand_ranking[card1_hand_raking[0]] == 5):  # flush
                for i in range(5):
                    if (ranks.index(card1_hand_raking[1][i]) > ranks.index(card2_hand_ranking[1][i])):
                        return True
                    elif (ranks.index(card1_hand_raking[1][i]) < ranks.index(card2_hand_ranking[1][i])):
                        return False

            elif (hand_ranking[card1_hand_raking[0]] == 6):  # full house
                for i in range(2):
                    if (ranks.index(card1_hand_raking[1][i]) > ranks.index(card2_hand_ranking[1][i])):
                        return True
                    elif (ranks.index(card1_hand_raking[1][i]) < ranks.index(card2_hand_ranking[1][i])):
                        return False
                    else:
                        continue

            elif (hand_ranking[card1_hand_raking[0]] == 7):  # four of a kind
                for i in range(2):
                    if (ranks.index(card1_hand_raking[1][i]) > ranks.index(card2_hand_ranking[1][i])):
                        return True
                    elif (ranks.index(card1_hand_raking[1][i]) < ranks.index(card2_hand_ranking[1][i])):
                        return False
                    else:
                        continue

            elif (hand_ranking[card1_hand_raking[0]] == 8):  # flush straight
                if (ranks.index(card1_hand_raking[1]) < ranks.index(card2_hand_ranking[1])):
                    return False
                return True
            return None


if __name__ == '__main__':
    def test(did_pass):
        """  Print the result of a test.  """
        linenum = sys._getframe(1).f_lineno  # Get the caller's line number.
        if did_pass:
            msg = "Test at line {0} ok.".format(linenum)
        else:
            msg = ("Test at line {0} FAILED.".format(linenum))
        print(msg)

    #기본 hand_ranking 비교
    test_code = [Hands([PKCard('3D'), PKCard('5D'), PKCard('7C'), PKCard('AD'), PKCard('4D')]),
                  Hands([PKCard('KD'), PKCard('JD'), PKCard('QC'), PKCard('AD'), PKCard('TD')])]
    test(test_code[0].tie_break(test_code[1]) == False) #high card < straight => False

    test_code = [Hands([PKCard('4D'), PKCard('4C'), PKCard('4C'), PKCard('AS'), PKCard('AD')]),
                  Hands([PKCard('2D'), PKCard('3D'), PKCard('4C'), PKCard('5D'), PKCard('6D')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # full house > straight => True

    test_code = [Hands([PKCard('2D'), PKCard('8D'), PKCard('4D'), PKCard('5D'), PKCard('6D')]),
                 Hands([PKCard('2D'), PKCard('2S'), PKCard('4H'), PKCard('JD'), PKCard('6D')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # flush > one pair => True

    test_code = [Hands([PKCard('4D'), PKCard('AH'), PKCard('AC'), PKCard('AS'), PKCard('AD')]),
                 Hands([PKCard('JH'), PKCard('2S'), PKCard('JS'), PKCard('8H'), PKCard('2H')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # four of a kind > two pair => True

    test_code = [Hands([PKCard('2D'), PKCard('8D'), PKCard('4D'), PKCard('5D'), PKCard('6D')]),
                 Hands([PKCard('6H'), PKCard('5S'), PKCard('4S'), PKCard('3H'), PKCard('2H')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # flush > straight => True

    test_code = [Hands([PKCard('QC'), PKCard('QS'), PKCard('2S'), PKCard('QH'), PKCard('9H')]),
                 Hands([PKCard('4D'), PKCard('4C'), PKCard('4C'), PKCard('AS'), PKCard('AD')])]
    test(test_code[0].tie_break(test_code[1]) == False)  # three of a kind < full house => False

    #같은 hand_ranking 일 때
    test_code = [Hands([PKCard('TC'), PKCard('8S'), PKCard('7S'), PKCard('6H'), PKCard('4C')]),
                 Hands([PKCard('TD'), PKCard('8D'), PKCard('7D'), PKCard('6H'), PKCard('3D')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # high card(T-8-7-6-4) > high card(T-8-7-6-3) => True

    test_code = [Hands([PKCard('TS'), PKCard('8S'), PKCard('TH'), PKCard('7H'), PKCard('4C')]),
                 Hands([PKCard('2D'), PKCard('2S'), PKCard('4H'), PKCard('JD'), PKCard('6D')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # one pair(T) > one pair(2) => True

    test_code = [Hands([PKCard('2S'), PKCard('8S'), PKCard('2H'), PKCard('7H'), PKCard('4C')]),
                 Hands([PKCard('2D'), PKCard('2C'), PKCard('4H'), PKCard('JD'), PKCard('6D')])]
    test(test_code[0].tie_break(test_code[1]) == False)  # one pair(2-8) < one pair(2-J) => False

    test_code = [Hands([PKCard('5C'), PKCard('5S'), PKCard('4S'), PKCard('4H'), PKCard('TH')]),
                 Hands([PKCard('5C'), PKCard('5S'), PKCard('3C'), PKCard('3D'), PKCard('QH')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # two pair(5-4) > two pair(5-3) => True

    test_code = [Hands([PKCard('KD'), PKCard('KS'), PKCard('7D'), PKCard('7H'), PKCard('8H')]),
                 Hands([PKCard('KC'), PKCard('KS'), PKCard('7S'), PKCard('7H'), PKCard('6H')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # two pair(K-7-8) > two pair(K-7-6) => True

    test_code = [Hands([PKCard('3D'), PKCard('3S'), PKCard('3C'), PKCard('JC'), PKCard('7H')]),
                 Hands([PKCard('3D'), PKCard('3S'), PKCard('3C'), PKCard('JS'), PKCard('5H')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # three of a kind(3-j-7) > three of a kind(3-j-5) => True

    test_code = [Hands([PKCard('AH'), PKCard('5S'), PKCard('4S'), PKCard('3H'), PKCard('2H')]),
                 Hands([PKCard('6H'), PKCard('5S'), PKCard('4S'), PKCard('3H'), PKCard('2H')])]
    test(test_code[0].tie_break(test_code[1]) == False)  # straight(5) < straight(6) => False

    test_code = [Hands([PKCard('KD'), PKCard('JD'), PKCard('9D'), PKCard('6D'), PKCard('4D')]),
                 Hands([PKCard('QC'), PKCard('JC'), PKCard('7C'), PKCard('6C'), PKCard('5C')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # flush(K) < flush(Q) => True

    test_code = [Hands([PKCard('JH'), PKCard('TH'), PKCard('8H'), PKCard('4H'), PKCard('3H')]),
                 Hands([PKCard('JC'), PKCard('TC'), PKCard('8C'), PKCard('4C'), PKCard('2C')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # flush(j-t-8-4-3) > flush(j-t-8-4-2) => True

    test_code = [Hands([PKCard('8S'), PKCard('8D'), PKCard('8H'), PKCard('7D'), PKCard('7C')]),
                 Hands([PKCard('4D'), PKCard('4C'), PKCard('4S'), PKCard('9D'), PKCard('9C')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # full house(8) > full house(4) => True

    test_code = [Hands([PKCard('8S'), PKCard('8D'), PKCard('8H'), PKCard('7D'), PKCard('7C')]),
                 Hands([PKCard('8D'), PKCard('8C'), PKCard('8S'), PKCard('9D'), PKCard('9C')])]
    test(test_code[0].tie_break(test_code[1]) == False)  # full house(8-7) < full house(8-9) => False

    test_code = [Hands([PKCard('5C'), PKCard('2D'), PKCard('5D'), PKCard('5H'), PKCard('5S')]),
                 Hands([PKCard('4D'), PKCard('6H'), PKCard('6C'), PKCard('6S'), PKCard('6D')])]
    test(test_code[0].tie_break(test_code[1]) == False)  # four of a kind(5) < four of a kind(6) => False

    test_code = [Hands([PKCard('5C'), PKCard('2D'), PKCard('5D'), PKCard('5H'), PKCard('5S')]),
                 Hands([PKCard('4D'), PKCard('5H'), PKCard('5C'), PKCard('5S'), PKCard('5D')])]
    test(test_code[0].tie_break(test_code[1]) == False)  # four of a kind(5-2) < four of a kind(5-4) => False

    test_code = [Hands([PKCard('TH'), PKCard('JH'), PKCard('KH'), PKCard('AH'), PKCard('QH')]),
                 Hands([PKCard('5S'), PKCard('2S'), PKCard('AS'), PKCard('4S'), PKCard('3S')])]
    test(test_code[0].tie_break(test_code[1]) == True)  # straight flush(A) > straight flush(5) => True

