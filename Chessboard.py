# This file describes the chessboard class
import numpy as np
from typing import NamedTuple

#Player's turn constants
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
PROMOTION_CAPTURE = 6

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
    def __init__(self, layout: list[int] | None = None, 
                 turn: str = WHITE, castling_rights: str = "KQkq",
                 en_passant_square: int = NO_PASSANT, 
                 halfmove_clock: int = 0, fullmove_number: int = 1):
        if layout is None: 
            self.squares = [0] * 64
        elif len(layout) != 64:
            raise ValueError("The requested layout does not have 64 squares.")
        else:
            self.squares = layout.copy()
        self.turn = turn
        self.castling_rights = castling_rights
        self.en_passant_square = en_passant_square   
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number

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
    
    @classmethod 
    def from_FEN(cls, FEN: str) -> "Chessboard":
        #example FEN: "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
        squares = cls.get_FEN_squares(FEN)
        turn_fromFEN = FEN.split(" ")[1]
        castling_rights_fromFEN = FEN.split(" ")[2]
        en_passant_square_fromFEN = cls.get_FEN_en_passant(FEN)
        halfmove_clock_fromFEN = int(FEN.split(" ")[4])
        fullmove_number_fromFEN = int(FEN.split(" ")[5])

        return cls(squares, turn_fromFEN, castling_rights_fromFEN, 
                   en_passant_square_fromFEN, halfmove_clock_fromFEN, fullmove_number_fromFEN)

    @staticmethod
    def get_FEN_squares(FEN: str) -> list[int]:
    #example FEN: "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
        FEN_squares = FEN.split(" ")[0] #returns just the board portion
        squareList = [0] * 64
        square_index = 0
        for letter in FEN_squares:
            if letter.upper() in "PNBRQK":
                num = Chessboard.char_to_int(letter)
                squareList[square_index] = num
                square_index += 1
            elif letter.isdigit():
                square_index += int(letter)

            elif letter == '/': #debugging check for now that will not be needed later
                if square_index % 8 != 0: raise ValueError("You're calculating this wrong")
            else: raise ValueError(f"Unexpected FEN character: {letter}")
        if square_index != 64: raise ValueError("Did not receive the expected amount of squares")
        return squareList

    #bunch of not very-useful helper functions
    @staticmethod
    def get_FEN_turn(FEN: str) -> str:
    #example FEN: "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
        turn_fromFEN = FEN.split(" ")[1]
        return turn_fromFEN
    @staticmethod
    def get_FEN_castling_rights(FEN: str) -> str:
        castling_rights_from_FEN = FEN.split(" ")[2]
        if castling_rights_from_FEN == "-": castling_rights_from_FEN = ""
        return castling_rights_from_FEN
    @staticmethod # this might be the most useful helper function
    def get_FEN_en_passant(FEN: str) -> int:
        en_passant_from_FEN_coords = FEN.split(" ")[3]
        if en_passant_from_FEN_coords == "-": return NO_PASSANT
        else: en_passant_from_FEN_index = Chessboard.coords_to_index(en_passant_from_FEN_coords)
        return en_passant_from_FEN_index
    @staticmethod
    def get_FEN_halfmove_clock(FEN: str) -> int:
        halfmove_clock_from_FEN = FEN.split(" ")[4]
        halfmove_clock_from_FEN = int(halfmove_clock_from_FEN)
        return halfmove_clock_from_FEN
    @staticmethod
    def get_FEN_fullmove_number(FEN: str) -> int:
        fullmove_number_from_FEN = FEN.split(" ")[5]
        fullmove_number_from_FEN = int(fullmove_number_from_FEN)
        return fullmove_number_from_FEN

    def set_position_from_FEN(self):
    #example FEN: "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
        return 0
    
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
            if (i+1) % 8 == 0:
                if blank_counter>0: 
                    FEN.append(str(blank_counter))
                    blank_counter = 0
                FEN.append("/")
        
        FEN = "".join(FEN).rstrip("/")
        #print(FEN) #now it has the whole board state
        en_passant_FEN = "-" if self.en_passant_square == NO_PASSANT else self.index_to_coords(self.en_passant_square)
        castling_rights_FEN = self.castling_rights if self.castling_rights else "-"
        FEN = FEN + f" {self.turn} {castling_rights_FEN} {en_passant_FEN} {self.halfmove_clock} {self.fullmove_number}"
        #print(FEN)
        return FEN


    def generate_psueod_valid_moves(self):
        print0 = False
        print1 = False
        print_moves = True
        valid_moves = []

        #Test en passant self.en_passant_square = self.coords_to_index("e3")
        for i, square in enumerate(self.squares):
            if square == 0:
                if print0: print(i, end=" ") #debugging
                continue
            current_piece_color = self.piece_color(square)
            if current_piece_color != self.turn:
                if print0: print(i, end=" ") #debugging
                continue

            rank, file = self.index_to_rankfile(i)

            # PAWN BEHAVIOR
            if abs(square) == PAWN: #white pawn behavior
                #checking one forward of pawn
                if current_piece_color == WHITE: one_forward_square = i-8
                elif current_piece_color == BLACK: one_forward_square = i+8
                else: raise ValueError("The piece color is not working")

                #if self.index_to_rank(target_square) != rank + 1: raise ValueError("Pawn did not move correctly???")
                if current_piece_color == WHITE and rank == 8: raise ValueError("You shouldn't have a pawn on this rank!!!")
                elif current_piece_color == BLACK and rank == 1: raise ValueError("You shouldn't have a pawn on this rank!!!")                    
                if self.squares[one_forward_square] == 0:
                    if (current_piece_color == WHITE and rank == 7) or (current_piece_color == BLACK and rank == 2):
                        if print0: print(f"{one_forward_square} Confirmed blank promotion: {self.index_to_coords(one_forward_square)}")
                        for promotional_piece in [KNIGHT, BISHOP, ROOK, QUEEN]:
                            valid_moves.append(Move(i, one_forward_square, PROMOTION, promotional_piece))
                    else:
                        valid_moves.append(Move(i, one_forward_square, NORMAL, 0))
                    #if pawn on starting rank and the first square was clear, check 2 forward
                    if (current_piece_color == WHITE and rank == 2) or (current_piece_color == BLACK and rank == 7):
                        if print0: print(f"White pawn hasn't moved on: {self.index_to_coords(i)}")
                        two_forward_square = i-16 if current_piece_color == WHITE else i + 16
                        if self.squares[two_forward_square] == 0:
                            if print0: print(f"{two_forward_square} Confirmed blank: {self.index_to_coords(two_forward_square)}")
                            valid_moves.append(Move(i, two_forward_square, DOUBLE_PAWN, 0))

                # Checking captures to right and left
                plusfile_capture = i-7 if current_piece_color == WHITE else i+9 #assumes piece is black if not white
                negfile_capture = i-9 if current_piece_color == WHITE else i+7 
                potential_captures = []
                if file != 8: potential_captures.append(plusfile_capture)
                if file != 1: potential_captures.append(negfile_capture)

                for capture_index in potential_captures:
                    if print0: print(f"capturable square on {capture_index}")
                    if self.squares[capture_index] != 0: 
                        if self.piece_color(self.squares[capture_index]) != current_piece_color:
                            if print0: print(f"Capturable piece on {capture_index}")
                            if (current_piece_color == WHITE and rank == 7) or (current_piece_color == BLACK and rank == 2):
                                for promotional_piece in [KNIGHT, BISHOP, ROOK, QUEEN]:
                                    valid_moves.append(Move(i, capture_index, PROMOTION_CAPTURE, promotional_piece))
                            else:
                                valid_moves.append(Move(i, capture_index, CAPTURE, 0))
                    elif capture_index == self.en_passant_square:
                        valid_moves.append(Move(i, capture_index, EN_PASSANT, 0))

            # KNIGHT BEHAVIOR
            elif abs(square) == KNIGHT:
                if print1: print(f"It's {self.turn}'s turn")
                if print1: print(f"The acctive piece's color is: {self.piece_color(square)}") 
                knight_move_deltas = [(2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2)]

                for delta in knight_move_deltas: #finding final move positions and checking if on board
                    endrank, endfile = (rank + delta[0], file + delta[1])
                    if 1<=endrank<=8 and 1<=endfile<=8: 
                        if print1: print("Knight move stays on board with:")
                        if print1: print(f"Start pos: ({rank},{file},{self.rankfile_to_coords((rank, file))}) "
                                            f"moves to ({endrank},{endfile},{self.rankfile_to_coords((endrank, endfile))})")
                        knight_move_index_delta = -8*delta[0] + delta[1] # convert from rank and file to index 
                        finalIndex = i + knight_move_index_delta
                        target_piece = self.squares[finalIndex]
                        if target_piece == EMPTY:
                            valid_moves.append(Move(i, finalIndex, NORMAL, 0))
                        elif self.piece_color(target_piece) != current_piece_color: #the only thing that changed to generalize to both colors
                            valid_moves.append(Move(i, finalIndex, CAPTURE, 0))

            # ALL BISHOP BEHAVIOR
            elif abs(square) == BISHOP: 
                #check northwest squares
                directions = [(1,1), (1,-1), (-1,-1), (-1,1)]
                for delta in directions:
                    hit = False
                    cur_rank = rank
                    cur_file = file
                    #valid_bishop_indices = []
                    while not hit: 
                        #rank and file variables
                        new_rank = cur_rank + delta[0]
                        new_file = cur_file + delta[1]
                        if 1<=new_rank<=8 and 1<=new_file<=8: #limits within board
                            valid_index = self.rankfile_to_index(new_rank, new_file)
                            target_piece = self.squares[valid_index]
                            
                            if target_piece == EMPTY:
                                valid_moves.append(Move(i, valid_index, NORMAL, 0))
                                cur_rank = new_rank
                                cur_file = new_file
                            else:
                                target_piece_color = self.piece_color(target_piece)
                                if target_piece_color == current_piece_color:
                                    hit = True
                                else: #assume opposite piece color
                                    valid_moves.append(Move(i, valid_index, CAPTURE, 0))
                                    hit = True  
                        else: #the board limits were reached
                            hit = True

            # ALL ROOK BEHAVIOR
            elif abs(square) == ROOK: 
                #check northwest squares
                directions = [(0,1), (1,0), (0,-1), (-1,0)]
                for delta in directions:
                    hit = False
                    cur_rank = rank
                    cur_file = file
                    #valid_bishop_indices = []
                    while not hit: 
                        #rank and file variables
                        new_rank = cur_rank + delta[0]
                        new_file = cur_file + delta[1]
                        if 1<=new_rank<=8 and 1<=new_file<=8: #limits within board
                            valid_index = self.rankfile_to_index(new_rank, new_file)
                            target_piece = self.squares[valid_index]
                            
                            if target_piece == EMPTY:
                                valid_moves.append(Move(i, valid_index, NORMAL, 0))
                                cur_rank = new_rank
                                cur_file = new_file
                            else:
                                target_piece_color = self.piece_color(target_piece)
                                if target_piece_color == current_piece_color:
                                    hit = True
                                else: #assume opposite piece color
                                    valid_moves.append(Move(i, valid_index, CAPTURE, 0))
                                    hit = True  
                        else: #the board limits were reached
                            hit = True  

            # ALL QUEEN BEHAVIOR
            elif abs(square) == QUEEN: 
                #check northwest squares
                directions = [(1,1), (1,-1), (-1,-1), (-1,1), (0,1), (1,0), (0,-1), (-1,0)]
                for delta in directions:
                    hit = False
                    cur_rank = rank
                    cur_file = file
                    #valid_bishop_indices = []
                    while not hit: 
                        #rank and file variables
                        new_rank = cur_rank + delta[0]
                        new_file = cur_file + delta[1]
                        if 1<=new_rank<=8 and 1<=new_file<=8: #limits within board
                            valid_index = self.rankfile_to_index(new_rank, new_file)
                            target_piece = self.squares[valid_index]
                            
                            if target_piece == EMPTY:
                                valid_moves.append(Move(i, valid_index, NORMAL, 0))
                                cur_rank = new_rank
                                cur_file = new_file
                            else:
                                target_piece_color = self.piece_color(target_piece)
                                if target_piece_color == current_piece_color:
                                    hit = True
                                else: #assume opposite piece color
                                    valid_moves.append(Move(i, valid_index, CAPTURE, 0))
                                    hit = True  
                        else: #the board limits were reached
                            hit = True  

            # KING BEHAVIOR
            elif abs(square) == KING: 
                directions = [(1,1), (1,-1), (-1,-1), (-1,1), (0,1), (1,0), (0,-1), (-1,0)]
                for delta in directions:
                    new_rank = rank + delta[0]
                    new_file = file + delta[1]

                    if 1<=new_rank<=8 and 1<=new_file<=8: # ensure new square is on board
                        valid_index = self.rankfile_to_index(new_rank, new_file)
                        target_piece = self.squares[valid_index]

                        if target_piece == EMPTY:
                            valid_moves.append(Move(i, valid_index, NORMAL, 0))
                        else:
                            target_piece_color = self.piece_color(target_piece)
                            if target_piece_color == current_piece_color: 
                                continue
                            else: #assume opposite piece color
                                valid_moves.append(Move(i, valid_index, CAPTURE, 0))
            
        #print() #debugging
        #print(f"pieces that can move: {pieces_that_can_moove}")
        if print_moves:
            for move in valid_moves:
                print(f"Piece {self.piece_to_char(self.squares[move[0]])} can move from "
                        f"{self.index_to_coords(move[0])} to {self.index_to_coords(move[1])} with move type: {move[2]}")
        return valid_moves
      

    #def make_move(self, start_i, target_i):
    #    self.squares[target_i] = self.squares[start_i]
    #    self.squares[start_i] = 0

    def make_move(self, move_deets: Move):
        start_i = move_deets.start
        end_i = move_deets.end
        move_type = move_deets.flag
        promotion_piece = move_deets.promotion

        self.en_passant_square = NO_PASSANT #only gets reassigned if there's a double pawn move

        if move_type == NORMAL or move_type == CAPTURE:
            self.squares[end_i] = self.squares[start_i]
            self.squares[start_i] = EMPTY

        elif move_type == DOUBLE_PAWN:
            self.squares[end_i] = self.squares[start_i]
            self.squares[start_i] = EMPTY
            self.en_passant_square = (start_i + end_i) // 2

        elif move_type == CASTLE:
            self.squares[end_i] = self.squares[start_i]
            self.squares[start_i] = EMPTY
            rook_start_i = start_i + 3 if end_i > start_i else start_i - 4 #end_i > start_i for king side castling
            rook_destination_i = (start_i + end_i) // 2
            self.squares[rook_destination_i] = self.squares[rook_start_i]
            self.squares[rook_start_i] = EMPTY

        elif move_type == EN_PASSANT:
            self.squares[end_i] = self.squares[start_i]
            self.squares[start_i] = 0
            if self.turn == BLACK: taken_index = end_i - 8
            else: taken_index = end_i+8 #self.turn == WHITE
            self.squares[taken_index] = EMPTY

        elif move_type == PROMOTION:
            print("need to work ont this ")
    
    @staticmethod
    def piece_color(piece: int):
        if piece > 0: return WHITE
        elif piece < 0: return BLACK
        elif piece == 0: raise ValueError("This is an empty square, not a piece")
        else: raise ValueError("How the hek did this happen?")
    
    @staticmethod
    def opposite_color(color: str) -> str:
        if color == WHITE: return BLACK
        elif color == BLACK: return WHITE
        else: raise ValueError("Unexpected input value. Input WHITE ('w') or BLACK ('b')")
    
    # print the board to the terminal
    def print_board(self, flipped: bool = False, letters: bool = False):
        if flipped: local_flipped_squares = self.flip_vertically(self.squares)
        else: local_flipped_squares = self.squares

        for i, piece_num in enumerate(local_flipped_squares):
            if letters == False:
                if piece_num >= 0: print(f" {piece_num}", end="")
                elif piece_num < 0: print(piece_num, end="")
            else:
                print(f"{self.piece_to_char(piece_num)} ", end="")
            if (i+1) % 8 == 0:
                print()
    
    @staticmethod
    def piece_to_char(piece: int) -> str:
        char = PIECE_TO_CHAR[abs(piece)]
        if piece < 0: char = char.lower()
        return char
    
    @staticmethod
    def char_to_int(char: str) -> int:
        #PIECE_TO_CHAR = ".PNBRQK"
        if char.upper() not in PIECE_TO_CHAR:
            raise ValueError("The input character is not in PIECE_TO_CHAR (.PNBRQK)")
        piece_integer = PIECE_TO_CHAR.index(char.upper())
        if char.islower(): piece_integer = -piece_integer
        return piece_integer

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
    def rankfile_to_index(rank: int, file: int) -> int:
        if not (1 <= rank <= 8 and 1 <= file <= 8): raise ValueError("Rank and file must both be in the range 1 to 8.")
        index = 8*(8 - rank) + (file - 1)
        return index
    
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

### Old deprecated stuff: 
'''             
# WHITE PAWN BEHAVIOR
if square == 1: #white pawn behavior
    #checking one forward of pawn
    target_square = i-8
    if self.index_to_rank(target_square) != rank + 1: raise ValueError("Pawn did not move correctly???")
    if rank == 8: raise ValueError("How do you have a pawn on the 8th rank???")                    
    if self.squares[target_square] == 0:
        if self.index_to_rank(target_square) != 8:
            if print0: print(f"{target_square} Confirmed blank: {self.index_to_coords(i-8)}")
            valid_moves.append(Move(i, target_square, NORMAL, 0))
        else:
            if print0: print(f"{target_square} Confirmed blank: {self.index_to_coords(i-8)}")
            valid_moves.append(Move(i, target_square, PROMOTION, 0))
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
                            
                            
# WHITE KNIGHT BEHAVIOR (nice guy)
elif square == 2 : 
    if print1: print(f"It's {self.turn}'s turn")
    if print1: print(f"The piece in question is: {self.piece_color(square)}") 
    knight_move_deltas = [(2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2)]
    #knight_move_deltas_index = [-15, -17, -6, 10, 17, 15, 6, -10]

    for delta in knight_move_deltas: #finding final move positions and checking if on board
        endrank, endfile = (rank + delta[0], file + delta[1])
        if 1<=endrank<=8 and 1<=endfile<=8: 
            if print1: print("Knight move stays on board with:")
            if print1: print(f"Start pos: ({rank},{file},{self.rankfile_to_coords((rank, file))}) "
                                f"moves to ({endrank},{endfile},{self.rankfile_to_coords((endrank, endfile))})")
                
            knight_move_index_delta = -8*delta[0] + delta[1] # convert from rank and file to index 
            finalIndex = i + knight_move_index_delta
            if self.squares[finalIndex] == 0:
                valid_moves.append(Move(i, finalIndex, NORMAL, 0))
            elif self.squares[finalIndex] < 0:
                valid_moves.append(Move(i, finalIndex, 1, 0))
                
#  WHITE BISHOP BEHAVIOR
elif abs(square) == BISHOP: 
    #check northwest squares
    directions = [(1,1), (1,-1), (-1,-1), (-1,1)]
    for delta in directions:
        hit = False
        cur_rank = rank
        cur_file = file
        #valid_bishop_indices = []
        while not hit: 
            #rank and file variables
            new_rank = cur_rank + delta[0]
            new_file = cur_file + delta[1]
            if 1<=new_rank<=8 and 1<=new_file<=8: #limits within board
                valid_index = self.rankfile_to_index(new_rank, new_file)
                
                if self.squares[valid_index] > 0:
                    hit = True
                elif self.squares[valid_index] == 0:
                    valid_moves.append(Move(i, valid_index, NORMAL, 0))
                    cur_rank = new_rank
                    cur_file = new_file
                elif self.squares[valid_index] < 0:
                    valid_moves.append(Move(i, valid_index, CAPTURE, 0))
                    hit = True  
            else: #the board limits were reached
                hit = True
                


            #WHITE ROOK BEHAVIOR
            elif square == 4: #rook behavior
                directions = [(0,1), (1,0), (0,-1), (-1,0)]
                for delta in directions:
                    hit = False
                    cur_rank = rank
                    cur_file = file
                    #valid_bishop_indices = []
                    while not hit: 
                        #rank and file variables
                        new_rank = cur_rank + delta[0]
                        new_file = cur_file + delta[1]
                        if 1<=new_rank<=8 and 1<=new_file<=8: #limits within board
                            valid_index = self.rankfile_to_index(new_rank, new_file)
                            if self.squares[valid_index] > 0:
                                hit = True
                            elif self.squares[valid_index] == 0:
                                valid_moves.append(Move(i, valid_index, NORMAL, 0))
                                cur_rank = new_rank
                                cur_file = new_file
                            elif self.squares[valid_index] < 0:
                                valid_moves.append(Move(i, valid_index, CAPTURE, 0))
                                hit = True  
                        else: #the board limits were reached
                            hit = True  

            #WHITE QUEEN BEHVAIOR
            elif square == 5: 
                directions = [(1,1), (1,-1), (-1,-1), (-1,1), (0,1), (1,0), (0,-1), (-1,0)]
                for delta in directions:
                    hit = False
                    cur_rank = rank
                    cur_file = file
                    #valid_bishop_indices = []
                    while not hit: 
                        #rank and file variables
                        new_rank = cur_rank + delta[0]
                        new_file = cur_file + delta[1]
                        if 1<=new_rank<=8 and 1<=new_file<=8: #limits within board
                            valid_index = self.rankfile_to_index(new_rank, new_file)
                            if self.squares[valid_index] > 0:
                                hit = True
                            elif self.squares[valid_index] == 0:
                                valid_moves.append(Move(i, valid_index, NORMAL, 0))
                                cur_rank = new_rank
                                cur_file = new_file
                            elif self.squares[valid_index] < 0:
                                valid_moves.append(Move(i, valid_index, CAPTURE, 0))
                                hit = True  
                        else: #the board limits were reached
                            hit = True  

            # WHITE KING BEHAVIOR
            elif square == 6: 
                directions = [(1,1), (1,-1), (-1,-1), (-1,1), (0,1), (1,0), (0,-1), (-1,0)]
                for delta in directions:
                    cur_rank = rank
                    cur_file = file
                    new_rank = cur_rank + delta[0]
                    new_file = cur_file + delta[1]

                    if 1<=new_rank<=8 and 1<=new_file<=8: # ensure new square is on board
                        valid_index = self.rankfile_to_index(new_rank, new_file)
                        if self.squares[valid_index] > 0:
                            hit = True
                        elif self.squares[valid_index] == 0:
                            valid_moves.append(Move(i, valid_index, NORMAL, 0))
                            cur_rank = new_rank
                            cur_file = new_file
                        elif self.squares[valid_index] < 0:
                            valid_moves.append(Move(i, valid_index, CAPTURE, 0))
                            hit = True  
                    else: #the board limits were reached
                        hit = True  

'''