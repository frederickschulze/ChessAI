from players import *
from chessboard import *
import time

class ChessGame:
    colorDict = {'w': "White", 'b': "Black"}

    def __init__(self, chessboard: Chessboard, white_player: Player, black_player: Player):
        self.white_player = white_player
        self.black_player = black_player
        self.board = chessboard
    
    def play_game(self, millisec_per_turn: int = 300, flip_on_turn: bool = False):
        while True:
            time.sleep(millisec_per_turn/1000)
            if flip_on_turn == False:
                board_flip = False
            else:
                board_flip = True if self.board.turn == BLACK else False
            self.board.print_board(flipped=board_flip, letters = True)
            print()
            legal_moves = self.board.generate_legal_moves()
            if not legal_moves:
                if self.board.is_in_check(self.board.turn):

                    print(f"Checkmate: {self.colorDict[Chessboard.opposite_color(self.board.turn)]} wins!")
                    return
                else:
                    print("Stalemate")
                    return
                break

            if self.board.turn == WHITE:
                move_to_make = self.white_player.choose_move(self.board)
            elif self.board.turn == BLACK:
                move_to_make = self.black_player.choose_move(self.board)
            else: raise ValueError("Invalid board.turn state")
            
            self.board.make_move(move_to_make)

            
