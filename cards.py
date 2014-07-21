# Cards module
"""A module containing objects like Card, Hand, Deck for card games.
"""
import random
import textwrap

# Define Constants

MAX_NUMBER_OF_DECKS_BEFORE_RNG = 6

DECK_SIZE = 52

CARD_RANKS = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

CARD_SUITS_SYMBOLS = {
    "classic": ("\u2660", "\u2661", "\u2662", "\u2663"),
    "open_symbols": ("\u2664", "\u2661", "\u2662", "\u2667"),
    "filled_symbols": ("\u2660", "\u2665", "\u2666", "\u2663"),
    "letters": ("S", "H", "D", "C")
}

CARD_SUITS = CARD_SUITS_SYMBOLS["classic"]

FACE_CARD_VALUE = 10

BUST_LIMIT_VALUE = 21


# Define Classes

class Card(object):
    "A card class"
    def __init__(self, card_index):
        """Create a card object and compute rank and suit
        from its index
        """
        self.card = card_index
        self.rank = self.card % 13
        self.suit = self.card // 13

    def __str__(self):
        return u"{}{}".format(CARD_RANKS[self.rank], CARD_SUITS[self.suit])


class CardCollection(list):
    "A generic class for a list of cards"
    def __init__(self, card_indices=[]):
        """Create a collection of cards from a list of card numbers
        """
        self.card_indices = card_indices
        self.cards = []
        for card_index in self.card_indices:
            self.cards.append(Card(card_index))

    def __str__(self):
        return u" ".join([card.__str__() for card in self.cards])


class Deck(CardCollection):
    "A deck of cards"
    def __init__(self, number_of_decks=1):
        """Create a blackjack deck containing
        one or more decks of 52 cards.
        """
        if number_of_decks < 1:
            raise ValueError
        self.number_of_decks = number_of_decks
        card_indices = []
        if number_of_decks > MAX_NUMBER_OF_DECKS_BEFORE_RNG:
            self.number_cards_left = sys.maxsize
            super().__init__(card_indices)
        else:
            card_indices = list(range(DECK_SIZE)) * number_of_decks
            self.number_cards_left = DECK_SIZE * number_of_decks
            random.shuffle(card_indices)
        super().__init__(card_indices)

    def draw_cards(self, ncards=1):
        if self.number_of_decks == 0:
            return [random.randint(0, DECK_SIZE-1) for i in range(ncards)]
        else:
            self.number_cards_left -= ncards
            for i in range(ncards):
                self.cards.pop()
            return [self.card_indices.pop() for i in range(ncards)]

    def show_next_cards(self, ncards=1):
        if self.number_of_decks > MAX_NUMBER_OF_DECKS_BEFORE_RNG:
            print("It's a mystery")
        else:
            cards_to_show = self.card_indices[-ncards:]
            print(CardCollection(cards_to_show))

    def __str__(self):
        return u" ".join([card.__str__() for card in reversed(self.cards)])


class Hand(CardCollection):
    "A hand of cards"
    def __init__(self, card_indices=[], holecard=False):
        """Initialize a hand of cards
        """
        self.hiddencard = []
        self.number_of_cards = len(card_indices)
        # Offers the possibility to hide a card ("hole cards")
        if holecard:
            self.hiddencard.append(card_indices[0])
            super().__init__(card_indices[1:])
        else:
            super().__init__(card_indices)

    def add_card(self, newcard):
        self.number_of_cards += 1
        if isinstance(newcard, int):
            self.card_indices.append(newcard)
            self.cards.append(Card(newcard))
        elif isinstance(newcard, list):
            try:
                (card,) = newcard
                if isinstance(card, int):
                    self.card_indices.append(card)
                    self.cards.append(Card(card))
                else:
                    raise TypeError
            except ValueError:
                print("add_card must be supplied an int"
                      "or a singleton list")

    def reveal_holecard(self):
        self.card_indices.extend(self.hiddencard)
        self.cards.append(Card(self.hiddencard))
        self.hiddencard = []

    def is_splittable(self):
        is_initial_hand = len(self.cards) == 2
        cards_have_same_rank = self.cards[0].rank == self.cards[1].rank
        return is_initial_hand and cards_have_same_rank

    def value(self):
        "returns the value of the hand"
        handvalue = -1
        card_ranks = sorted([card.rank for card in self.cards], reverse=True)
        handvalue = sum([min(FACE_CARD_VALUE, r+1) for r in card_ranks if r > 0])
        num_aces = card_ranks.count(0)
        if num_aces > 0:
            use_aces_as_one = handvalue + 10 + 1 * num_aces > BUST_LIMIT_VALUE
            if use_aces_as_one:
                handvalue += num_aces
            else:
                handvalue += 10 + 1 * num_aces
        return handvalue


# class DiscardPile(CardCollection):
#     "A discard pile to keep track of play history"
#     def __init__(self):
#         super().__init__()
#     def show(self, n=1):
#         print()
