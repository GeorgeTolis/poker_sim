#import pygame

card_value_to_int = {"A": 1, "2": 2, "3": 3, "4": 4,
                     "5": 5, "6": 6, "7": 7, "8": 8,
                     "9": 9, "10": 10, "J": 11, "Q": 12, 
                     "K": 13, "Back1": 0, "Back2": 0, "": 0}

int_to_card_value = {1: "A", 2: "2", 3: "3", 4: "4",
                     5: "5", 6: "6", 7: "7", 8: "8",
                     9: "9", 10: "10", 11: "J", 12: "Q", 
                     13: "K", 14: "A", -1: "Back1", -2: "Back2", 0: "Dummy"}

class Card:
    """
    Definition of Card class. Each card has:
    value --> name of card
    int_value --> list of potential integer values that correspond to its value
    suit --> suit it belongs (clubs, diamonds, hearts, spades)
    """
    def get_int_value(self, value: str) -> int:
        return card_value_to_int[value]

    def get_card_value(self, int_value: int) -> str:
        return int_to_card_value[int_value]

    def __init__(self, int_value: list, suit: str):
        self.value = self.get_card_value(int_value)
        self.int_value = 14 if int_value == 1 else int_value
        self.suit = suit

    # For comparisons between cards
    def __lt__(self, other): return self.int_value < other.int_value
    def __le__(self, other): return self.int_value <= other.int_value
    def __gt__(self, other): return self.int_value > other.int_value
    def __ge__(self, other): return self.int_value >= other.int_value
    def __eq__(self, other): return self.int_value == other.int_value

    # Debug
    def __str__(self) -> str:
        return f'{self.value} of {self.suit}'
    def __repr__(self):
        return str(self)
    
