# This file describes the chessboard class
import numpy as np

WHITE = 0
BLACK = 1
NO_PASSANT = "-"
EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
PIECE_TO_CHAR = ".PNBRQK"


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
    # WHITE: Positive, BLACK: Negative

    def __init__(self, layout: list[int] | None = None):
        if layout is None: 
            self.squares = [0] * 64
        elif len(layout) != 64:
            raise ValueError("The requested layout does not have 64 squares.")
        else:
            self.squares = layout.copy()
        self.turn = WHITE
        self.castling_rights = "KQkq"
        self.en_passant = NO_PASSANT
        self.half_move_clock = 0
        self.full_move_number = 1
        
    def generate_FEN(self):
        #example FEN: "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
        FEN = []
        blank_counter = 0
        for i, square in enumerate(self.squares):
            char = self.piece_to_char(square)
            if char == ".":
                blank_counter += 1
            elif blank_counter > 0:
                FEN.append(str(blank_counter))
                FEN.append(char)
                blank_counter = 0
            else:
                FEN.append(char)
            if (i+1)%8 == 0:
                if blank_counter>0: 
                    FEN.append(str(blank_counter))
                    blank_counter = 0
                FEN.append("/")
        return "".join(FEN).rstrip("/")

    @classmethod
    def empty(cls) -> "Chessboard":
        squares = [0]*64
        return cls(squares)
    
    @classmethod
    def standard(cls) -> "Chessboard":
        squares = [0]*64
        squares[0:8] = [4, 2, 3, 5, 6, 3, 2, 4]
        squares[8:16] = [1, 1, 1, 1, 1, 1,1, 1]
        squares[Chessboard.coords_to_index("a7"):Chessboard.coords_to_index("h7")+1] = [-1]*8 #just another way to define this
        squares[Chessboard.coords_to_index("a8"):Chessboard.coords_to_index("h8")+1] = [-4, -2, -3, -5, -6, -3, -2, -4]
        return cls(squares)

    def print_board(self, flipped: bool = False):
        i = 0
        local_flipped_squares = self.squares
        if flipped:
            local_flipped_squares = self.flip_vertically(local_flipped_squares)
        for char in local_flipped_squares:
            print(char, end="")
            i += 1
            if i >= 8:
                i = 0
                print()
    
    @staticmethod
    def piece_to_char(piece: int) -> str:
        char = PIECE_TO_CHAR[abs(piece)]
        if piece < 0: char = char.lower()
        return char

    @staticmethod
    def flip_vertically(squares: list[int]) -> list[int]:
        if len(squares) != 64:
            raise ValueError("The intput layout does not have 64 squares.")
        
        flippedSquares = [0]*64
        for rank in range(0,8):
            flippedSquares[8*rank:(8*(rank+1))] = squares[(8*(7-rank)):(8*(8-rank))]
        return flippedSquares
        

    def set_square(self, value: int, start_coords: str, end_coords = None):
        start_index = self.coords_to_index(start_coords)
        if end_coords is not None:
            end_index = self.coords_to_index(end_coords)
            if start_index > end_index:
                start_index, end_index = end_index, start_index
            self.squares[start_index:end_index+1] = [value]*(end_index-start_index+1)
        else:
            self.squares[start_index] = value

    @staticmethod
    def get_square_rankrow(i: int):
        rank = i // 8 # Floor division returns row
        row = i % 8 # Remainder returns column
        
        return(rank, row)

    @staticmethod
    def coords_to_index(coords: str) -> int:
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
