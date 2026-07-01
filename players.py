from chessboard import Chessboard, Move
from stockfish import Stockfish

class Player:
    def choose_move(self, board: Chessboard) -> Move:
        raise NotImplementedError("Called the wrong version of choose_move")
    
class HumanPlayer(Player):
    def choose_move(self, board: Chessboard) -> Move:
        while True:
            move_text = input("Enter move start and end coords format (e2e4, h7h8q, etc): ")
            try:
                move = board.coords_to_Move(move_text)
                return move
            except ValueError as error:
                print(error)
                print("No legal move was found, try again.")

class EnginePlayer(Player): 
    def choose_move(self, board: Chessboard) -> Move:
        raise NotImplementedError()
    
class StockfishPlayer(Player):
    def __init__(self, stockfish: Stockfish | None = None):
        if stockfish == None:
            self.stockfish = Stockfish(path="/Users/frede/Documents/Code Projects/ChessAI/engines/stockfish/stockfish-windows-x86-64-avx2.exe", 
                          depth=18, parameters={"Threads": 4, "Hash": 4096, "Minimum Thinking Time": 100})
        else: self.stockfish = stockfish

    def choose_move(self, board: Chessboard) -> Move:
        current_fen = board.generate_FEN()
        self.stockfish.set_fen_position(current_fen)
        move_coords = self.stockfish.get_best_move()
        if move_coords == None:
            raise ValueError("Stockfish found no best move")
        return board.coords_to_Move(move_coords)