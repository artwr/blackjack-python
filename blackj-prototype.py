#!/usr/bin/env python
"""
SYNOPSIS

    blackjack

AUTHOR

    Arthur Wiedmer <arthur.wiedmer_pyscript@m4x.org>

LICENSE

    This script is released under the CC0 1.0 Universal
    http://creativecommons.org/publicdomain/zero/1.0/
"""

from __future__ import print_function
import math
import random
import traceback
import os, sys

#class Deck:
#    pass

class Hand(object):
    "A hand of cards"
    def __init__(self, ncards = 2, holecard = False):
        """Initialize a hand of cards for blackjack.
        Defaults to 2 cards with no hidden card.
        """
        self.cards = []
        self.hiddencard = []
        self.number_of_cards = ncards
        self.visible_cards = ncards
        # Offers the possibility to hide a card ("hole cards")
        if holecard:
            self.visible_cards -= 1
            self.hiddencard = [draw_card()]
        for i in range(self.visible_cards):
            self.cards.append(draw_card())
        self.cardranks = {
            '0': "A",
            '1': "2",
            '2': "3",
            '3': "4",
            '4': "5",
            '5': "6",
            '6': "7",
            '7': "8", 
            '8': "9",
            '9': "10",
            '10': "J",
            '11': "Q",
            '12': "K"
        }
        self.cardsuits = {
            '0': u"\u2660",
            '1': u"\u2661",
            '2': u"\u2662",
            '3': u"\u2663"
        }
    
    def __str__(self):
        handstr = u""
        for card in self.cards:
            rank = str(card % 13)
            suit = str(card / 13)
            handstr += u"{}{}".format(self.cardranks[rank],self.cardsuits[suit])
        return handstr.encode(sys.stdout.encoding)

    def add_card(self,newcard):
        self.number_of_cards += 1
        self.visible_cards += 1
        self.cards.append(newcard)

    def reveal_cards(self):
        self.cards.extend(self.hiddencard)
        self.visible_cards += len(self.hiddencard)
        self.hiddencard = []

    def value(self):
        "returns the value of the hand"
        handvalue = 0
        for card in sorted(self.cards, reverse = True):
            rank = card % 13
            if rank > 0:
                handvalue += min(10,rank+1)
            elif handvalue + 11 > 21:
                handvalue += 1
            else: 
                handvalue += 11
        return handvalue


def draw_card():
    "Draw a random card"
    return random.choice(range(52))

def draw_initial_hands(dealerholecard = False):
    "Draw hands for the dealer and the player with two cards"
    return Hand(holecard = dealerholecard), Hand()


def bet(player_money):
    while True:
        bet_str = raw_input("How much would you like to bet? [1-"+str(player_money)+"]\n")
        try:
            bet = int(bet_str.strip())
        except ValueError:
            print("You must enter an integer\n")
        else:
            if bet > player_money:
                print("You do not have enough money for this bet. You should place a lower bet\n")
                continue
            elif bet < 1:
                print("You need to bet at least 1\n")
                continue
            else:
                return bet
    return bet


def play_round(money_left):
    bet_value = 0
    bet_value += bet(money_left)
    DealerHand, PlayerHand = draw_initial_hands()
    print("The dealer's hand is:\n",DealerHand)
    print("Your hand is:\n",PlayerHand)
    if PlayerHand.value() == 21:
        print("You have a Blackjack")
        player_blackjack = True
    else:
        player_blackjack = False
    # Require user action
    while True:
        chosen_action = raw_input("What would you like to do? [H]it, [S]tand, Increase your [B]et?\n")
        if chosen_action in ["H","h"]:
            PlayerHand.add_card(draw_card())
            print("Your hand is now:\n",PlayerHand)
            print("Value: {} \n".format(PlayerHand.value()))
            if PlayerHand.value() > 21:
                print("You busted\n")
                return False, bet_value
            else:
                continue
        elif chosen_action in ["B","b"]:
            bet_value += bet(money_left - bet_value)
        elif chosen_action in ["S","s"]:
            yourhand = PlayerHand.value()
            break
        else:
            print("Please make another selection using 'h','b' or 's'\n")
            continue
    # Resolve Dealer
    DealerHand.reveal_cards()
    print("The dealer's hand is:\n",DealerHand)
    if DealerHand.value() == 21:
        print("The dealer has a Blackjack")
        if player_blackjack:
            print("This is a push. No winner.")
            return True, 0
        else:
            print("You lost this round.")
            return False, bet_value
    while DealerHand.value() < 17:
        print("The dealer draws a card\n")
        DealerHand.add_card(draw_card())
        print("The dealer's hand is now:\n",DealerHand)
    if DealerHand.value() > 21:
        print("The dealer busted\n")
        return True, bet_value
    else:
        if yourhand > DealerHand.value():
            print("You won this round.")
            if player_blackjack:
                return True, math.floor(1.5*bet_value)
            else:
                return True, bet_value
        else:
            print("You lost this round.")
            return False, bet_value
    print("wrong end")
    return False, bet_value


def main ():
    holecards = False
    player_money = 100
    print("Welcome to our blackjack table")
    while player_money > 0:
        print("You have "+str(player_money)+" money units.")
        win, bet = play_round(player_money)
        if win:
            player_money += bet
        else:
            player_money -= bet
    print("You lost the game.")
    #random.shuffle
    #print(u'\u2660\u2661\u2662\u2663\u2664\u2665\u2666\u2667')
    # DealerHand = draw_initial_hand()
    # print(DealerHand.cards)
    # print(DealerHand)
    # print("Dealer hand value",DealerHand.value())
    #
    return

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e: # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)