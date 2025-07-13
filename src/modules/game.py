#import pygame
from .deck import Deck
from .cards import Card
from .player import Player

class Game:
    def __init__(self, num_of_players: int):
        self.deck = Deck()
        self.players = [Player() for i in range(num_of_players)]
        self.board_cards = []
        self.game_actions = [self.deal_cards, self.flop, self.turn, self.river]

    # Resets deck so it doesn't have missing cards
    def reset_deck(self) -> None:
        self.deck = Deck()

    # Cycles players so there are new small and big blinds
    def cycle_players(self) -> None:
        temp = self.players.pop(0)
        self.players.append(temp)

    # Makes preperations for the next blind
    def next_blind(self) -> None:
        self.reset_deck()
        self.cycle_players

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
        pass

    # Initiates play
    def play(self):
        for action in self.game_actions:
            action()
            self.player_actions()
            print(self)
            print(50 * "-")
    
    # Debug
    def __str__(self) -> str:
        return "\n".join(str(player) for player in self.players) + "\nBoard: " + ", ".join(str(card) for card in self.board_cards)
    def __repr__(self):
        return str(self)

        