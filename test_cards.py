import unittest
import cards

class TestCard(unittest.TestCase):

    def setUp(self):
        self.card = cards.Card(13)
    
    def test_print(self):
        # make sure the shuffled sequence does not lose any elements
        self.assertEqual(self.card.__str__(), u"A\u2661")


class TestHand(unittest.TestCase):

    def setUp(self):
        self.hand = cards.Hand([0,13,12])
        self.holecardhand = cards.Hand([0,25], holecard = True)
    
    def test_print(self):
        # make sure the shuffled sequence does not lose any elements
        self.assertEqual(self.hand.__str__(), u"A\u2660 A\u2661 K\u2660")

    def test_value(self):
        pass

    def test_reveal(self):
        pass


class TestDeck(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

# card1 = cards.Card(23)
# print(card1)
# cardcoll1 = cards.CardCollection([12, 13])
# print(cardcoll1.card_indices)
# print(cardcoll1.cards)
# print(cardcoll1)
# bDeck = cards.Deck(1)
# print(bDeck)
# print(cards.Card(bDeck.draw_cards(1)[0]))
# print(bDeck)
# bDeck.show_next_cards(5)
# h = cards.Hand(bDeck.draw_cards(2))
# print(h)
# print(h.value())
