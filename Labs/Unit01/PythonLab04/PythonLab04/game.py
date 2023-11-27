"""
A game of Crazy 8s

ATCS 2023-2024
"""

# TODO 1: Import Statements
from deck import Deck
from player import Player

class Game:
    def __init__(self, player_names):
        self.players = [Player(n) for n in player_names]# TODO 2: Initialize players
        self.deck = Deck()
        self.deck.shuffle()
        self.current_player_index = 0
        self.is_game_over = False

        # Select an initial card
        self.current_card = self.deck.deal()

        self.deal_initial_hand()
    
    def deal_initial_hand(self):
        # TODO 3: Deal 5 cards to each player
        for c in range(1):
            for i in range(len(self.players)):
                self.players[i].draw(self.deck.deal())
    
    def is_valid_card(self, card):
        # TODO 4: Determine if the player's chosen card is valid
        return self.current_card.rank == card.rank or self.current_card.suit == card.suit

    """
    Determines if the game is over by checking
    if the current player has any cards left
    """
    def check_game_over(self):
        if not self.players[self.current_player_index].has_cards():
            self.is_game_over = True
            print(self.players[self.current_player_index], "wins!")
    
    """
    Draws a card from the deck
    and adds it to the current player's hand
    then displays the new card to the player
    """
    def draw_card(self):
        card = self.deck.deal()
        if card is not None:
            self.players[self.current_player_index].draw(card)
            print("You've drawn", card)

    def play(self):
        while(not self.is_game_over):
            print(str(self.players[self.current_player_index]) + "'s turn")
            print("The top card is", self.current_card)

            # TODO 5: Complete the play function
            print("You have the following cards in your hand: ")
            self.players[self.current_player_index].show_hand()
            while True:
                index = int(input("Choose a card by selecting an index or enter -1 to draw a card: "))
                if index < 0 or index >= len(self.players[self.current_player_index].hand):
                    self.draw_card()
                    break
                else:
                    c = self.players[self.current_player_index].hand[index]
                    if self.is_valid_card(c):
                        self.current_card = self.players[self.current_player_index].play(index)
                        break
                    else:
                        print("Invalid move.")
                        continue
            self.check_game_over()
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

if __name__ == "__main__":
    # TODO 6: Initialize and play the game
    game = Game(['Sam', 'Opponent'])
    game.play()