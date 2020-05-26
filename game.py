import numpy as np
import pygame
import sys

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (255, 255, 120)
DARK_RED = (255, 59, 59)

ROW_COUNT = 6
COL_COUNT = 7
CONNECT = 4


def create_board():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[0][col] == 0


def get_next_open_row(board, col):
    for r in reversed(range(ROW_COUNT)):
        if board[r][col] == 0:
            return r
    return -1


def print_board(board):
    for row in range(ROW_COUNT):
        for col in range(COL_COUNT):
            print(int(board[row][col]), end=" ")
        print()


def check_win(board, piece):
    v = 0
    for r in range(ROW_COUNT):
        v = 0
        for c in range(COL_COUNT):
            if board[r][c] == piece:
                v += 1
            else:
                v = 0
            if v == CONNECT:
                return True
    for c in range(COL_COUNT):
        v = 0
        for r in range(ROW_COUNT):
            if board[r][c] == piece:
                v += 1
            else:
                v = 0
            if v == CONNECT:
                return True
    for r in range(CONNECT - 1, ROW_COUNT):
        for c in range(COL_COUNT - CONNECT + 1):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    for r in range(ROW_COUNT - CONNECT + 1):
        for c in range(COL_COUNT - CONNECT + 1):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    return False


def draw_board(board):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE * 1.5)), radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE * 1.5)), radius)
                pygame.draw.circle(screen, DARK_RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE * 1.5)), small_radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE * 1.5)), radius)
                pygame.draw.circle(screen, DARK_YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE * 1.5)), small_radius)


def animation(col, piece, dest):
    rows = 0
    while rows < dest:
        draw_board(previous_board)
        if piece == 1:
            pygame.draw.circle(screen, YELLOW, (int(col * SQUARESIZE + SQUARESIZE / 2), int(rows * SQUARESIZE + SQUARESIZE * 1.5)), radius)
            pygame.draw.circle(screen, DARK_YELLOW, (int(col * SQUARESIZE + SQUARESIZE / 2), int(rows * SQUARESIZE + SQUARESIZE * 1.5)), small_radius)
        elif piece == 0:
            pygame.draw.circle(screen, RED, (int(col * SQUARESIZE + SQUARESIZE / 2), int(rows * SQUARESIZE + SQUARESIZE * 1.5)), radius)
            pygame.draw.circle(screen, DARK_RED, (int(col * SQUARESIZE + SQUARESIZE / 2), int(rows * SQUARESIZE + SQUARESIZE * 1.5)), small_radius)
        pygame.display.update()
        pygame.time.wait(35)
        rows += 1


board = create_board()
game_over = False
turn = 0

pygame.init()
pygame.display.set_caption('Connect 4 by Benson Shen')


SQUARESIZE = 80

width = COL_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE + SQUARESIZE

size = (width, height)

radius = int(SQUARESIZE / 2 - 5)
small_radius = int(SQUARESIZE / 2 - 15)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("tkinter", 75)

while not game_over:
    move_made = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), radius)
                pygame.draw.circle(screen, DARK_RED, (posx, int(SQUARESIZE / 2)), small_radius)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), radius)
                pygame.draw.circle(screen, DARK_YELLOW, (posx, int(SQUARESIZE / 2)), small_radius)

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)
            previous_board = board.copy()
            if turn == 0:
                posx = event.pos[0]
                selection = int(posx/SQUARESIZE)
                if is_valid_location(board, selection):
                    move_made = True
                    row = get_next_open_row(board, selection)
                    drop_piece(board, row, selection, 1)
            else:
                posx = event.pos[0]
                selection = int(posx / SQUARESIZE)
                if is_valid_location(board, selection):
                    move_made = True
                    row = get_next_open_row(board, selection)
                    drop_piece(board, row, selection, 2)

            pygame.time.wait(35)
            if turn == 0 and move_made:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), radius)
            elif turn == 1 and move_made:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), radius)

            if check_win(board, 1):
                label = myfont.render("Player 1 wins!", 1, DARK_RED)
                pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE / 2)), radius)
                screen.blit(label, (40, int(SQUARESIZE/4)))
                game_over = True
            elif check_win(board, 2):
                label = myfont.render("Player 2 wins!", 1, DARK_YELLOW)
                pygame.draw.circle(screen, BLACK, (posx, int(SQUARESIZE / 2)), radius)
                screen.blit(label, (40, int(SQUARESIZE / 4)))
                game_over = True

            #print_board(board)
            animation(selection, turn, get_next_open_row(board, selection) + 1)
            draw_board(board)
            pygame.display.update()

            if move_made:
                turn += 1
                turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
