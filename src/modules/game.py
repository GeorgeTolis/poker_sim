#import pygame
from .deck import Deck
from .cards import Card
from .player import Player

import itertools as itr
from collections import Counter

HAND_RANKS = {
    "High Card": 0,
    "One Pair": 1,
    "Two Pair": 2,
    "Three of a Kind": 3,
    "Straight": 4,
    "Flush": 5,
    "Full House": 6,
    "Four of a Kind": 7,
    "Straight Flush": 8,
    "Royal Flush": 9
}

IRRELEVANT_KICKER = Card(0, "")

# Determine best hand from the selected 7 cards
def evaluate_hand(total_cards) -> tuple:
    pass

# Evaluate a player's best hand
def best_player_hand(self, player_hand, board) -> tuple:
        total_cards = list(player_hand) + board

        best = None
        best_kicker = None
        for comb in itr.combinations(total_cards, 5):
            rank, kicker = evaluate_hand(comb)
            if best is None or rank > best:
                best = rank
                best_kicker = kicker

        return best, best_kicker

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

    # Determines winner of the current blind
    def determin_winner(self) -> list:
        # Edge case, no player active for some reason, cancel search
        player_pool = [player for player in self.players if player.active]
        if len(player_pool) <= 0:
            return None

        # Assess everyone's best hands and get all players with the same hand
        player_scores = [(best_player_hand(player.hand, self.board_cards), player) for player in player_pool]
        player_scores.sort(reverse=True, key=lambda x: (x[0], x[1])) # So that the highest rank is in the lowest position
        best_hand = player_scores[0]

        # Winners are all players with the same hand and kicker
        winners = [score for score in player_scores if score[0] == best_hand[0] and score[1] == best_hand[1]]
        return winners

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
