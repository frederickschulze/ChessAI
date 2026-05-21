# This file describes the chessboard class
import numpy as np

WHITE = 0
BLACK = 1

class Chessboard:
    # Storing the state of the chess board essentially as a 64 character list
    # ie board indices looks like
    # 56 57 58 ... 63
    # ...
    # ...
    # 8  9  10 ... 15 
    # 0  1  2  ... 7
    #
    # Blank square: 0
    # Pawn: 1
    # Knight: 2
    # Bishop: 3
    # Rook: 4
    # Queen: 5
    # King: 6

    def __init__(self, layout: list[int]):
        if len(layout) != 64:
            raise ValueError("ValueError: The requested layout does not have 64 squares.")
        else:
            self.squares = layout.copy()
    
    @classmethod
    def empty(cls) -> "Chessboard":
        squares = [0]*64
        return cls(squares)
    
    @classmethod
    def standard(cls) -> "Chessboard":
        squares = [0]*64
        squares[0:8] = [4, 2, 3, 5, 6, 3, 2, 4]
        squares[8:16] = [1, 1, 1, 1, 1, 1,1, 1]
        return cls(squares)

    def print_board(self):
        i = 0
        for char in reversed(self.squares):
            print(char, end="")
            i += 1
            if i >= 8:
                i = 0
                print()


    def set_squares(self, value: int, start_coords: str, end_coords = None):
        start_index = self.get_square_index(start_coords)
        if end_coords is not None:
            end_index = self.get_square_index(end_coords)
            if start_index > end_index:
                start_index, end_index = end_index, start_index
            self.squares[start_index:end_index+1] = [value]*(end_index-start_index+1)
        else:
            self.squares[start_index] = value

    @staticmethod
    def get_square_name(i: int):
        rank = i // 8 # Floor division returns row
        row = i % 8 # Remainder returns column
        return(rank, row)

    @staticmethod
    def get_square_index(coords: str) -> int:
        fileNames = "abcdefgh"
        rankNames = "12345678"
        if (not isinstance(coords, str)
            or len(coords) != 2
            or coords[0] not in fileNames
            or coords[1] not in rankNames):
            raise ValueError("The input coords are not in the correct format")
        
        fileNum = fileNames.index(coords[0])
        rankNum = int(coords[1])

        overall_index = 8*(rankNum-1)+fileNum

        return overall_index
    
        

    def set_board_state(self, board: str):
        self.squares = self.squares
    

# Test Script:
board = Chessboard.standard()
print(board.get_square_name(0))
print(board.get_square_name(7))
print(board.get_square_name(8))
print(board.get_square_name(63))
print(board.get_square_name(64))

board.print_board()

board.set_squares(1, "f4")

board.print_board()