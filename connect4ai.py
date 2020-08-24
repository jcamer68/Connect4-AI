import numpy as np
import pygame
import sys
import math
import random

# uses a minimax algorithm that keeps evaluating all possible board states and then choose the one that guarantees the highest score
# looks at the min and max values for each respective scoring decision

# static variable, does not change
ROW = 6
COLUMN = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

BLUE = (150,0,150)
BLACK = (0,0,0)

# colours for pieces
RED = (255,0,0)
YELLOW = (255,255,0)

WINDOW_LENGTH = 4


#initialize the board using a numpy matrix
def create_board():
    # (columns, rows)
    board = np.zeros((ROW,COLUMN))
    return board

#drops the piece for each player
def drop_piece(board,row,col,piece):
    board[row][col] = piece

def is_valid_location(board, col):
    #checks to see if column has been filled in all the way
    return board[ROW-1][col] == 0

#determines which row the piece will fall into based on the column
def get_next_open_row(board,col):
    # loop checks to see which row is open
    for r in range(ROW):
        if board[r][col] == 0:
            return r

#changes orientation to re-organize positions within the matrix
def print_board(board):
    print(np.flip(board,0))

#checks if a player has won
def winning_move(board, piece):
    # check horizontal locations
    # index count goes from left to right so to get a connect 4 you can only start from index of 3
    for c in range(COLUMN-3):
        for r in range(ROW):
            #checks to see if there are four pieces in a row
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check horizontal locations
    for c in range(COLUMN):
        for r in range(ROW-3):
            #checks to see if there are four pieces in a row
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # positively sloped diagonal1
    for c in range(COLUMN-3):
        for r in range(ROW-3):
            #checks to see if there are four pieces in a row
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # negatively sloped diagonal
    for c in range(COLUMN-3):
        for r in range(3, ROW):
            #checks to see if there are four pieces in a row
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    # incentivizes AI to win the game (i.e. 4 pieces)
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

#adds certain value to each move
def score_position(board, piece):
    score = 0
    # Add preference for center pieces
    #gets the middle column
    center_array = [int(i) for i in list(board[:, COLUMN//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal
    for r in range(ROW):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical
    for c in range(COLUMN):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positively sloped diagonal
    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negatively sloped diagonal
    for r in range(ROW - 3):
        for c in range(COLUMN - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

#is when a player is about to win or play the last position
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000)
            else: #Game is over, no more valid moves
                return (None, 0)
        else: #depth is zero
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN):
        if is_valid_location(board,col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board,col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def draw_board(board):
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)


    pygame.display.update()

board = create_board()
print(board)
game_over = False
# determines which player goes

pygame.init()

myfont = pygame.font.SysFont('monospace', 125)

# randomly determines if player or AI goes first
turn = random.randint(PLAYER, AI)

#need to set the final build of the project
SQUARESIZE = 100
width = COLUMN * SQUARESIZE
height = (ROW+1) * SQUARESIZE
size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while not game_over:

    # If the game is over, close the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        # updates the screen
        pygame.display.update()


        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
            #        print(event.pos)
            #Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                # checks to see if column is full or not
                if is_valid_location(board,col):
                    #if column is not full, checks to see which row is the lowest open
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("player 1 wins!", 1, RED)
                        screen.blit(label, (60,10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)
            #
            #
    #         # Ask for Player 2 Input
    if turn == AI and not game_over:

        # selects random
        # for easy col = random.randint(0, COLUMN-1)
        #col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if is_valid_location(board,col):
            #pygame.time.wait(500)
            #if column is not full, checks to see which row is the lowest open
            row = get_next_open_row(board,col)
            drop_piece(board,row,col,AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("player 2 wins!", 1, YELLOW)
                screen.blit(label, (60,10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    # waits 3 seconds (3000 milliseconds) before closing the window after the game is over
    if game_over:
        pygame.time.wait(3000)