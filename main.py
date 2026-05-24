from Chessboard import Chessboard
from stockfish import Stockfish

def main():

    stockfish = Stockfish(path="/Users/frede/Documents/Code Projects/ChessAI/engines/stockfish/stockfish-windows-x86-64-avx2.exe", 
                          depth=18, parameters={"Threads": 4, "Hash": 4096,"Minimum Thinking Time": 100})
    #stockfish = Stockfish(r"C:\Users\frede\Documents\Code Projects\ChessAI\engines\stockfish\stockfish-windows-x86-64-avx2.exe")

    board = Chessboard.standard()
    '''print(board.get_square_rankrow(0))
    print(board.get_square_rankrow(7))
    print(board.get_square_rankrow(8))
    print(board.get_square_rankrow(63))
    print(board.get_square_rankrow(64))'''

    board.set_square(1, "f4")

    board.print_board()
    print()
    board.print_board(True)

    print(stockfish.get_best_move())

    print(f"(13+1)%8: {(13+1)%8}")
    FEN = board.generate_FEN()
    print(FEN)

if __name__ == "__main__":
    main()