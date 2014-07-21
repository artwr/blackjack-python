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

# Imports
import math
import random
import traceback
import os
import sys

# Import custom cards module
import cards

# Define global constants

BLACKJACK_PAYOUT = 3.0/2

# Define auxiliary functions


def draw_initial_hands(bljdeck, dealerholecard=False):
    "Draw hands for the dealer and the player with two cards"
    initial_cards = bljdeck.draw_cards(ncards=4)
    dhand = cards.Hand(card_indices=[initial_cards[1], initial_cards[3]],
                       holecard=dealerholecard)
    phand = cards.Hand(card_indices=[initial_cards[0], initial_cards[2]])
    return dhand, phand


def bet(player_money):
    while True:
        bet_str = input("How much would you like to bet?"
                        " [1-"+str(player_money)+"]\n")
        try:
            bet = int(bet_str.strip())
        except ValueError:
            print("You must enter an integer\n")
        else:
            if bet > player_money:
                print("You do not have enough money for this bet."
                      "You should place a lower bet\n")
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
    print("The dealer's hand is:\n", DealerHand)
    print("Your hand is:\n", PlayerHand)
    if PlayerHand.value() == 21:
        print("You have a Blackjack")
        player_blackjack = True
    else:
        player_blackjack = False
    # Require user action
    while True:
        chosen_action = input("What would you like to do?\
         [H]it, [S]tand, Increase your [B]et?\n")
        if chosen_action in ["H", "h"]:
            PlayerHand.add_card(draw_card())
            print("Your hand is now:\n", PlayerHand)
            print("Value: {} \n".format(PlayerHand.value()))
            if PlayerHand.value() > 21:
                print("You busted\n")
                return False, bet_value
            else:
                continue
        elif chosen_action in ["B", "b"]:
            bet_value += bet(money_left - bet_value)
        elif chosen_action in ["S", "s"]:
            yourhand = PlayerHand.value()
            break
        else:
            print("Please make another selection using 'h','b' or 's'\n")
            continue
    # Resolve Dealer
    DealerHand.reveal_cards()
    print("The dealer's hand is:\n", DealerHand)
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
        print("The dealer's hand is now:\n", DealerHand)
    if DealerHand.value() > 21:
        print("The dealer busted\n")
        return True, bet_value
    else:
        if yourhand > DealerHand.value():
            print("You won this round.")
            if player_blackjack:
                return True, math.floor(BLACKJACK_PAYOUT*bet_value)
            else:
                return True, bet_value
        else:
            print("You lost this round.")
            return False, bet_value
    print("wrong end")
    return False, bet_value


# main()

def main():
    holecards = False
    player_money = 100
    print("Welcome to our blackjack table")
    nround = 0
    while player_money > 0:
        print("Round "+str(nround))
        print("You have "+str(player_money)+" money units.")
        win, bet = play_round(player_money)
        if win:
            player_money += bet
        else:
            player_money -= bet
        nround += 1
    print("You lost the game.")
    return

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)
