from enum import Enum
import random
import collections

class Suit(Enum):
    SPADE = 0
    CLUB = 1
    DIAMOND = 2
    HEART = 3

    def __repr__(self):
        return 'スペード' if self == Suit.SPADE \
            else 'クラブ' if self == Suit.CLUB \
            else 'ダイヤ' if self == Suit.DIAMOND \
            else 'ハート' 

    def __str__(self):
        return self.__repr__()


class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __repr__(self):
        return 'A' if self == Rank.ACE \
            else 'J' if self == Rank.JACK \
            else 'Q' if self == Rank.QUEEN \
            else 'K' if self == Rank.KING \
            else str(self.value)
    
    def __str__(self):
        return self.__repr__()

    def __gt__(self, other):
        return self.value + 13 > other.value if self.value == 1 \
            else self.value > other.value

    def __sub__(self, other):
        return self.value - other.value

class Card:

    def __init__(self, rank, suit):
        if not isinstance(rank, Rank):
            raise TypeError(
                'rank argument error. expected type: Rank, actual: {}'.format(type(rank)))
        if not isinstance(suit, Suit):
            raise TypeError(
                'suit argument error. expected type: Suit, actual: {}'.format(type(suit)))
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return '{}{}'.format(self.suit, self.rank)
    
    def __str__(self):
        return self.__repr__()
    
    def equals_as_suit(self, other):
        return self.suit == other.suit

    def equals_as_rank(self, other):
        return self.rank == other.rank

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __gt__(self, other):
        return self.rank > other.rank


class InvalidOperationError(Exception):
    pass

class Deck:

    def __init__(self):
        self.cards = [Card(r, s) for s in Suit for r in Rank]
    
    def __len__(self):
        return len(self.cards)
    
    def is_empty(self):
        return len(self) == 0
    
    def draw(self):
        if len(self) == 0:
            raise InvalidOperationError('the deck is already empty.')
        c = self.cards[0]
        self.cards = self.cards[1:]
        return c
    
    def shuffle(self):
        random.shuffle(self.cards)

class PokerHand(Enum):
    NO_PAIR = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_CARD = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_CARD = 7
    STRAIGHT_FLUSH = 8
    ROYAL_STRAIGHT_FLUSH = 9

class PokerPlayer:

    def __init__(self):
        self.pokerplayer = []
    
    def append(self, card):
        if not isinstance(card, Card):
            raise TypeError(
                'card argument error. expected type: Card, actual: {}'.format(type(card)))
        if len(self) < 5:
            self.pokerplayer.append(card)
        else:
            raise InvalidOperationError('You have already five cards.')

    def discard(self, indices):
        if (not isinstance(indices, list)) or any(map(lambda x: not isinstance(x, int), indices)):
            raise TypeError(
                'index argument error. expected type: [int]')
        if any(map(lambda x: not 0 <= x <= 4, indices)):
            raise InvalidOperationError('index parameter must be 0 <= indices <= 4.')
        self.pokerplayer = [c for i, c in enumerate(self.pokerplayer) if i not in indices]

    def evaluate(self):
        rk_ls = [c.rank for c in self.pokerplayer]
        s = set(rk_ls)
        t = set([c.suit for c in self.pokerplayer])
        c = collections.Counter(rk_ls)
        return PokerHand.ONE_PAIR if len(s) == 4 \
            else PokerHand.TWO_PAIR if len(s) == 3 and 2 in c.values() \
            else PokerHand.THREE_CARD if len(s) == 3 and 3 in c.values() \
            else PokerHand.FOUR_CARD if len(s) == 2 and 4 in c.values() \
            else PokerHand.FULL_HOUSE if len(s) == 2 and 3 in c.values() \
            else PokerHand.ROYAL_STRAIGHT_FLUSH if len(t) == 1 and ((Rank.ACE in s) and (Rank.TEN in s) and (Rank.JACK in s) and (Rank.QUEEN in s) and (Rank.KING in s)) \
            else PokerHand.STRAIGHT_FLUSH if (len(t) == 1 and (max(rk_ls) - min(rk_ls) == 4)) \
            else PokerHand.STRAIGHT_FLUSH if (len(t) == 1 and ((Rank.ACE in s) and (Rank.TWO in s) and (Rank.THREE in s) and (Rank.FOUR in s) and (Rank.FIVE in s))) \
            else PokerHand.FLUSH if len(t) == 1 and max(rk_ls) - min(rk_ls) != 4 \
            else PokerHand.STRAIGHT if len(s) == 5 and (max(rk_ls) - min(rk_ls) == 4) \
            else PokerHand.STRAIGHT if len(s) == 5 and (Rank.ACE in s) and (Rank.TWO in s) and (Rank.THREE in s) and (Rank.FOUR in s) and (Rank.FIVE in s) \
            else PokerHand.STRAIGHT if len(s) == 5 and (Rank.ACE in s) and (Rank.TEN in s) and (Rank.JACK in s) and (Rank.QUEEN in s) and (Rank.KING in s) \
            else PokerHand.NO_PAIR

    def __len__(self):
        return len(self.pokerplayer)


