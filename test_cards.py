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
        self.holecardhand = cards.Hand([0,12], holecard = True)
    
    def test_print(self):
        # make sure the shuffled sequence does not lose any elements
        self.assertEqual(self.hand.__str__(), u"A\u2660 A\u2661 K\u2660")

    def test_value(self):
        # make sure the corner case for hand value is covered
        self.assertEqual(self.hand.value(), 12)

    def test_reveal(self):
        self.holecardhand.reveal_holecard()
        self.assertEqual(self.holecardhand.__str__(), u"K\u2660 A\u2660")
        self.assertEqual(self.holecardhand.value(), 21)


class TestDeck(unittest.TestCase):
    
    def setUp(self):
        self.deck1 = cards.Deck(1)
        self.deck2 = cards.Deck(8)

    def test_draw_cards(self):
        self.assertEqual(self.deck1.__str__()[:2],
                         cards.Card(self.deck1.draw_cards(1)).__str__())

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
