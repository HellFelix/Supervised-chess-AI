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
    return possible_moves

# handle the machanics for promotion
def promotion(square):
    del position[square]
    has_chosen = False
    while not has_chosen:
        print("\n", "enter 1 for queen", "\n", "enter 2 for rook", "\n", "enter 3 for bishop", "\n", "enter 4 for knight")
        choice = input()
        if square[0] == 7: # This means it's a black pawn
            if choice == "1":
                position[square] = Piece("black", "b_queen.png", 15, None, False, False)
                has_chosen = True
            elif choice == "2":
                position[square] = Piece("black", "b_rook.png", 12, None, False, False)
                has_chosen = True
            elif choice == "3":
                position[square] = Piece("black", "b_rook.png", 12, None, False, False)
                has_chosen = True
            elif choice == "4":
                position[square] = Piece("black", "b_knight.png", 13, None, False, False)
                has_chosen = True
            else:
                print("Invalid input, choose again")
        elif square[0] == 0: # this means the pawn is white
            if choice == "1":
                position[square] = Piece("white", "w_queen.png", 5, None, False, False)
                has_chosen = True
            elif choice == "2":
                position[square] = Piece("white", "w_rook.png", 2, None, False, False)
                has_chosen = True
            elif choice == "3":
                position[square] = Piece("white", "w_rook.png", 2, None, False, False)
                has_chosen = True
            elif choice == "4":
                position[square] = Piece("white", "w_knight.png", 3, None, False, False)
                has_chosen = True
            else:
                print("Invalid input, choose again")
        else:
            raise Exception("invalid promotion square")


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

    filtered = filter(lambda square: position[square] == 0 or position[square].colour != self.colour, can_go)

            
    return filtered

def move(start_square, finish_square):
    global position
    if finish_square in can_go(start_square):
        # destroy the class instance (the piece) if it happens to be on the square
        if position[finish_square] != 0:
            if position[finish_square].can_capture:
                del position[finish_square]
            else:
                raise Exception("tried to capture uncapturable piece")
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

        # save the previous position just in case the move turns out to be invalid
        prev_position = position

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
                        position = prev_position
                        print("invalid move")
                        return 



        # handle promotion
        if position[key] != 0:
            if "pawn" in position[finish_square].image:
                if position[finish_square].colour == "white" and finish_square[0] == 0:
                    promotion(finish_square)
                elif position[finish_square].colour =="black" and finish_square[0] == 7:
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

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

class Square:
    def __init__(self, colour, x_cor, y_cor):
        self.colour = colour
        self.x_cor = x_cor
        self.y_cor = y_cor


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

    while running:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for square in position:
                    if squares[square].x_cor < event.pos[0] and squares[square].x_cor + 100 > event.pos[0] and squares[square].y_cor < event.pos[1] and squares[square].y_cor + 100 > event.pos[1]:
                        if not selected is None and square in can_go(selected):
                            # above basically means that for every square, if player pressed the square and the pice can go to the square then...
                            rect_piece[position[selected]].x, rect_piece[position[selected]].y = squares[square].x_cor, squares[square].y_cor
                            draw(squares, position)
                            move(selected, square)
                            print(board)

                            break

                # return all squares to their original colour
                for s in squares:
                    squares[s].colour = org_colour[s]
                # reset selected piece
                selected = None
                # show all squares that the piece can go to
                for square in position:
                    if position[square] != 0:
                        if rect_piece[position[square]].collidepoint(event.pos):
                            highlight(square)
                            selected = square

        draw(squares, position)

# run program
main()