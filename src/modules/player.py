import random

list_of_names = ["John", "Mike", "Greg", "Seth", "Peter", "Brad", "Carl", "Albert", "Kathleen"]

class Player:
    def __init__(self, name):
        self.name = name if name is not None else list_of_names(random.randrange(0, len(list_of_names)))
        self.hand = None
    
    def get_hand(self) -> tuple:
        return self.hand
    
    def new_hand(self, hand: tuple) -> None:
        self.hand = hand