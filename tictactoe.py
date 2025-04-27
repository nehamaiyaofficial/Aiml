import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 500
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
BUTTON_COLOR = (50, 200, 200)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cute Tic Tac Toe')
screen.fill(BG_COLOR)

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
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_winner(player):
    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return True
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
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

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, w, h), border_radius=12)
    font = pygame.font.SysFont(None, 30)
    label = font.render(text, True, BUTTON_TEXT_COLOR)
    label_rect = label.get_rect(center=(x + w/2, y + h/2))
    screen.blit(label, label_rect)

def draw_mode_selection():
    screen.fill(BG_COLOR)
    draw_button("Player vs Computer", 100, 120, 200, 50)
    draw_button("2 Players", 100, 200, 200, 50)
    pygame.display.update()

running = True
player = 'X'
game_over = False
mode_selected = False
mode = None

# Mode selection
while not mode_selected:
    draw_mode_selection()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if 100 <= mx <= 300 and 120 <= my <= 170:
                mode = '1'
                mode_selected = True
            elif 100 <= mx <= 300 and 200 <= my <= 250:
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
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if clicked_row < 3 and clicked_col < 3:
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

