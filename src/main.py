#import pygame
from modules.deck import Deck


if __name__ == "__main__":
    deck = Deck()
    print(deck)
    print(50 * "-")

    deck.shuffle()
    print(deck)