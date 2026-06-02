# This file describes the chessboard class
import numpy as np
from typing import NamedTuple

#Player turn constants
WHITE = 'w'
BLACK = 'b'
#No en passant flag
NO_PASSANT = -1
#Piece constants
EMPTY = 0
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6
#Converting piece integer to chars or back
PIECE_TO_CHAR = ".PNBRQK"
#move flags
NORMAL = 0
CAPTURE = 1
DOUBLE_PAWN = 2
CASTLE = 3
EN_PASSANT = 4
PROMOTION = 5


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
        en_passant_FEN = "-" if self.en_passant_square == NO_PASSANT else self.index_to_coords(self.en_passant_square)
        FEN = FEN + f" {self.turn} {self.castling_rights} {en_passant_FEN} {self.halfmove_clock} {self.fullmove_number}"
        #print(FEN)
        return FEN

    def set_position_from_FEN(self):
        return 0

    '''#Check for en passant
        ep_attacker_left = i-17 #up 2, left 1
        ep_attacker_right = i-15 #up 2, right 1
        for attacker_index in [ep_attacker_left, ep_attacker_right]:
            attacker_pieceint = self.squares[attacker_index]
            if self.index_to_rank(attacker_index) == self.index_to_rank(i)+2: #then potential enemy is on board
                if attacker_pieceint == -square: #then it should be a pawn of the opposite color

                    self.en_passant_square = self.''' 


    def generate_valid_moves(self):
        print0 = False
        print1 = True
        print_moves = False
        pieces_that_can_moove = []
        indexes_that_can_moove = []
        valid_moves = []
        #Test en passant self.en_passant_square = self.coords_to_index("e3")
        for i, square in enumerate(self.squares):
            rank, file = self.index_to_rankfile(i)
            if square == 0 or self.piece_color(square) != self.turn:
                if print0: print(i, end=" ") #debugging
                continue

            elif self.piece_color(square) == self.turn:
                pieces_that_can_moove.append((self.index_to_coords(i), square)) #debugging
                indexes_that_can_moove.append(i)

                if square == 1: #white pawn behavior
                    #checking one forward of pawn
                    if self.squares[i-8] == 0:
                        if print0: print(f"{i-8} Confirmed blank: {self.index_to_coords(i-8)}")
                        valid_moves.append(Move(i, i-8, NORMAL, 0))
                        #if pawn on starting rank and the first square was clear, check 2 forward
                        if rank == 2:
                            if print0: print(f"White pawn hasn't moved on: {self.index_to_coords(i)}")
                            if self.squares[i-16]==0:
                                if print0: print(f"{i-16} Confirmed blank: {self.index_to_coords(i-16)}")
                                move = Move(i, i-16, DOUBLE_PAWN, 0)
                                valid_moves.append(move)

                    # Checking capture to right
                    right_capture = i-7
                    if file != 8: #can't capture right on file 8
                        if print0: print(f"capturable square on {right_capture}")
                        if self.squares[right_capture] < 0:
                            if print0: print(f"Capturable piece on {right_capture}")
                            valid_moves.append(Move(i, right_capture, CAPTURE, 0))
                        elif right_capture == self.en_passant_square:
                            valid_moves.append(Move(i, right_capture, EN_PASSANT, 0))

                    # Checking capture to left
                    left_capture = i-9
                    if file != 1: #can't capture left on file 1
                        if print0: print(f"capturable square on {left_capture}")
                        if self.squares[left_capture] < 0: 
                            if print0: print(f"Capturable piece on {left_capture}")
                            valid_moves.append(Move(i, left_capture, CAPTURE, 0))
                        elif left_capture == self.en_passant_square:
                            valid_moves.append(Move(i, left_capture, EN_PASSANT, 0))
                        
                elif square == 2 : #knight behaviors
                    if print1: print(f"It's {self.turn}'s turn")
                    if print1: print(f"The piece in question is: {self.piece_color(square)}") 
                    knight_move_deltas = [(2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2)]
                    for delta in knight_move_deltas:
                        endrank, endfile = (rank + delta[0], file + delta[1])
                        if 1<=endrank<=8 and 1<=endfile<=8:
                            if print1: print(f"Start pos: {rank},{file},{self.rankfile_to_coords((rank, file))},"
                                             f"moves to {endrank},{endfile},{self.rankfile_to_coords((endrank, endfile))}")
                    continue
                elif square == 3: #bishop behavior  
                    continue
                elif square == 4: #rook behavior
                    continue
                elif square == 5: #queen behavior
                    continue
                elif square == 6: #king behavior
                    continue
                

        #print() #debugging
        print(f"pieces that can move: {pieces_that_can_moove}")
        #deprecated: for i in indexes_that_can_moove:
        print(f"Valid moves: {valid_moves}")
        if print_moves:
            for move in valid_moves:
                print(f"Piece can move from {self.index_to_coords(move[0])} to {self.index_to_coords(move[1])} with move type: {move[2]}")

        return valid_moves
      
    def make_move(self):
        return 0

    @staticmethod
    def piece_color(piece: int):
        if piece > 0: return WHITE
        elif piece < 0: return BLACK
        elif piece == 0: raise ValueError("This is an empty square, not a piece")
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
    
    @staticmethod
    def rankfile_to_coords(rankfile: tuple) -> str:
        rankNames = "12345678"
        fileNames = "abcdefgh"
        
        rankChar = rankNames[rankfile[0]-1]
        fileChar = fileNames[rankfile[1]-1]

        coords = str(fileChar)+str(rankChar)

        return coords

    def set_board_state(self, board: str):
        self.squares = self.squares

    

# Test Script:
