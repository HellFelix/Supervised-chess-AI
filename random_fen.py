import chess
import numpy as np

def random_move(board):
    possible_moves = []
    for move in board.legal_moves:
        possible_moves.append(move)

    move = str(possible_moves[np.random.randint(0, len(possible_moves))]).split("(")
    board.push(chess.Move.from_uci(move[0]))

def set_board(board):
    n_moves = np.random.randint(0, 100)
    for _ in range(n_moves):
        if not board.is_game_over():
            random_move(board)
        else:
            break
    return board

def random_fen():
    board = chess.Board()
    return set_board(board).fen()
