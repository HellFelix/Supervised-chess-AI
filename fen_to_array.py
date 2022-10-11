import chess
import numpy

squares = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
}

def square_to_index(square):
    letter = chess.square_name(square)
    return 8 - int(letter[1]), squares[letter[0]]

def get_array(fen):
    board = chess.Board(fen)

    # 3 dimentional matrix (14x8x8) - i.e an array with 14 8x8 matrices all filled with zeroes
    board_matrix = numpy.zeros((14, 8, 8), dtype=numpy.int8)

    # Populating the arrays - one array for each piece of one type, "1" means there is a piece, "0" means no piece
    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = numpy.unravel_index(square, (8, 8))
            board_matrix[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = numpy.unravel_index(square, (8, 8))
            board_matrix[piece + 5][7 - idx[0]][idx[1]] = 1
    #the last two 8x8 matrices will display the attacked squares by the respecctive sides
    to_move = board.turn # saves the information fo who is to move
    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j  = square_to_index(move.to_square)
        board_matrix[12][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board_matrix[13][i][j] = 1
    board.turn = to_move

    return board_matrix