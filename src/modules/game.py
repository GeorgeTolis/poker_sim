#import pygame
from .deck import Deck
from .cards import Card
from .player import Player

from itertools import cycle

class Game:
    def __init__(self, num_of_players: int):
        self.deck = Deck()
        self.players = [Player() for i in range(num_of_players)]
        self.board_cards = []
        self.pot_size = 0
        self.game_actions = [self.deal_cards, self.flop, self.turn, self.river]

    # Resets deck so it doesn't have missing cards
    def reset_deck(self) -> None:
        self.deck = Deck()

    # Cycles players so there are new small and big blinds
    def cycle_players(self) -> None:
        temp = self.players.pop(0)
        self.players.append(temp)

    # Set all players to active
    def activate_players(self) -> None:
        for player in self.players: player.active = True

    # Makes preperations for the next blind
    def next_blind(self) -> None:
        self.reset_deck()
        self.cycle_players()
        self.activate_players()
        self.pot_size = 0

    # Deals a hand to each player
    def deal_cards(self) -> None:
        self.deck.shuffle()

        for player in self.players:
            player_hand = (self.deck.pop(), self.deck.pop())
            player.new_hand(player_hand)

    # Initiates the flop
    def flop(self):
        self.board_cards = [self.deck.pop(), self.deck.pop(), self.deck.pop()]

    # Gets the turn card
    def turn(self):
        self.board_cards.append(self.deck.pop())

    # Finishes out board with the river
    def river(self):
        self.board_cards.append(self.deck.pop())

    # Questions each player for his action
    def player_actions(self):
        players_to_act = len([player for player in self.players if player.active])
        last_raise = 0

        while players_to_act > 0:
            for player in self.players:
                if players_to_act <= 0: break
                if not player.active: continue

                action, bet = player.action(last_raise)
                if action == "check":
                    players_to_act -= 1
                elif action == "fold":
                    players_to_act -= 1
                    player.active = False
                elif action == "raise":
                    players_to_act = len([player for player in self.players if player.active]) - 1
                    self.pot_size += bet
                elif action == "call":
                    players_to_act -= 1
                    self.pot_size += bet


    # Initiates play
    def play(self):
        for action in self.game_actions:
            action()
            self.player_actions()
            # Debug
            print(self)
            print(50 * "-")
        
    
    # Debug
    def __str__(self) -> str:
        return "\n".join(str(player) for player in self.players) + "\nBoard: " + ", ".join(str(card) for card in self.board_cards)
    def __repr__(self):
        return str(self)
