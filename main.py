from Chessboard import Chessboard
from stockfish import Stockfish

def main():

    stockfish = Stockfish(path="/Users/frede/Documents/Code Projects/ChessAI/engines/stockfish/stockfish-windows-x86-64-avx2.exe", 
                          depth=18, parameters={"Threads": 4, "Hash": 4096,"Minimum Thinking Time": 100})
    #stockfish = Stockfish(r"C:\Users\frede\Documents\Code Projects\ChessAI\engines\stockfish\stockfish-windows-x86-64-avx2.exe")

    board = Chessboard.standard()
    print(board.get_square_rankfile(0))
    print(board.get_square_rankfile(7))
    print(board.get_square_rankfile(8))  
    print(board.get_square_rankfile(63))

    print(board.index_to_coords(0))
    print(board.index_to_coords(7))
    print(board.index_to_coords(8))
    print(board.index_to_coords(56))
    print(board.index_to_coords(63))
    

    #board.set_square(1, "f4")

    board.print_board(flipped = False)
    print()    
    FEN = board.generate_FEN()
    print(f"FEN of my board object: {FEN}")
    print(f"FEN of stockfish object: {stockfish.get_fen_position()}")
    stockfish.make_moves_from_start(["e2e4", "e7e6"])
    print(f"stonkfish after moving: {stockfish.get_fen_position()}")
    print(f"stonkfish best move now: {stockfish.get_best_move()}")
    

if __name__ == "__main__":
    main()