"""
A pared down Tic Tac Toe 
board to practice backtracking.

@author: Ms. Namasivayam
@version: 2023-2024
"""


class TicTacToe:
    # Class Variables
    NUM_ROWS = 3
    NUM_COLS = 3

    def __init__(self):
        # Set up the board to be empty
        self.board = None
        self.reset_game()
        
        # Tracks the number of boards created
        self.board_count = 0

    def reset_game(self):
        """
        Reset the board to be empty
        Set it back to player_1's turn
        """
        self.board = []
        for row in range(self.NUM_ROWS):
            self.board.append(['-', '-', '-'])

        self.player1_turn = True

    def print_board(self):
        """
        Print the board to the console including row and col numbers
        """
        print('\t0\t1\t2')
        for row in range(self.NUM_ROWS):
            print(str(row) + '\t' + '\t'.join(self.board[row]))

    def place_player(self, player, row, col):
        """
        Places the given player at the row and col
        :param player: String player token
        :param row: row number indexed from 0
        :param col: col number indexed from 0
        """
        self.board[row][col] = player
    
    def print_every_board(self, player="X"):
        # Switches players every turn
        next_player = "O" if player=="X" else "X"
        
        # TODO: Complete this function so it 
        # creates every possible game board
        # When completed correctly, board_count
        # should equal 986409
        #19683 unique boards
        # self.print_board()
        self.board_count += 1
        for r in range(self.NUM_ROWS):
            for c in range(self.NUM_COLS):
                if self.board[r][c] == '-':
                    self.place_player(player, r, c)
                    self.print_every_board(next_player)
                    self.place_player('-', r, c)
        

if __name__ == "__main__":
    game = TicTacToe()
    game.print_every_board()
    print(game.board_count)
            