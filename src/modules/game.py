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

RANK_TO_HAND = {
    0 : "High Card",
    1 : "One Pair",
    2 : "Two Pair",
    3 : "Three of a Kind",
    4 : "Straight",
    5 : "Flush",
    6 : "Full House",
    7 : "Four of a Kind",
    8 : "Straight Flush",
    9 : "Royal Flush"
}

IRRELEVANT_KICKER = Card(0, "")

# Check if hand is a flush
def is_flush(cards) -> bool:
    suits = set([card.suit for card in cards])
    return len(suits) == 1

# Check if hand is a straight
def is_straight(cards) -> bool:
    # Get all unique card values
    values = sorted(set([card.int_value for card in cards]), reverse=True)
    
    # Less than 5 unique values, hand can't be a straight 
    if len(values) < 5: return False

    if values[0] - values[4] == 4: return True # (Not so) cool math for the nerds    
    if set([14, 2, 3, 4, 5]).issubset(values): return True # Check for A-2-3-4-5, because A=14 in my code
    return False # If none of the above, then hand is not a straight

# Return the high card of a straight (only call if hand is confirmed a straight)
def get_straight_high(cards) -> bool:
    values = sorted(set([card.int_value for card in cards]), reverse=True)
    return values[1] if set([14, 2, 3, 4, 5]).issubset(values) else values[0]

# Determine best hand from the selected 7 cards
def evaluate_hand(cards) -> tuple:
    # Get info about hand
    card_values = sorted([card.int_value for card in cards], reverse=True)
    flush = is_flush(cards)
    straight = is_straight(cards)
    count = Counter(card_values)
    count_freq = count.most_common()

    # Straight flush and royal flush
    if flush and straight:
        high = get_straight_high(cards)
        if high == 12: return (HAND_RANKS["Royal Flush"], IRRELEVANT_KICKER)
        return (HAND_RANKS["Straight Flush"], high)
    
    # Four of a kind
    if count_freq[0][1] == 4:
        return (HAND_RANKS["Four of a Kind"], count_freq[0][0])
    
    # Full House
    if count_freq[0][1] == 3 and count_freq[1][1] == 2:
        return (HAND_RANKS["Full House"], count_freq[0][1]) # Should change this to include the pair
    
    # Flush
    if flush:
        return (HAND_RANKS["Flush"], card_values[0])
    
    # Straight
    if straight:
        return (HAND_RANKS["Straight"], get_straight_high(cards))
    
    # Three of a kind
    if count_freq[0][1] == 3:
        return (HAND_RANKS["Three of a Kind"], count_freq[0][1]) # Should change this to include the kicker, so tie breakers can happen
    
    # Two Pair
    if count_freq[0][1] == 2 and count_freq[1][1] == 2:
        return (HAND_RANKS["Two Pair"], max(count_freq[0][1], count_freq[1][1])) # Should change this to include the kicker, so tie breakers can happen
    
    # One pair
    if count_freq[0][1] == 2:
        return (HAND_RANKS["One Pair"], count_freq[0][1]) # Should change this to include the kicker, so tie breakers can happen

    # High Card
    return (HAND_RANKS["High Card"], card_values[0])

# Evaluate a player's best hand
def best_player_hand(player_hand, board) -> tuple:
    total_cards = list(player_hand) + board

    best = None
    best_kicker = None
    for comb in itr.combinations(total_cards, 5):
        rank, kicker = evaluate_hand(comb)
        if best is None or rank > best or (best == rank and kicker > best_kicker):
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
        player_scores.sort(reverse=True, key=lambda x: x[0]) # So that the highest rank is in the lowest position
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
        
        winners = self.determin_winner()
        for winner in winners:
            print(f'{winner[1]} won with a {RANK_TO_HAND[winner[0][0]]}')
        
    
    # Debug
    def __str__(self) -> str:
        return "\n".join(str(player) for player in self.players) + "\nBoard: " + ", ".join(str(card) for card in self.board_cards)
    def __repr__(self):
        return str(self)
