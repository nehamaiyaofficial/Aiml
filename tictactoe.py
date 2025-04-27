import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 6
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw lines
def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

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
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_winner(player):
    # Check rows and columns
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return True
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(BOARD_ROWS)]):
        return True
    if all([board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True
    return False

def computer_move():
    available = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if available_square(r, c)]
    if available:
        move = random.choice(available)
        mark_square(move[0], move[1], 'O')

# Setup selection screen
mode_selected = False
mode = None
font = pygame.font.SysFont(None, 40)

def draw_mode_selection():
    screen.fill(BG_COLOR)
    text1 = font.render("Press 1: vs Computer", True, (255, 255, 255))
    text2 = font.render("Press 2: 2 Players", True, (255, 255, 255))
    screen.blit(text1, (30, 100))
    screen.blit(text2, (50, 160))
    pygame.display.update()

running = True
player = 'X'
game_over = False

# Mode Selection Loop
draw_mode_selection()
while not mode_selected:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = '1'
                mode_selected = True
            elif event.key == pygame.K_2:
                mode = '2'
                mode_selected = True

# Start game
draw_lines()

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    draw_figures()

                    if check_winner(player):
                        print(f"Player {player} wins!")
                        game_over = True
                    elif is_board_full():
                        print("It's a tie!")
                        game_over = True
                    else:
                        if mode == '1':
                            player = 'O'
                            computer_move()
                            draw_figures()
                            if check_winner('O'):
                                print("Computer wins!")
                                game_over = True
                            player = 'X'
                        else:
                            player = 'O' if player == 'X' else 'X'

    pygame.display.update()

pygame.quit()
sys.exit()

