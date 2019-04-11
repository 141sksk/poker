import unittest
from models.trump import Card, Rank, Suit, Deck, InvalidOperationError, PokerPlayer, PokerHand


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

class TestPokerPlayer(unittest.TestCase):

    def test_hands_append(self):
        pokerplayer = PokerPlayer()
        self.assertEqual(len(pokerplayer), 0)
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FIVE, suit=Suit.SPADE))
        self.assertEqual(len(pokerplayer), 5)

    def test_append_fail_caused_by_invalid_type(self):
        pokerplayer = PokerPlayer()
        with self.assertRaises(TypeError):
            pokerplayer.append('スペードA')

    def test_append_fail_caused_by_invalid_opration(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FIVE, suit=Suit.SPADE))
        with self.assertRaises(InvalidOperationError):
            pokerplayer.append(Card(rank=Rank.SIX, suit=Suit.SPADE))

    def test_discard(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FIVE, suit=Suit.SPADE))
        pokerplayer.discard([1, 2])
        self.assertTrue(len(pokerplayer) == 3)
        
    def test_discard_fail_caused_by_invalid_type(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        with self.assertRaises(TypeError):
            pokerplayer.discard('test')
    
    def test_discard_fail_caused_by_invalid_index(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        with self.assertRaises(InvalidOperationError):
            pokerplayer.discard([10])

    def test_evaluate_ONE_PAIR(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FIVE, suit=Suit.SPADE))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.ONE_PAIR)

    def test_evaluate_TWO_PAIR(self):    
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.CLUB))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.TWO_PAIR)

    def test_evaluate_THREE_CARD(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.CLUB))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.THREE_CARD)
        
    def test_evaluate_STRAIGHT(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.SIX, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FIVE, suit=Suit.CLUB))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.STRAIGHT)
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.JACK, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.QUEEN, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.KING, suit=Suit.CLUB))
        self.assertFalse(pokerplayer.evaluate() == PokerHand.STRAIGHT)
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.JACK, suit=Suit.HEART))
        pokerplayer.append(Card(rank=Rank.TEN, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.CLUB))
        pokerplayer.append(Card(rank=Rank.EIGHT, suit=Suit.DIAMOND))
        self.assertNotEqual(pokerplayer.evaluate(), PokerHand.STRAIGHT)

    def test_evaluate_FLUSH(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.SIX, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.NINE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.KING, suit=Suit.SPADE))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.FLUSH)

    def test_evaluate_FULL_HOUSE(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.HEART))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.HEART))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.DIAMOND))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.FULL_HOUSE)
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.HEART))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.CLUB))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.DIAMOND))
        self.assertNotEqual(pokerplayer.evaluate(), PokerHand.FOUR_CARD)

    def test_evaluate_FOUR_CARD(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.HEART))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.CLUB))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.DIAMOND))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.FOUR_CARD)
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.HEART))
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.CLUB))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.DIAMOND))
        self.assertNotEqual(pokerplayer.evaluate(), PokerHand.FOUR_CARD)

    def test_evaluate_STRAIGHT_FLUSH(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FIVE, suit=Suit.SPADE))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.STRAIGHT_FLUSH)
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.KING, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.THREE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FOUR, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.FIVE, suit=Suit.SPADE))
        self.assertNotEqual(pokerplayer.evaluate(), PokerHand.STRAIGHT_FLUSH)
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.KING, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.QUEEN, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.JACK, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TEN, suit=Suit.SPADE))
        self.assertNotEqual(pokerplayer.evaluate(), PokerHand.STRAIGHT_FLUSH)

    def test_evaluate_RIYAL_STRAIGHT_FLUSH(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TEN, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.JACK, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.QUEEN, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.KING, suit=Suit.SPADE))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.ROYAL_STRAIGHT_FLUSH)
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.NINE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.TEN, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.JACK, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.QUEEN, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.KING, suit=Suit.SPADE))
        self.assertFalse(pokerplayer.evaluate() == PokerHand.ROYAL_STRAIGHT_FLUSH)

    def test_evaluate_NO_PAIR(self):
        pokerplayer = PokerPlayer()
        pokerplayer.append(Card(rank=Rank.ACE, suit=Suit.SPADE))
        pokerplayer.append(Card(rank=Rank.JACK, suit=Suit.HEART))
        pokerplayer.append(Card(rank=Rank.TEN, suit=Suit.DIAMOND))
        pokerplayer.append(Card(rank=Rank.TWO, suit=Suit.CLUB))
        pokerplayer.append(Card(rank=Rank.EIGHT, suit=Suit.DIAMOND))
        self.assertEqual(pokerplayer.evaluate(), PokerHand.NO_PAIR)

if __name__ == "__main__":
    unittest.main()