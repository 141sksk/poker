from enum import Enum
import random

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
