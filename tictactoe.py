import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
ROWS, COLS = 3, 3
SQSIZE = WIDTH // COLS
LINE_WIDTH = 5
CIRCLE_RADIUS = SQSIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 10
SPACE = SQSIZE // 4

# Colors
BG_COLOR = (250, 248, 239)
LINE_COLOR = (187, 173, 160)
CIRCLE_COLOR = (84, 191, 255)
CROSS_COLOR = (255, 105, 180)
BUTTON_COLOR = (147, 112, 219)
TEXT_COLOR = (255, 255, 255)
WIN_LINE_COLOR = (255, 99, 71)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Aesthetic Tic Tac Toe')

# Fonts
font = pygame.font.SysFont('Comic Sans MS', 40)
small_font = pygame.font.SysFont('Comic Sans MS', 30)

# Board
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Draw grid
def draw_grid():
    screen.fill(BG_COLOR)
    for x in range(1, COLS):
        pygame.draw.line(screen, LINE_COLOR, (x * SQSIZE, 0), (x * SQSIZE, WIDTH), LINE_WIDTH)
    for y in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, y * SQSIZE), (WIDTH, y * SQSIZE), LINE_WIDTH)

# Draw X and O
def draw_marks():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'X':
                start_desc = (col * SQSIZE + SPACE, row * SQSIZE + SPACE)
                end_desc = (col * SQSIZE + SQSIZE - SPACE, row * SQSIZE + SQSIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                start_asc = (col * SQSIZE + SPACE, row * SQSIZE + SQSIZE - SPACE)
                end_asc = (col * SQSIZE + SQSIZE - SPACE, row * SQSIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
            elif board[row][col] == 'O':
                center = (col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2)
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)

# Helpers
def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    return all(all(cell is not None for cell in row) for row in board)

def check_win(player):
    for row in range(ROWS):
        if all(board[row][col] == player for col in range(COLS)):
            return ('row', row)
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            return ('col', col)
    if all(board[i][i] == player for i in range(ROWS)):
        return ('diag', 0)
    if all(board[i][COLS - i - 1] == player for i in range(ROWS)):
        return ('antidiag', 0)
    return None

def draw_win_line(info):
    if info:
        direction, idx = info
        if direction == 'row':
            y = idx * SQSIZE + SQSIZE // 2
            pygame.draw.line(screen, WIN_LINE_COLOR, (20, y), (WIDTH - 20, y), 10)
        elif direction == 'col':
            x = idx * SQSIZE + SQSIZE // 2
            pygame.draw.line(screen, WIN_LINE_COLOR, (x, 20), (x, WIDTH - 20), 10)
        elif direction == 'diag':
            pygame.draw.line(screen, WIN_LINE_COLOR, (20, 20), (WIDTH - 20, WIDTH - 20), 10)
        elif direction == 'antidiag':
            pygame.draw.line(screen, WIN_LINE_COLOR, (WIDTH - 20, 20), (20, WIDTH - 20), 10)

def computer_move():
    options = [(r, c) for r in range(ROWS) for c in range(COLS) if available_square(r, c)]
    if options:
        r, c = random.choice(options)
        mark_square(r, c, 'O')

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, w, h), border_radius=12)
    label = small_font.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=(x + w//2, y + h//2))
    screen.blit(label, label_rect)

def draw_menu():
    screen.fill(BG_COLOR)
    draw_button("Play vs Computer", 100, 150, 300, 60)
    draw_button("2 Player Mode", 100, 250, 300, 60)
    pygame.display.update()

# Game Variables
running = True
player = 'X'
game_over = False
mode_selected = False
mode = None
winner_info = None

# Mode Selection
while not mode_selected:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 100 <= mx <= 400 and 150 <= my <= 210:
                mode = '1'
                mode_selected = True
            if 100 <= mx <= 400 and 250 <= my <= 310:
                mode = '2'
                mode_selected = True

# Main Game Loop
while running:
    draw_grid()
    draw_marks()

    if game_over or is_board_full():
        draw_button("Replay", 50, 520, 150, 50)
        draw_button("Quit", 300, 520, 150, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if game_over or is_board_full():
                if 50 <= mx <= 200 and 520 <= my <= 570:
                    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
                    player = 'X'
                    game_over = False
                    winner_info = None
                if 300 <= mx <= 450 and 520 <= my <= 570:
                    pygame.quit()
                    sys.exit()
            else:
                if my < WIDTH:
                    clicked_row = my // SQSIZE
                    clicked_col = mx // SQSIZE
                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        winner_info = check_win(player)
                        if winner_info:
                            game_over = True
                        elif is_board_full():
                            game_over = True
                        else:
                            if mode == '1' and player == 'X':
                                player = 'O'
                                computer_move()
                                winner_info = check_win('O')
                                if winner_info:
                                    game_over = True
                                player = 'X'
                            else:
                                player = 'O' if player == 'X' else 'X'

    if winner_info:
        draw_win_line(winner_info)

    pygame.display.update()

pygame.quit()
sys.exit()

