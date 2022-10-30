import numpy as np
import pygame
import os

class Piece:
    def __init__(self, colour, image, number, pos, can_en_passent, has_moved):
        self.colour = colour
        self.image = image
        self.number = number
        self.pos = pos
        self.can_en_passent = can_en_passent
        self.has_moved = has_moved
        self.can_capture = False

class Colour:
    def __init__(self, is_check, is_checkmate):
        self.is_check = is_check
        self.is_checkmate = is_checkmate

white = Colour(False, False)
black = Colour(False, False)

# Board representation
board = np.zeros((8, 8), dtype=np.int32)

# Starting position (dict will change as pieces move)
position = {
            (0, 0): Piece("black", "b_rook.png", 12, None, False, False), (0, 1): Piece("black", "b_knight.png", 13, None, False, False), (0, 2): Piece("black", "b_bishop.png", 14, None, False, False), (0, 3): Piece("black", "b_queen.png", 15, None, False, False), (0, 4): Piece("black", "b_king.png", 16, None, False, False), (0, 5): Piece("black", "b_bishop.png", 14, None, False, False), (0, 6): Piece("black", "b_knight.png", 13, None, False, False), (0, 7): Piece("black", "b_rook.png", 12, None, False, False),
            (1, 0): Piece("black", "b_pawn.png", 11, None, False, False), (1, 1): Piece("black", "b_pawn.png", 11, None, False, False), (1, 2): Piece("black", "b_pawn.png", 11, None, False, False), (1, 3): Piece("black", "b_pawn.png", 11, None, False, False), (1, 4): Piece("black", "b_pawn.png", 11, None, False, False), (1, 5): Piece("black", "b_pawn.png", 11, None, False, False), (1, 6): Piece("black", "b_pawn.png", 11, None, False, False), (1, 7): Piece("black", "b_pawn.png", 11, None, False, False),
            (2, 0): 0, (2, 1): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (2, 6): 0, (2, 7): 0,
            (3, 0): 0, (3, 1): 0, (3, 2): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (3, 6): 0, (3, 7): 0,
            (4, 0): 0, (4, 1): 0, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0, (4, 6): 0, (4, 7): 0,
            (5, 0): 0, (5, 1): 0, (5, 2): 0, (5, 3): 0, (5, 4): 0, (5, 5): 0, (5, 6): 0, (5, 7): 0,
            (6, 0): Piece("white", "w_pawn.png", 1, None, False, False), (6, 1): Piece("white", "w_pawn.png", 1, None, False, False), (6, 2): Piece("white", "w_pawn.png", 1, None, False, False), (6, 3): Piece("white", "w_pawn.png", 1, None, False, False), (6, 4): Piece("white", "w_pawn.png", 1, None, False, False), (6, 5): Piece("white", "w_pawn.png", 1, None, False, False), (6, 6): Piece("white", "w_pawn.png", 1, None, False, False), (6, 7): Piece("white", "w_pawn.png", 1, None, False, False),
            (7, 0): Piece("white", "w_rook.png", 2, None, False, False), (7, 1): Piece("white", "w_knight.png", 3, None, False, False), (7, 2): Piece("white", "w_bishop.png", 4, None, False, False), (7, 3): Piece("white", "w_queen.png", 5, None, False, False), (7, 4): Piece("white", "w_king.png", 6, None, False, False), (7, 5): Piece("white", "w_bishop.png", 4, None, False, False), (7, 6): Piece("white", "w_knight.png", 3, None, False, False), (7, 7): Piece("white", "w_rook.png", 2, None, False, False)
            }

def set_board():
    # set position
    for key in position:
        if position[key] != 0:
            piece_rep = position[key].number
        else:
            piece_rep = 0
        board[key[0]][key[1]] = piece_rep

    # sets piece.pos to the assigned position
    for key in position:
        if position[key] != 0:
            position[key].pos = key

# set starting position
set_board()

# movement rules for pawn, returns a list of all possible squares the pawn can go to - note: this function will only be called upon after the piece type has been determined
def possible_moves_pawn(square):
    possible_moves = []
    # "self" being the pice in question based on the provided square
    self = position[square] 
    if self.colour == "white":
        if position[(self.pos[0]-1, self.pos[1])] == 0:
            # normal movement for pawn
            possible_moves.append((self.pos[0]-1, self.pos[1]))
            if self.pos[0] == 6:
                # can move two squares if on starting square
                if position[(self.pos[0]-2, self.pos[1])] == 0:
                    possible_moves.append((self.pos[0]-2, self.pos[1]))

        # if there is a black piece directly down-right or down-left, the square is added to can_go
        if self.pos[1] != 0: # don't allow pawn to capture outside of board lol
            if position[(self.pos[0]-1, self.pos[1]-1)] != 0 and position[(self.pos[0]-1, self.pos[1]-1)].colour == "black":
                possible_moves.append((self.pos[0]-1, self.pos[1]-1))
            # en passent rule - in move mechanic, pawns are given a can_en_passent = True if they are moved two squares
            if position[(self.pos[0], self.pos[1]-1)] != 0 and position[(self.pos[0], self.pos[1]-1)].can_en_passent:
                possible_moves.append((self.pos[0]-1, self.pos[1]-1))
        if self.pos[1] != 7: # don't allow pawn to capture outside of board lol
            if position[(self.pos[0]-1, self.pos[1]+1)] != 0 and position[(self.pos[0]-1, self.pos[1]+1)].colour == "black":
                possible_moves.append((self.pos[0]-1, self.pos[1]+1))
            # en passent rule - in move mechanic, pawns are given a can_en_passent = True if they are moved two squares
            if position[(self.pos[0], self.pos[1]+1)] != 0 and position[(self.pos[0], self.pos[1]+1)].can_en_passent:
                possible_moves.append((self.pos[0]-1, self.pos[1]+1))

    elif self.colour == "black":
        if position[(self.pos[0]+1, self.pos[1])] == 0:
            # normal movement for pawn
            possible_moves.append((self.pos[0]+1, self.pos[1]))
            if self.pos[0] == 1:
                # can move two squares if on starting square
                if position[(self.pos[0]+2, self.pos[1])] == 0:
                    possible_moves.append((self.pos[0]+2, self.pos[1]))

        # if there is a white piece directly up-right or up-left, the square is added to can_go
        if self.pos[1] != 0:
            if position[(self.pos[0]+1, self.pos[1]-1)] != 0 and position[(self.pos[0]+1, self.pos[1]-1)].colour == "white":
                possible_moves.append((self.pos[0]+1, self.pos[1]-1))
            # en passent
            if position[(self.pos[0], self.pos[1]-1)] != 0 and position[(self.pos[0], self.pos[1]-1)].can_en_passent:
                possible_moves.append((self.pos[0]+1, self.pos[1]-1))
        if self.pos[1] != 7:
            if position[(self.pos[0]+1, self.pos[1]+1)] != 0 and position[(self.pos[0]+1, self.pos[1]+1)].colour == "white":
                possible_moves.append((self.pos[0]+1, self.pos[1]+1))
            # en passent
            if position[(self.pos[0], self.pos[1]+1)] != 0 and position[(self.pos[0], self.pos[1]+1)].can_en_passent:
                possible_moves.append((self.pos[0]+1, self.pos[1]+1))
    return possible_moves

# Logic - see possible_moves_pawn(square), logic is all the same
def possible_moves_rook(square):
    possible_moves = []
    self = position[square]

    # squares to the left - adds all the squares in a straight line right of the piece until it we hit the edge or stumble across another piece
    occupied = False
    i = 1
    while not occupied and self.pos[1]-i >= 0:
        possible_moves.append((self.pos[0], self.pos[1]-i))
        if position[(self.pos[0], self.pos[1]-i)] != 0:
            occupied = True
        i += 1

    # squares to the right
    occupied = False
    i = 1
    while not occupied and self.pos[1]+i <= 7:
        possible_moves.append((self.pos[0], self.pos[1]+i))
        if position[(self.pos[0], self.pos[1]+i)] != 0:
            occupied = True
        i += 1

    # squares upward
    occupied = False
    i = 1
    while not occupied and self.pos[0]-i >= 0:
        possible_moves.append((self.pos[0]-i, self.pos[1]))
        if position[(self.pos[0]-i, self.pos[1])] != 0:
            occupied = True
        i += 1

    # squares upward
    occupied = False
    i = 1
    while not occupied and self.pos[0]+i <= 7:
        possible_moves.append((self.pos[0]+i, self.pos[1]))
        if position[(self.pos[0]+i, self.pos[1])] != 0:
            occupied = True
        i += 1

    return possible_moves

# Logic - see possible_moves_pawn(square), logic is all the same
def possible_moves_knight(square):
    possible_moves = []
    self = position[square]
    # The squares a horse can go to is always the same relative to its position - all these squares are added to possible_squares
    possible_squares = [(self.pos[0]+2, self.pos[1]+1), (self.pos[0]+2, self.pos[1]-1), (self.pos[0]+1, self.pos[1]+2), (self.pos[0]+1, self.pos[1]-2), 
                        (self.pos[0]-1, self.pos[1]+2), (self.pos[0]-1, self.pos[1]-2), (self.pos[0]-2, self.pos[1]+1), (self.pos[0]-2, self.pos[1]-1)]
    for square in possible_squares:
        # Remove the square if outside the bounds of the board
        if square[0] >= 0 and square[0] <= 7 and square[1] >= 0 and square[1] <= 7:
            possible_moves.append(square)
    return possible_moves

# Logic - see possible_moves_pawn(square), logic is all the same
def possible_moves_bishop(square):
    possible_moves = []
    self = position[square]

    # down-right diagonal - adds all the squares in a straight diagonal in the downwards-right direction
    occupied = False
    i = 1
    while not occupied and self.pos[0]+i <= 7 and self.pos[1]+i <=7:
        possible_moves.append((self.pos[0]+i, self.pos[1]+i))
        if position[(self.pos[0]+i, self.pos[1]+i)] != 0:
            occupied = True
        i += 1

    # up-right diagonal
    occupied = False
    i = 1
    while not occupied and self.pos[0]-i >= 0 and self.pos[1]+i <=7:
        possible_moves.append((self.pos[0]-i, self.pos[1]+i))
        if position[(self.pos[0]-i, self.pos[1]+i)] != 0:
            occupied = True
        i += 1

    # down-left diagonal
    occupied = False
    i = 1
    while not occupied and self.pos[0]+i <= 7 and self.pos[1]-i >=0:
        possible_moves.append((self.pos[0]+i, self.pos[1]-i))
        if position[(self.pos[0]+i, self.pos[1]-i)] != 0:
            occupied = True
        i += 1

    # up-left diagonal
    occupied = False
    i = 1
    while not occupied and self.pos[0]-i >= 0 and self.pos[1]-i >=0:
        possible_moves.append((self.pos[0]-i, self.pos[1]-i))
        if position[(self.pos[0]-i, self.pos[1]-i)] != 0:
            occupied = True
        i += 1

    return possible_moves

# Logic - see possible_moves_pawn(square), logic is all the same
def possible_moves_king(square):
    possible_moves = []
    self = position[square]
    attacked = []
    for s in position:
        if position[s] != 0:
            if position[s].colour != position[square].colour:
                # to avoid recursion - the case of "king" is treated separately, also pawns are handled separately because their capture mechamic is different
                if not "king" in position[s].image and not "pawn" in position[s].image:
                    for attacked_square in can_go(s):
                        attacked.append(attacked_square)
                elif "king" in position[s].image:
                    opp_king = position[s]
                    attacked += [(opp_king.pos[0], opp_king.pos[1]+1), (opp_king.pos[0]-1, opp_king.pos[1]+1), (opp_king.pos[0]-1, opp_king.pos[1]), (opp_king.pos[0]-1, opp_king.pos[1]-1), 
                                 (opp_king.pos[0], opp_king.pos[1]-1), (opp_king.pos[0]+1, opp_king.pos[1]-1), (opp_king.pos[0]+1, opp_king.pos[1]), (opp_king.pos[0]+1, opp_king.pos[1]+1)]
                # separate case, if the piece is a pawn
                elif "pawn" in position[s].image:
                    if position[s].colour == "white":
                        if position[s].pos[1] != 0:
                            attacked.append((position[s].pos[0]-1, position[s].pos[1]-1))
                        if position[s].pos[1] != 7:
                            attacked.append((position[s].pos[0]-1, position[s].pos[1]+1))
                    elif position[s].colour == "black":
                        if position[s].pos[1] != 0:
                            attacked.append((position[s].pos[0]+1, position[s].pos[1]-1))
                        if position[s].pos[1] != 7:
                            attacked.append((position[s].pos[0]+1, position[s].pos[1]+1))

    in_reach = [(self.pos[0], self.pos[1]+1), (self.pos[0]-1, self.pos[1]+1), (self.pos[0]-1, self.pos[1]), (self.pos[0]-1, self.pos[1]-1), 
                (self.pos[0], self.pos[1]-1), (self.pos[0]+1, self.pos[1]-1), (self.pos[0]+1, self.pos[1]), (self.pos[0]+1, self.pos[1]+1)]
    for s in in_reach:
        if not s in attacked:
            # remove all squares under attack
            if not 8 in s and not -1 in s:
                # remove squares outside the bounds of the board
                possible_moves.append(s)
    
    # add the squares for castling if it is possible
    if can_castle(square, "left"):
        possible_moves.append((square[0], square[1]-2))
    if can_castle(square, "right"):
        possible_moves.append((square[0], square[1]+2))

    return possible_moves

def can_castle(square, side):
    # create a list of all the attacked squares
    attacked = []
    for s in position:
        if position[s] != 0 and position[s].colour != position[square].colour:
            if not "king" in position[s].image: # to avoid recursion, this case is dropped, there also does not exist a case in which this would be problematic
                attacked += can_go(s)

    # left side
    if side == "left":
        if position[(square[0], square[1]-1)] == 0 and position[(square[0], square[1]-2)] == 0 and position[(square[0], square[1]-3)] == 0:
            # if the squares left of the king are empty
            if position[square].has_moved == False and position[(square[0], square[1]-4)].has_moved == False:
                # if neither the rook nor the king have moved
                if not square in attacked and not (square[0], square[1]-1) in attacked and not (square[0], square[1]-2) in attacked:
                    # if none of the squares that the king will pass through are attacked by the opponents pieces
                    return True

    # right side
    elif side == "right":
        if position[(square[0], square[1]+1)] == 0 and position[(square[0], square[1]+2)] == 0:
            # if the squares right of the king are empty
            if position[square].has_moved == False and position[(square[0], square[1]+3)].has_moved == False:
                # if neither the rook nor the king have moved
                if not square in attacked and not (square[0], square[1]+1) in attacked and not (square[0], square[1]+2) in attacked:
                    # if none of the squares that the king will pass through are attacked by the opponents pieces
                    return True

    # default return False
    return False

def can_go(square):
    self = position[square] 
    if self == 0:
        raise Exception("Input square empty")
    elif "pawn" in self.image:
        can_go = possible_moves_pawn(square)
    elif "rook" in self.image:
        can_go = possible_moves_rook(square)
    elif "knight" in self.image:
        can_go = possible_moves_knight(square)
    elif "bishop" in self.image:
        can_go = possible_moves_bishop(square)
    elif "queen" in self.image:
        # there's no reason to define a separate function for the movement of the queen since it's just the movement of the bishop and rook combined
        can_go = possible_moves_bishop(square) + possible_moves_rook(square)
    elif "king" in self.image:
        can_go = possible_moves_king(square)
    else:
        raise Exception("Input square did not yeild a recognisable")
    
    for square in can_go:
        if position[square] != 0:
            if position[square].colour != self.colour:
                position[square].can_capture = True

    filtered = list(filter(lambda square: position[square] == 0 or position[square].colour != self.colour, can_go))

            
    return filtered

def move(start_square, finish_square):
    global position
    # save the previous position just in case the move turns out to be invalid
    prev_position = position[finish_square]

    
    if finish_square in can_go(start_square):
        
        # handle en passent during the move
        if "pawn" in position[start_square].image:
            if finish_square[0] != 0 and finish_square[0] != 7 and start_square[1] != finish_square[1]:

                if position[(finish_square[0]+1, finish_square[1])] != 0:
                    if position[start_square].colour == "white" and position[(finish_square[0]+1, finish_square[1])].can_en_passent:
                        del position[(finish_square[0]+1, finish_square[1])]
                        position[(finish_square[0]+1, finish_square[1])] = 0

                if position[(finish_square[0]-1, finish_square[1])] != 0:
                    if position[start_square].colour == "black" and position[(finish_square[0]-1, finish_square[1])].can_en_passent:
                        del position[(finish_square[0]-1, finish_square[1])]
                        position[(finish_square[0]-1, finish_square[1])] = 0

        # if castling is in play, the rook should be moved as well
        if "king" in position[start_square].image:
            if abs(start_square[1] - finish_square[1]) == 2:
                # if the king has moved two steps horizontally, it must be the case that castling is in play
                if start_square[1] > finish_square[1]: # the king has moved left

                    # change the representation on the board (rect_piecce) 
                    rect_piece[position[(start_square[0], start_square[1]-4)]].x, rect_piece[position[(start_square[0], start_square[1]-4)]].y = squares[(start_square[0], start_square[1]-1)].x_cor, squares[(start_square[0], start_square[1]-1)].y_cor
                    
                    # change internal representation
                    position[(start_square[0], start_square[1]-1)] = position[(start_square[0], start_square[1]-4)]
                    position[(start_square[0], start_square[1]-4)] = 0

                elif start_square[1] < finish_square[1]: # the king has moved right

                    # change the representation on the board (rect_piecce) 
                    rect_piece[position[(start_square[0], start_square[1]+3)]].x, rect_piece[position[(start_square[0], start_square[1]+3)]].y = squares[(start_square[0], start_square[1]+1)].x_cor, squares[(start_square[0], start_square[1]+1)].y_cor
                    
                    # change internal representation
                    position[(start_square[0], start_square[1]+1)] = position[(start_square[0], start_square[1]+3)]
                    position[(start_square[0], start_square[1]+3)] = 0

        # move the piece
        position[finish_square] = position[start_square]
        position[start_square] = 0

        # make sure check is not unblocked
        for key in position:
            if position[key] != 0 and position[finish_square] != 0:
                if "king" in position[key].image and position[key].colour == position[finish_square].colour:
                    king = position[key] # identify the king piece of the side that is to move
        for key in position:
            if position[key] != 0 and position[finish_square] != 0:
                if position[key].colour != position[finish_square].colour:
                    # for every piece of the opposite colour
                    if king.pos in can_go(position[key].pos):
                        # if the king is under attack by one of these peices now, when it wasn't before, it means that the check was unblocked, hence the move is invalid
                        rect_piece[position[finish_square]].x, rect_piece[position[finish_square]].y = squares[start_square].x_cor, squares[start_square].y_cor
                        position[start_square] = position[finish_square]
                        position[finish_square] = prev_position
                        print("invalid move")
                        return 
        
        # destroy the class instance (the piece) if it happens to be on the square
        if prev_position != 0:
            if prev_position.can_capture:
                del prev_position
            else:
                raise Exception("tried to capture uncapturable piece")

        if "pawn" in position[finish_square].image:
            if finish_square[0] == 0 or finish_square[0] == 7:
                promotion(finish_square)

        # set the board
        set_board()

        # set piece.has_moved to true (because the piece has moved)
        position[finish_square].has_moved = True

    else:
        # give an error message in terminal - this is intentionally not an exception since we don't necessarily want to close the program upon this occuring
        print("invalid move")

    # clear previous is_check attributes
    white.is_check = False
    black.is_check = False

    # set is_check = True if king is under attack
    attacked = []
    for s in position:
        if position[s] != 0 and position[finish_square] != 0:
            if position[s].colour == position[finish_square].colour:
                # to avoid recursion - the case of "king" is treated separately, also pawns are handled separately because their capture mechamic is different
                if not "king" in position[s].image and not "pawn" in position[s].image:
                    for attacked_square in can_go(s):
                        attacked.append(attacked_square)
                elif "king" in position[s].image:
                    opp_king = position[s]
                    attacked += [(opp_king.pos[0], opp_king.pos[1]+1), (opp_king.pos[0]-1, opp_king.pos[1]+1), (opp_king.pos[0]-1, opp_king.pos[1]), (opp_king.pos[0]-1, opp_king.pos[1]-1), 
                                 (opp_king.pos[0], opp_king.pos[1]-1), (opp_king.pos[0]+1, opp_king.pos[1]-1), (opp_king.pos[0]+1, opp_king.pos[1]), (opp_king.pos[0]+1, opp_king.pos[1]+1)]
                # separate case, if the piece is a pawn
                elif "pawn" in position[s].image:
                    if position[s].colour == "white":
                        if position[s].pos[1] != 0:
                            attacked.append((position[s].pos[0]-1, position[s].pos[1]-1))
                        if position[s].pos[1] != 7:
                            attacked.append((position[s].pos[0]-1, position[s].pos[1]+1))
                    elif position[s].colour == "black":
                        if position[s].pos[1] != 0:
                            attacked.append((position[s].pos[0]+1, position[s].pos[1]-1))
                        if position[s].pos[1] != 7:
                            attacked.append((position[s].pos[0]+1, position[s].pos[1]+1))

    for s in position:
        if position[s] != 0 and position[finish_square] != 0:
            if "king" in position[s].image and position[s].colour != position[finish_square].colour and position[s].pos in attacked:
                if position[s].colour == "white":
                    white.is_check = True
                if position[s].colour == "black":
                    black.is_check = True

                
    # clear all previous en passent rights
    for square in position:
        if position[square] != 0:
            position[square].can_en_passent = False

    # set stage for en passesnt - very important because we are indeed cultured people, sets any pawn that just moved two steps to can_en_passent = True
    if position[finish_square] != 0:
        if "pawn" in position[finish_square].image:
            if position[finish_square].colour == "white":
                if start_square[0] == 6 and finish_square[0] == 4:
                    position[finish_square].can_en_passent = True
            elif position[finish_square].colour == "black":
                if start_square[0] == 1 and finish_square[0] == 3:
                    position[finish_square].can_en_passent = True


################ Fuck yeah! the actual game! You know, the part where you play the... you get it ##################

pygame.init()

pygame.display.set_icon(pygame.image.load(os.path.join('assets', "w_king.png")))

pygame.display.set_caption('chess')

# Dimentions
HEIGHT = 800
WIDTH = 1200

# Colours
WHITE = (255, 255, 255)
BLUE = (0,191,255)
YELLOW = (255,255,0)
BLACK = (0, 0, 0)

# define the window that will be displayed
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Square:
    def __init__(self, colour, x_cor, y_cor):
        self.colour = colour
        self.x_cor = x_cor
        self.y_cor = y_cor

# handle the machanics for promotion - this is handled in the actual game because it requires the selection of a piece
# arguably, this should be handled in the internal game made above, but it was more difficult and didn't work the way I wanted so I couldn't be bothered and did it this way instead
# this works without issues (to the extent that I tested it) and doesn't break the internal game mechanics 
def promotion(square):
    del rect_piece[position[square]]
    del position[square]

    # keep track on if the player has chosen a piece
    chosen = False

    # because promotion is handled differently depending on which side is promoting, this will be handled in two different cases
    if square[0] == 0: # this means the colour is white
        select_screen = pygame.Rect(900, 100, 200, 200)
        pygame.draw.rect(WIN, WHITE, select_screen)
        # display queen
        WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('assets', "w_queen.png")), (100, 100)), (900, 100)) 
        # representation that can be clicked on
        queen = pygame.Rect(900, 100, 100, 100)

        # display rook
        WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('assets', "w_rook.png")), (100, 100)), (1000, 100))
        rook = pygame.Rect(1000, 100, 100, 100)

        # display bishop
        WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('assets', "w_bishop.png")), (100, 100)), (900, 200))
        bishop = pygame.Rect(900, 200, 100, 100)

        # display knight
        WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('assets', "w_knight.png")), (100, 100)), (1000, 200))
        knight = pygame.Rect(1000, 200, 100, 100)

        # display changes on screen
        draw(squares, position)

        while not chosen:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if queen.collidepoint(event.pos):
                        position[square] = Piece("white", "w_queen.png", 5, None, False, False)
                        chosen = True
                    elif rook.collidepoint(event.pos):
                        position[square] = Piece("white", "w_rook.png", 2, None, False, False)
                        chosen = True
                    elif bishop.collidepoint(event.pos):
                        position[square] = Piece("white", "w_bishop.png", 4, None, False, False)
                        chosen = True
                    elif knight.collidepoint(event.pos):
                        position[square] = Piece("white", "w_knight.png", 3, None, False, False)
                        chosen = True
        
        # remove the squares that represent the peices and also the select screen
        del queen
        del rook
        del bishop
        del knight
        del select_screen
        # what we now see on screen are only empty sprites that we can, so we redraw everything i.e. we clear the screen and draw over it
        WIN.fill(BLACK)

    elif square[0] == 7: # this means the colour is white
        select_screen = pygame.Rect(900, 100, 200, 200)
        pygame.draw.rect(WIN, WHITE, select_screen)
        # display queen
        WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('assets', "b_queen.png")), (100, 100)), (900, 100)) 
        # representation that can be clicked on
        queen = pygame.Rect(900, 100, 100, 100)

        # display rook
        WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('assets', "b_rook.png")), (100, 100)), (1000, 100))
        rook = pygame.Rect(1000, 100, 100, 100)

        # display bishop
        WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('assets', "b_bishop.png")), (100, 100)), (900, 200))
        bishop = pygame.Rect(900, 200, 100, 100)

        # display knight
        WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('assets', "b_knight.png")), (100, 100)), (1000, 200))
        knight = pygame.Rect(1000, 200, 100, 100)

        # display changes on screen
        draw(squares, position)

        while not chosen:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if queen.collidepoint(event.pos):
                        position[square] = Piece("white", "b_queen.png", 15, None, False, False)
                        chosen = True
                    elif rook.collidepoint(event.pos):
                        position[square] = Piece("white", "b_rook.png", 12, None, False, False)
                        chosen = True
                    elif bishop.collidepoint(event.pos):
                        position[square] = Piece("white", "b_bishop.png", 14, None, False, False)
                        chosen = True
                    elif knight.collidepoint(event.pos):
                        position[square] = Piece("white", "b_knight.png", 13, None, False, False)
                        chosen = True
        
        # remove the squares that represent the peices and also the select screen
        del queen
        del rook
        del bishop
        del knight
        del select_screen
        # what we now see on screen are only empty sprites that we can, so we redraw everything i.e. we clear the screen and draw over it
        WIN.fill(BLACK)


    # make sure the piece can move properly i.e it has a functional representation in rect_piece dict
    rect_piece[position[square]] = pygame.Rect(squares[square].x_cor, squares[square].y_cor, 100, 100)
    draw(squares, position)


# create a dict with squares corresponding to the piece
squares = {}
for key in position:
    if (key[0] + key[1]) % 2 == 0:
        colour = WHITE
    else:
        colour = BLUE
    x_cor = key[1]*100
    y_cor = key[0]*100
    squares[key] = Square(colour, x_cor, y_cor)

# create a dict to keep track of the squares original colour
org_colour = {}
for key in position:
    if (key[0] + key[1]) % 2 == 0:
        colour = WHITE
    else:
        colour = BLUE
    org_colour[key] = colour

# create rectangles that will represent the pieces on the board for movement porpouses
rect_piece = {}
for key in position:
    if position[key] != 0:
        rect_piece[position[key]] = pygame.Rect(squares[key].x_cor, squares[key].y_cor, 100, 100)

def draw(squares, position):
    # draw all the squares on screen
    for key in squares:
        square = squares[key]
        pygame.draw.rect(WIN, square.colour, pygame.Rect(square.x_cor, square.y_cor, 100, 100))
    # draw all the pieces on the screen
    for key in position:
        if position[key] != 0:
            piece_image = pygame.image.load(os.path.join('assets', position[key].image))
            piece = pygame.transform.scale(piece_image, (100, 100))
            WIN.blit(piece, (rect_piece[position[key]].x, rect_piece[position[key]].y))
    pygame.display.update()


# when a piece is clicked, the squares to which it can move should be highlighted
def highlight(square):
    for s in can_go(square):
        squares[s].colour = YELLOW
    draw(squares, position)

def main():
    # variable for running game
    running = True

    # keeping track of what piece is selected
    selected = None

    game_chosen = False

    # gamemodes
    pvp = False
    play_ai = False
    ai_vs_ai = False
    ai_vs_random = False

    while running:
        if not game_chosen:
            draw(squares, position)
            pvp_rect = pygame.Rect(850, 200, 300, 100)
            pygame.draw.rect(WIN, WHITE, pvp_rect)
            play_ai_rect = pygame.Rect(850, 350, 300, 100)
            pygame.draw.rect(WIN, WHITE, play_ai_rect)
            ai_vs_ai_rect = pygame.Rect(850, 500, 300, 100)
            pygame.draw.rect(WIN, WHITE, ai_vs_ai_rect)
            ai_vs_random_rect = pygame.Rect(850, 650, 300, 100)
            pygame.draw.rect(WIN, WHITE, ai_vs_random_rect)
            font = pygame.font.Font('freesansbold.ttf', 42)
            text1 = font.render('Play Manual', True, BLACK, WHITE)
            WIN.blit(text1, (pvp_rect.x+25, pvp_rect.y+25))
            text2 = font.render('Play AI', True, BLACK, WHITE)
            WIN.blit(text2, (play_ai_rect.x+70, play_ai_rect.y+25))
            text3 = font.render('AI vs AI', True, BLACK, WHITE)
            WIN.blit(text3, (ai_vs_ai_rect.x+70, ai_vs_ai_rect.y+25))
            text4 = font.render('AI vs Random', True, BLACK, WHITE)
            WIN.blit(text4, (ai_vs_random_rect.x+5, ai_vs_random_rect.y+25))
            font_title = pygame.font.Font('freesansbold.ttf', 35)
            text5 = font_title.render('Choose gamemode', True, WHITE, BLACK)
            WIN.blit(text5, (840, 100))
            pygame.display.update()
            while not game_chosen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pvp_rect.collidepoint(event.pos):
                            pvp = True
                            game_chosen = True
                        elif play_ai_rect.collidepoint(event.pos):
                            play_ai = True
                            game_chosen = True
                        elif ai_vs_ai_rect.collidepoint(event.pos):
                            ai_vs_ai = True
                            game_chosen = True
                        elif ai_vs_random_rect.collidepoint(event.pos):
                            ai_vs_random = True
                            game_chosen = True
            del pvp_rect
            del play_ai_rect
            del ai_vs_ai_rect
            del ai_vs_random_rect
            del text1
            del text2
            del text3
            del text4
            del text5
            WIN.fill(BLACK)
            draw(squares, position)


        if pvp:
            turn = 1
            while not white.is_checkmate and not black.is_checkmate:
                for event in pygame.event.get():  
                    if event.type == pygame.QUIT:  
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # clear the board of the squares that a piece can move to 
                        for s in squares:
                            squares[s].colour = org_colour[s]

                        # keep track on if a piece has moved this turn
                        moved = False

                        for square in position:
                            if squares[square].x_cor < event.pos[0] and squares[square].x_cor + 100 > event.pos[0] and squares[square].y_cor < event.pos[1] and squares[square].y_cor + 100 > event.pos[1]:
                                if not selected is None and square in can_go(selected):
                                    if (position[selected].colour == "white" and turn % 2 == 1) or (position[selected].colour == "black" and turn % 2 == 0):
                                        # above basically means that for every square, if player pressed the square and the piece can go to the square and it's that sides turn then...
                                        rect_piece[position[selected]].x, rect_piece[position[selected]].y = squares[square].x_cor, squares[square].y_cor
                                        move(selected, square)
                                        draw(squares, position)
                                        print(board)


                                        if position[selected] == 0:

                                            # change moved to True because a piece has moved on this click
                                            moved = True

                                            # change the turn 
                                            turn += 1

                                        # reset selected piece
                                        selected = None

                                        break

                        if not moved: # of course, if we move a piece, we don't want to show the squares it can move to
                            # show all squares that the piece can go to
                            for square in position:
                                if position[square] != 0:
                                    if rect_piece[position[square]].collidepoint(event.pos):
                                        if (position[square].colour == "white" and turn % 2 == 1) or (position[square].colour == "black" and turn % 2 == 0):
                                            highlight(square)
                                            selected = square

                draw(squares, position)


# run program
main()