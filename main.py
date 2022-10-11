import chess
import chess.svg
import numpy as np
from tensorflow import keras
from keras import models
import fen_to_array as fenArray
import random_fen as randFen

ai = models.load_model('Chess_AI.model')

board = chess.Board()

chess.svg.board(board, squares=chess.SquareSet(chess.BB_DARK_SQUARES & chess.BB_FILE_B), size=350)

def ai_eval(board):
    board_array = fenArray.get_array(board.fen())
    board_array = np.expand_dims(board_array, 0)
    prediction = ai.predict(board_array)[0][0]
    return prediction



def ai_move(board):
    evaluations = []
    moves = []
    for move in board.legal_moves:
        move = str(move).split("(")
        board.push(chess.Move.from_uci(move[0]))
        eval = ai_eval(board)
        evaluations.append(eval)
        moves.append(move[0])
        board.pop()

    highest_value = max(evaluations)
    req_index = evaluations.index(highest_value)
    board.push(chess.Move.from_uci(moves[req_index]))

def random_move():
    possible_moves = []
    for move in board.legal_moves:
        possible_moves.append(move)

    move = str(possible_moves[np.random.randint(0, len(possible_moves))]).split("(")
    board.push(chess.Move.from_uci(move[0]))

# Interface

print("Gamemode: ")
mode = input()

if mode == "random":
    while not board.is_checkmate():
        ai_move(board)
        print(board)
        random_move()
        print(board)
elif mode == "challenge":
    while not board.is_checkmate():
        ai_move(board)
        print(board)
        move_input = input()
        board.push(chess.Move.from_uci(move_input))
        print(board)