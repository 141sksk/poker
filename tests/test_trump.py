import unittest
from models.trump import Card, Rank, Suit, Deck, InvalidOperationError


class TestCard(unittest.TestCase):
    """test class of models.trump.Card
    """

    def test_card_constructor_success(self):
        """test constructor of Card. success pattern.
        """
        Card(Rank.ACE, Suit.SPADE)
        self.assertTrue(True)

    def test_card_constructor_fail(self):
        '''test constructor of Card. fail pattern.
        '''
        with self.assertRaises(TypeError):
            Card(Suit.SPADE, Rank.TWO)
    
    def test_card_to_string(self):
        c = Card(suit=Suit.SPADE, rank=Rank.TWO)
        self.assertEqual(str(c), 'スペード2')
        c = Card(suit=Suit.HEART, rank=Rank.KING)
        self.assertEqual(str(c), 'ハートK')
        c = Card(suit=Suit.CLUB, rank=Rank.ACE)
        self.assertEqual(str(c), 'クラブA')
        c = Card(suit=Suit.DIAMOND, rank=Rank.JACK)
        self.assertEqual(str(c), 'ダイヤJ')

    def test_card_equals(self):
        c1 = Card(suit=Suit.SPADE, rank=Rank.ACE)
        c2 = Card(suit=Suit.SPADE, rank=Rank.ACE)
        self.assertTrue(c1 == c2)
        c3 = Card(suit=Suit.HEART, rank=Rank.FIVE)
        self.assertFalse(c1 == c3)
    
    def test_card_equals_as_suit(self):
        c1 = Card(suit=Suit.HEART, rank=Rank.ACE)
        c2 = Card(suit=Suit.HEART, rank=Rank.EIGHT)
        self.assertTrue(c1.equals_as_suit(c2))
        c3 = Card(suit=Suit.SPADE, rank=Rank.FIVE)
        self.assertFalse(c1.equals_as_suit(c3))
    
    def test_card_equals_as_rank(self):
        c1 = Card(suit=Suit.HEART, rank=Rank.TEN)
        c2 = Card(suit=Suit.CLUB, rank=Rank.TEN)
        self.assertTrue(c1.equals_as_rank(c2))
        c3 = Card(suit=Suit.SPADE, rank=Rank.KING)
        self.assertFalse(c1.equals_as_rank(c3))

    def test_card_great(self):
        c1 = Card(suit=Suit.DIAMOND, rank=Rank.QUEEN)
        c2 = Card(suit=Suit.SPADE, rank=Rank.TEN)
        self.assertTrue(c1 > c2)
        c3 = Card(suit=Suit.HEART, rank=Rank.ACE)
        self.assertTrue(c3 > c2)

        
class TestDeck(unittest.TestCase):
    '''test class of trump card deck
    '''

    def test_deck_constructor(self):
        deck = Deck()
        self.assertEqual(52, len(deck))
    
    def test_deck_draw(self):
        deck = Deck()
        c = deck.draw()
        self.assertTrue(isinstance(c, Card))
        self.assertEqual(51, len(deck))

    def test_draw_empty_deck(self):
        deck = Deck()
        for _ in range(52):
            deck.draw()
        with self.assertRaises(InvalidOperationError):
            deck.draw()
    
    def test_shuffle_deck(self):
        import random
        random.seed(1)
        deck = Deck()
        deck.shuffle()
        c = deck.draw()
        self.assertFalse(c.rank == Rank.ACE and c.suit == Suit.SPADE)

class TestRank(unittest.TestCase):

    def test_rank_compare(self):
        self.assertTrue(Rank.ACE > Rank.TEN)
        self.assertFalse(Rank.JACK > Rank.QUEEN)
        self.assertTrue(Rank.THREE < Rank.FOUR)
        self.assertTrue(Rank.THREE < Rank.ACE)

if __name__ == "__main__":
    unittest.main()