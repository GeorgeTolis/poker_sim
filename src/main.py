#import pygame
from modules.game import Game
from modules.deck import Deck


if __name__ == "__main__":
    game = Game(3)
    game.play()