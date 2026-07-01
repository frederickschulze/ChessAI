from chessboard import Chessboard
from stockfish import Stockfish
from chessgame import ChessGame
from players import HumanPlayer, StockfishPlayer

def main():

    stockfish = Stockfish(path="/Users/frede/Documents/Code Projects/ChessAI/engines/stockfish/stockfish-windows-x86-64-avx2.exe", 
                          depth=18, parameters={"Threads": 4, "Hash": 4096, "Minimum Thinking Time": 100})
    #stockfish = Stockfish(r"C:\Users\frede\Documents\Code Projects\ChessAI\engines\stockfish\stockfish-windows-x86-64-avx2.exe")

    #board = Chessboard.standard()
    FENexample = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
    board = Chessboard.from_FEN(FENexample)

    #Testing coords and name conversions
    '''print(board.get_square_rankfile(0))
    print(board.get_square_rankfile(7))
    print(board.get_square_rankfile(8))  
    print(board.get_square_rankfile(63))

    print(board.index_to_coords(0))
    print(board.index_to_coords(7))
    print(board.index_to_coords(8))
    print(board.index_to_coords(56))
    print(board.index_to_coords(63))'''
    

    #board.set_square(1, "f4")

    board.print_board(flipped = False, letters = True)
    print()    
    FEN = board.generate_FEN()
    print(f"The FEN generated is: {FEN}")
    print("\nNow making the move bc4, nc6, qf3, qe7, nh3, a6, O-O")
    board.make_move_coords("f1c4")
    board.make_move_coords("b8c6")
    board.make_move_coords("d1f3")
    board.make_move_coords("d8e7")
    board.make_move_coords("g1h3")
    board.make_move_coords("a7a6")
    board.make_move_coords("e1g1")
    board.print_board(letters = True)
    FEN = board.generate_FEN()
    print(f"The FEN generated for my board is: {FEN}")

    stockfish_test = False
    if stockfish_test == True:
        print("This is a test of the stockfish library")
        stockfish.make_moves_from_start(["e2e4", "e7e6", "d2d4", "d7d5"]) #
        print(f"stonkfish after making some moves: {stockfish.get_fen_position()}")
        print(f"stonkfish best move now: {stockfish.get_best_move()}\n")
    '''
    print(f"FEN of stockfish object: {stockfish.get_fen_position()}")
    '''
    test_move_generation = False
    if test_move_generation:
        valid_moves = board.generate_valid_moves()
        print(f"the valid moves of my board are:")
        for move in valid_moves:
            print(f"Piece {board.piece_to_char(board.get_piece_at_index(move[0]))} can move from "
                f"{Chessboard.index_to_coords(move[0])} to {Chessboard.index_to_coords(move[1])} with move type: {move[2]} and promotion {move[3]}")
    
    print("\nTesting the is_attacked() function:")
    coord = "g6"
    print(f"Is {coord} attacked?: {board.is_attacked(Chessboard.coords_to_index(coord), 'w')}\n")
    
    test_chess_notation = True
    if test_chess_notation:
        test_coord = "f5"
        print(f"The board.notation_to_coords('{test_coord}') returns {board.notation_to_coords(test_coord)}")

    play_game_test = False
    if play_game_test:
        player1 = HumanPlayer()
        player2 = StockfishPlayer()
        player3 = StockfishPlayer()
        gameboard = board.standard()
        game = ChessGame(gameboard, player3, player2)
        game.play_game(flip_on_turn=False)

if __name__ == "__main__":
    main()