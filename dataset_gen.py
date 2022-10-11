from turtle import pos
import chess.engine
import chess
import random_fen as randfen
import fen_to_array as fenArray
from progress import printProgressBar
import numpy

dataset_size = 250000

def create_data():
    # Create the board along with a random position (random fen)
    fen = randfen.random_fen()
    board = chess.Board(fen)

    # Initiate engine
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    def stockfish_evaluation(board, time_limit = 0.01):
        result = engine.analyse(board, chess.engine.Limit(time=time_limit))
        score = result['score'].white().score()
        return score

    # Scoring of position in accordance with stockfish 15
    if board.is_valid():
        score = stockfish_evaluation(board)
    else:
        raise Exception("Position is not vaid")
    
    engine.quit()

    return fenArray.get_array(fen), score

def determine_greatest_abs(list):
    new_list = []
    for value in list:
        new_list.append(abs(value))
    return max(list)


# Rescale all scores between -1 and 1 to be used in the model later on
def scale_scores(scores_list):
    new_list = []
    greatest_score = determine_greatest_abs(scores_list)
    for score in scores_list:
        score /= greatest_score
        new_list.append(score)
    return new_list

positions = []
evaluations = []
# A List of Items
items = list(range(0, dataset_size))
l = len(items)

# Initial call to print 0% progress
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

for i, item in enumerate(items):
    position, evaluation = create_data()
    if not evaluation is None:
        positions.append(position)
        evaluations.append(evaluation)
    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

scaled_evaluations = scale_scores(evaluations)

position_array = numpy.asarray(positions)
evaluation_array = numpy.asarray(scaled_evaluations)

numpy.save("positions", position_array)
numpy.save("evaluations", evaluation_array)

print(evaluation_array)
print(numpy.shape(position_array))
print(numpy.shape(evaluation_array))