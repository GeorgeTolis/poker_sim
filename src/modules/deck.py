#import pygame
from .cards import Card
import random

class Deck:
    def __init__(self):
        clubs = [Card(i, "clubs") for i in range(1, 14)]
        diamonds = [Card(i, "diamonds") for i in range(1, 14)]
        hearts = [Card(i, "hearts") for i in range(1, 14)]
        spades = [Card(i, "spades") for i in range(1, 14)]

        self.cards = clubs + diamonds + hearts + spades
    
    def shuffle(self) -> None:
        random.shuffle(self.cards)
        random.shuffle(self.cards)
        random.shuffle(self.cards)

    def __str__(self) -> str:
        return ", ".join(str(card) for card in self.cards)

    def __repr__(self):
        return str(self)
    
