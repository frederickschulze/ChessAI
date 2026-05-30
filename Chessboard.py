# This file describes the chessboard class
import numpy as np
from typing import NamedTuple

WHITE = 'w'
BLACK = 'b'
NO_PASSANT = "-"
EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
PIECE_TO_CHAR = ".PNBRQK"

class Move(NamedTuple):
    start: int
    end: int
    flag: int = 0
    promotion: int = 0

class Chessboard:
    # Storing the state of the chess board essentially as a 64 character list
    # ie board indices looks like
    # 0 1 2 ... 7
    # 8 9 10 .. 15
    # ...
    # ...
    # 56 57 ... 63
    #
    # Blank square: 0
    # Pawn: 1
    # Knight: 2
    # Bishop: 3
    # Rook: 4
    # Queen: 5
    # King: 6
    # WHITE: Positive, BLACK: Negative   

    # makes a board with optional custom layout which is a list of 64 ints
    def __init__(self, layout: list[int] | None = None):
        if layout is None: 
            self.squares = [0] * 64
        elif len(layout) != 64:
            raise ValueError("The requested layout does not have 64 squares.")
        else:
            self.squares = layout.copy()
        self.turn = WHITE
        self.castling_rights = "KQkq"
        self.en_passant_square = NO_PASSANT   
        self.halfmove_clock = 0
        self.fullmove_number = 1

    # makes an empty chessboard
    @classmethod
    def empty(cls) -> "Chessboard":
        squares = [0]*64
        return cls(squares)
    
    #make a board with the standard starting position
    @classmethod
    def standard(cls) -> "Chessboard":
        squares = [0]*64
        squares[0:8] = [-4, -2, -3, -5, -6, -3, -2, -4]
        squares[8:16] = [-1, -1, -1, -1, -1, -1, -1, -1]
        squares[Chessboard.coords_to_index("a2"):Chessboard.coords_to_index("h2")+1] = [1]*8 #just making use of my coords_to_index function
        squares[Chessboard.coords_to_index("a1"):Chessboard.coords_to_index("h1")+1] = [4, 2, 3, 5, 6, 3, 2, 4]
        return cls(squares)

    # generate an FEN from the current board state
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
        
        FEN = "".join(FEN).rstrip("/")
        #print(FEN) #now it has the whole board state
        FEN = FEN + f" {self.turn} {self.castling_rights} {self.en_passant_square} {self.halfmove_clock} {self.fullmove_number}"
        #print(FEN)
        return FEN

    def set_position_from_FEN(self):
        return 0

    
    def generate_valid_moves(self):
        pieces_that_can_moove = []
        indexes_that_can_moove = []
        valid_moves = []
        for i, square in enumerate(self.squares):
            if square == 0 or self.piece_color(square) != self.turn:
                print(i, end=" ") #debugging
            elif self.piece_color(square) == self.turn:
                pieces_that_can_moove.append((self.index_to_coords(i), square)) #debugging
                indexes_that_can_moove.append(i)
                if square == 1: #pawn behavior
                    if self.index_to_rank(i) == 2:
                        print(f"White pawn hasn't moved on: {self.index_to_coords(i)}")
                        if self.squares[i-8]==0:
                            print(f"{i-8} Confirmed blank: {Chessboard.index_to_coords(i-8)}")
                            move = Move(i, i-8, 0, 0)
                            valid_moves.append(move)
                            if self.squares[i-16]==0:
                                print(f"{i-16} Confirmed blank: {Chessboard.index_to_coords(i-16)}")
                                move = Move(i, i-16, 0, 0)
                                valid_moves.append(move)
                        # deal with captures, logic is wrong right now elif self.squares[]<0:
                    if self.index_to_rank(i-7) == (self.index_to_rank(i)-1): #lazy check to ensure attacked square is o   n board
                        print(f"capturable square on {i-7}")
                        if self.squares[i-7] != 0:
                            print(f"Capturable piece on {i-7}")
                            move = Move(i, i-7, 1, 0)
                    if self.index_to_rank(i-9) == (self.index_to_rank(i)-1): #lazy check to ensure attacked square is on board
                        print(f"capturable square on {i-9}")
                        if self.squares[i-9] != 0:
                            print(f"Capturable piece on {i-9}")
                            move = Move(i, i-7, 1, 0)
                           # print(f"{i-16}   Capturable: {Chessboard.index_to_coords{i-16}}")
                           # move = Move(i, i-16, 1, 0)
                           # valid_moves.append(move)
                              
                                
                        
                elif i == 2 : #knight behaviors 
                    continue
                elif i == 3: #bishop behavior
                    continue
                elif i == 4: #rook behavior
                    continue
                elif i == 5: #queen behavior
                    continue
                elif i == 6: #king behavior
                    continue
        #print() #debugging
        print(f"pieces that can move: {pieces_that_can_moove}")
        #deprecated: for i in indexes_that_can_moove:
        print(f"Valid moves: {valid_moves}")
        return valid_moves
      
    def make_move(self):
        return 0

    @staticmethod
    def piece_color(piece: int):
        if piece > 0: return WHITE
        elif piece < 0: return BLACK
        elif piece ==0:raise ValueError("This is an empty square, not a piece")
        else: raise ValueError("How the hek did this happen?")
        return color
    
    # print the board to the terminal
    def print_board(self, flipped: bool = False):
        i = 0
        if flipped:
            local_flipped_squares = self.flip_vertically(self.squares)
        else: local_flipped_squares = self.squares
        for char in local_flipped_squares:
            if char >= 0: print(f" {char}", end="")
            elif char < 0: print(char, end="")
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

    #gives rank and file indexed from 1
    @staticmethod
    def index_to_rankfile(index: int):
        rank = Chessboard.index_to_rank(index)
        file = Chessboard.index_to_file(index) # Remainder returns column
        return(rank, file)
    
    @staticmethod #singular versions of above
    def index_to_rank(index: int):
        if index < 0 or index > 63: raise ValueError("The index is outside of the expected range.")
        rank_reversed = index // 8
        rank = 8 - rank_reversed
        return rank

    @staticmethod #singular versions of above
    def index_to_file(index: int):
        if index < 0 or index > 63:
            raise ValueError("The index is outside of the expected range.")
        file = index % 8 + 1
        return file

    @staticmethod
    def index_to_coords(index: int):
        if index < 0 or index > 63: 
            raise ValueError("The index is outside of the expected range.")
        rank, file = Chessboard.index_to_rankfile(index)
        file_lookup = "abcdefgh"
        file_name = file_lookup[file-1]
        return file_name + str(rank)

    @staticmethod
    def coords_to_index(coords: str) -> int:
        # order goes a8, b8, c8, ... h8, a7, b7, ... g1, h1. 
        fileNames = "abcdefgh"
        rankNames = "87654321"
        
        # input check
        if (not isinstance(coords, str)
            or len(coords) != 2
            or coords[0] not in fileNames
            or coords[1] not in rankNames):
            raise ValueError("The input coords are not in the correct format")
        
        fileNum = fileNames.index(coords[0])
        rankNum = rankNames.index(coords[1])

        overall_index = 8*(rankNum)+fileNum
        return overall_index
    
   

    def set_board_state(self, board: str):
        self.squares = self.squares

    

# Test Script:
