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


def deal_initial_hands(bljdeck, dealerholecard=False):
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


def play_round(bdeck, pmoney, pwholecard):
    # Require user input for the bet
    bet_value = bet(pmoney)

    # Create the initial hands for the dealer and the player
    DealerHand, PlayerHand = deal_initial_hands(bdeck, pwholecard)

    # Display the initial hands
    print("The dealer's hand is:\n", DealerHand)
    print("Your hand is:\n", PlayerHand)
    # Check for a blackjack
    player_blackjack = PlayerHand.value() == 21
    if player_blackjack:
        print("You have a Blackjack\n")

    # Require user input for hand resolution
    while True:
        chosen_action = input("What would you like to do?\n"
                              "[H]it or [S]tand?  :")
        if chosen_action in ["H", "h"]:
            PlayerHand.add_card(bdeck.draw_cards())
            print("Your hand is now:\n", PlayerHand)
            print("Value: {} \n".format(PlayerHand.value()))
            if PlayerHand.value() > 21:
                print("You busted\n")
                return False, bet_value
            else:
                continue
        elif chosen_action in ["S", "s"]:
            yourhand = PlayerHand.value()
            break
        else:
            print("Please make another selection using 'h' or 's'\n")
            continue

    # Resolve Dealer
    if pwholecard:
        DealerHand.reveal_holecard()
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
        DealerHand.add_card(bdeck.draw_cards())
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


def print_welcome_msg():
    """Prints a welcome message"""
    print("\n\nWelcome to our blackjack table\n")
    print(u" "*12+u"A\u2661 K\u2660"+u" "*12+"\n")


def game_action():
    while True:
        chosen_action = input("Would you like to:\n"
                              "1. [P]lay another round or\n"
                              "2. [Q]uit?\n")
        if chosen_action in ["P", "p", "1"]:
            return "p"
        elif chosen_action in ["Q", "q", "2"]:
            return
        else:
            print("Please make another selection using 'p' or 'q'\n")
            continue


# main()

def main():
    # Welcome message
    print_welcome_msg()

    # Setup global variables
    play_with_holecards = False
    player_money = 100
    ndecks = 2
    nround = 0

    # Setup Deck
    bdeck = cards.Deck(ndecks)

    # Start round loop
    while player_money > 0:
        print("Round "+str(nround))
        print("You have "+str(player_money)+" money units.")
        if bdeck.number_cards_left < 8:
            bdeck = cards.Deck(ndecks)
        win, bet = play_round(bdeck, player_money, play_with_holecards)
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
