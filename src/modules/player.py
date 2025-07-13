import random

list_of_names = ["John", "Mike", "Greg", "Seth", "Peter", "Brad", "Carl", "Albert", "Kathleen"]

class Player:
    """
    Player class is the base for User_Player and AI_Player classes.
    Each player has:
    name --> random or user generated name
    hand --> their current hand
    """
    def __init__(self, name=None, balance=1000):
        self.name = name if name is not None else list_of_names[random.randrange(0, len(list_of_names))]
        self.hand = None
        self.active = True
        self.balance = balance
    
    # Returns player's hand
    def get_hand(self) -> tuple:
        return self.hand
    
    # Updates player's hand
    def new_hand(self, hand: tuple) -> None:
        self.hand = hand

    # Requests player's action
    def action(self, last_raise: int) -> tuple:
        return "check", 0 # temporary placeholder
    
    # Debug
    def __str__(self) -> str:
        return f'{self.name} {self.hand}'
    def __repr__(self):
        return str(self)