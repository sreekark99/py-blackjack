# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:53:31 2023

@author: sreek
"""

import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ('ace', 'two', 'three', 'four', 'five', 'six', 'seven',
         'eight', 'nine', 'ten', 'jack', 'queen', 'king')
values_arr = {'ace': 11, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
              'eight': 8, 'nine': 9, 'ten': 10, 'jack': 10, 'queen': 10, 'king': 10}

playing = True


class card:
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank.capitalize()} of {self.suit.capitalize()}"


class deck:
    def __init__(self):
        self.all_cards = []
        for i in suits:
            for j in ranks:
                self.all_cards.append(card(i, j))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def take_out_one_card(self):
        try:
            return self.all_cards.pop()
        except:
            print("Out of cards")
            return None

    def __str__(self):
        s = "Deck currently has\n"
        for i in self.all_cards:
            s += (i.__str__() + " | ")
        return s


class player:
    def __init__(self, name="Computer"):
        self.name = name
        self.cards_in_hand = []
        self.curr_value = 0
        self.ace_ctr = 0

    def add_card(self, new_card):
        self.cards_in_hand.append(new_card)
        self.curr_value += values_arr[new_card.rank.lower()]
        if(new_card.rank.lower() == "ace"):
            self.ace_ctr += 1

    def ace_func(self):
        while(self.curr_value > 21) and (self.ace_ctr > 0):
            self.curr_value -= 10
            self.ace_ctr -= 1


class chips:
    def __init__(self, total_chips=100):
        self.total_chips = total_chips
        self.bet = 0

    def win(self):
        self.total_chips += self.bet

    def lose(self):
        self.total_chips -= self.bet


def bet_taker(chips_obj, player_obj):
    while True:
        try:
            chips_obj.bet = int(
                input(f">> {player_obj.name}, enter the of chips you wanna bet: "))
        except ValueError:
            print(
                f"Enter an integer, {player_obj.name}\nYou currently have {chips_obj.total_chips} chips")
            continue
        else:
            if(chips_obj.bet > chips_obj.total_chips):
                print(
                    f"Sorry {player_obj.name}! You don't have that many chips to bet\nYou currently have {chips_obj.total_chips} chips")
                continue
            elif chips_obj.bet < 1:
                print(
                    f"Please check what you have entered, {player_obj.name}\nYou currently have {chips_obj.total_chips} chips")
                continue
            else:
                break


def hit(deck_obj, player_obj):
    new_card = deck_obj.take_out_one_card()
    if new_card != None:
        player_obj.add_card(new_card)
        player_obj.ace_func()


def hit_or_stand(deck_obj, player_obj):
    global playing
    input_arr = ('h', 's')
    while True:
        try:
            command = input(">> Enter 'h' to hit (or) 's' to stand: ").split()
            if len(command) > 1 or len(command) == 0:
                print(
                    f"Please check what you have entered, {player_obj.name}")
                raise Exception
            else:
                if len(command[0]) > 1:
                    print(
                        f"Enter either 'h' or 's' only, {player_obj.name}")
                    raise Exception
                else:
                    break
            if command not in input_arr:
                print(f"Enter either 'h' or 's' only, {player_obj.name}")
                raise Exception
        except:
            continue
        else:
            break
    command = command[0]
    if command == 'h':
        hit(deck_obj, player_obj)

    else:
        print(f"{player_obj.name} stands")
        playing = False


def display_some(player_obj, dealer_obj):
    print()
    print("<< Dealer's hand has: >>")
    print("**First card hidden**")
    print(dealer_obj.cards_in_hand[1])
    print()
    print("<< Player's hand has: >>")
    for i in player_obj.cards_in_hand:
        print(i)
    print(f"Value of player's cards: {player_obj.curr_value}")
    print()


def display_all(player_obj, dealer_obj):
    print()
    print("<< Dealer's hand has: >>")
    for i in dealer_obj.cards_in_hand:
        print(i)
    print(f"Value of dealer's cards: {dealer_obj.curr_value}")
    print()
    print("<< Player's hand has: >>")
    for i in player_obj.cards_in_hand:
        print(i)
    print(f"Value of player's cards: {player_obj.curr_value}")
    print()


def player_bust(player, dealer, chips):
    print(f"{player.name} busted. {dealer.name} wins!")
    chips.lose()


def player_win(player, dealer, chips):
    print(f"{player.name} wins!. {dealer.name} busted.")
    chips.win()


def dealer_bust(player, dealer, chips):
    print(f"{dealer.name} busted. {player.name} wins!")
    chips.win()


def dealer_win(player, dealer, chips):
    print(f"{dealer.name} wins! {player.name} busted")
    chips.lose()


def push(player, dealer):
    print(f"{dealer.name} and {player.name} pushed to a tie!")


while True:
    p1_name = input(">> What's your name, player? ").split()
    while(len(p1_name) != 1):
        print("Enter your name! Don't worry I won't store it")
        p1_name = input(">> What's your name, player? ").split()
    p1_name = p1_name[0]
    print(f">> Welcome to SK-PyJack, {p1_name}! <<")
    deck1 = deck()
    deck1.shuffle()

    player_hand = player(p1_name)
    player_hand.add_card(deck1.take_out_one_card())
    player_hand.add_card(deck1.take_out_one_card())

    dealer_hand = player()
    dealer_hand.add_card(deck1.take_out_one_card())
    dealer_hand.add_card(deck1.take_out_one_card())

    while True:
        try:
            total_chips = input(
                ">> Enter the number of chips to begin with, press return to start with 100 chips: ")
            if total_chips == "":
                total_chips = 100
                break
            else:
                total_chips = int(total_chips)
        except:
            print(f"{player_hand.name}, type a number")
            continue
        else:
            break
    player_chips = chips(total_chips)
    bet_taker(player_chips, player_hand)
    print()
    display_some(player_hand, dealer_hand)
    while playing == True:
        hit_or_stand(deck1, player_hand)
        display_some(player_hand, dealer_hand)
        if player_hand.curr_value > 21:
            player_bust(player_hand, dealer_hand, player_chips)
            break
    if (player_hand.curr_value <= 21):
        while dealer_hand.curr_value < player_hand.curr_value:
            # We can alternatively check as long as dealer's hand value is less than 17
            hit(deck1, dealer_hand)
        display_all(player_hand, dealer_hand)
        if dealer_hand.curr_value > 21:
            dealer_bust(player_hand, dealer_hand, player_chips)
        elif (dealer_hand.curr_value > player_hand.curr_value):
            dealer_win(player_hand, dealer_hand, player_chips)
        elif dealer_hand.curr_value < player_hand.curr_value:
            player_win(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    print(f"{player_hand.name} has {player_chips.total_chips} chips in the end!")
    print()
    new_game_arr = ("y", "n")
    while True:
        try:
            new_game = input(">> Do you want to play again? 'y/n': ").split()
            if len(new_game) != 1:
                raise Exception
            else:
                if len(new_game[0]) > 1:
                    raise Exception
                elif new_game[0].lower() not in new_game_arr:
                    raise Exception
        except:
            print(
                f"Please check what you have entered, {player_hand.name}")
            continue
        else:
            break
    new_game = new_game[0].lower()
    if new_game == "y":
        playing = True
        continue
    else:
        print(f"See ya later {player_hand.name}!")
        break
