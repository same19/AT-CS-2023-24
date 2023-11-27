"""
A class representing a deck of cards
"""

import random
# TODO 1: Get the card class
from card import Card

class Deck:
    # TODO 2: Constructor Parameters
    def __init__(self, ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'], suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']):
        self.cards = []
        # Initialize all cards
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        # Pop and return the end card
        if not self.is_empty():
            return self.cards.pop()
        else:
            return None

    # TODO 3: Is the deck empty
    def is_empty(self):
        return len(self.cards)<=0