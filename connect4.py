import numpy as np
import pygame
import sys
import math

# uses a minimax algorithm that keeps evaluating all possible board states and then choose the one that guarantees the highest score
# looks at the min and max values for each respective scoring decision

# static variable, does not change
ROW = 6
COLUMN = 7

BLUE = (150,0,150)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)


#initialize the board using a numpy matrix
def create_board():
    # (columns, rows)
    board = np.zeros((6,7))
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

def winning_move(board, piece):
    # check horizontal locations
    # index count goes from left to right so to get a connect 4 you can only start from index of 3
    for c in range(COLUMN-3):
        for r in range(ROW):
            #checks to see if there are four pieces in a row
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # check vertical locations
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

    # Check vertical locations for win

def draw_board(board):
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)


    pygame.display.update()

board = create_board()
print(board)
game_over = False
# determines which player goes
turn = 0

pygame.init()

myfont = pygame.font.SysFont('monospace', 125)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()


        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
    #        print(event.pos)
    #Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                # checks to see if column is full or not
                if is_valid_location(board,col):
                    #if column is not full, checks to see which row is the lowest open
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,1)

                    if winning_move(board, 1):
                        label = myfont.render("player 1 wins!", 1, RED)
                        screen.blit(label, (60,10))
                        game_over = True
    #
    #
    #         # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board,col):
                    #if column is not full, checks to see which row is the lowest open
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,2)

                    if winning_move(board, 2):
                        label = myfont.render("player 2 wins!", 1, YELLOW)
                        screen.blit(label, (60,10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)


