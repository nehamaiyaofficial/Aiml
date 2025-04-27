import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 550
LINE_WIDTH = 4
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 5

# Colors
BG_COLOR = (245, 245, 245)
LINE_COLOR = (200, 200, 200)
CIRCLE_COLOR = (100, 149, 237)
CROSS_COLOR = (255, 105, 180)
BUTTON_COLOR = (173, 216, 230)
BUTTON_TEXT_COLOR = (40, 40, 40)
WIN_LINE_COLOR = (255, 165, 0)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe - Cute Edition')
screen.fill(BG_COLOR)

# Fonts
font = pygame.font.SysFont('comicsans', 30)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw lines
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WIDTH), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    return all(all(cell is not None for cell in row) for row in board)

def check_winner(player):
    # Horizontal, Vertical and Diagonal Check
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return (row, 'row')
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return (col, 'col')
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return (0, 'diag')
    if all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        return (0, 'antidiag')
    return None

def computer_move():
    available = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if available_square(r, c)]
    if available:
        move = random.choice(available)
        mark_square(move[0], move[1], 'O')

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, w, h), border_radius=15)
    label = font.render(text, True, BUTTON_TEXT_COLOR)
    label_rect = label.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(label, label_rect)

def draw_mode_selection():
    screen.fill(BG_COLOR)
    draw_button("Player vs Computer", 100, 150, 200, 50)
    draw_button("2 Players", 100, 250, 200, 50)
    pygame.display.update()

def draw_win_line(info):
    if info:
        idx, direction = info
        if direction == 'row':
            y = idx * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, WIN_LINE_COLOR, (20, y), (WIDTH - 20, y), 8)
        elif direction == 'col':
            x = idx * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, WIN_LINE_COLOR, (x, 20), (x, WIDTH - 20), 8)
        elif direction == 'diag':
            pygame.draw.line(screen, WIN_LINE_COLOR, (20, 20), (WIDTH - 20, WIDTH - 20), 8)
        elif direction == 'antidiag':
            pygame.draw.line(screen, WIN_LINE_COLOR, (WIDTH - 20, 20), (20, WIDTH - 20), 8)

running = True
player = 'X'
game_over = False
mode_selected = False
mode = None
winner_info = None

# Mode selection
while not mode_selected:
    draw_mode_selection()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 100 <= mx <= 300 and 150 <= my <= 200:
                mode = '1'
                mode_selected = True
            elif 100 <= mx <= 300 and 250 <= my <= 300:
                mode = '2'
                mode_selected = True

# Start game
screen.fill(BG_COLOR)
draw_lines()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if clicked_row < BOARD_ROWS and clicked_col < BOARD_COLS:
                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        draw_figures()
                        winner_info = check_winner(player)

                        if winner_info:
                            draw_win_line(winner_info)
                            game_over = True
                        elif is_board_full():
                            game_over = True
                        else:
                            if mode == '1' and player == 'X':
                                player = 'O'
                                computer_move()
                                draw_figures()
                                winner_info = check_winner('O')
                                if winner_info:
                                    draw_win_line(winner_info)
                                    game_over = True
                                player = 'X'
                            else:
                                player = 'O' if player == 'X' else 'X'

    pygame.display.update()

pygame.quit()
sys.exit()

