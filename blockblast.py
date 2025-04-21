import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
MARGIN = 5
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
BG_COLOR = (20, 20, 40)
BLOCK_COLORS = [
    (255, 100, 100), (100, 255, 100), (100, 100, 255),
    (255, 255, 100), (255, 100, 255), (100, 255, 255)
]

# Shapes
SHAPES = [
    [[1, 1],
     [1, 1]],

    [[1, 1, 1, 1]],

    [[1, 0],
     [1, 0],
     [1, 1]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 1, 1],
     [0, 1, 0]]
]

# --- Game Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Puzzle")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
score = 0

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = GRAY if grid[row][col] == 0 else grid[row][col]
            pygame.draw.rect(screen, color, 
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN), border_radius=4)

def draw_shape(shape, top_left, color):
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                x = top_left[0] + j * CELL_SIZE
                y = top_left[1] + i * CELL_SIZE
                pygame.draw.rect(screen, color, 
                                 (x, y, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN), border_radius=4)

def generate_block():
    shape = random.choice(SHAPES)
    color = random.choice(BLOCK_COLORS)
    return {'shape': shape, 'color': color}

blocks = [generate_block() for _ in range(3)]

def can_place(shape, top, left):
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                r = top + i
                c = left + j
                if r >= GRID_SIZE or c >= GRID_SIZE or grid[r][c] != 0:
                    return False
    return True

def place_block(shape, top, left, color):
    global score
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                grid[top + i][left + j] = color
    score += 10
    clear_lines()

def clear_lines():
    global grid, score
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_rows = GRID_SIZE - len(new_grid)
    if cleared_rows:
        score += cleared_rows * 50
        for _ in range(cleared_rows):
            new_grid.insert(0, [0] * GRID_SIZE)
        grid = new_grid

def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, HEIGHT - 80))

def draw_blocks():
    start_y = HEIGHT - 150
    for idx, block in enumerate(blocks):
        x = 20 + idx * 180
        draw_shape(block['shape'], (x, start_y), block['color'])

# --- Main Loop ---
selected = None

running = True
while running:
    screen.fill(BG_COLOR)
    draw_grid()
    draw_blocks()
    draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Block selection
            if my > HEIGHT - 150:
                for idx, block in enumerate(blocks):
                    bx = 20 + idx * 180
                    by = HEIGHT - 150
                    bw = len(block['shape'][0]) * CELL_SIZE
                    bh = len(block['shape']) * CELL_SIZE
                    if bx <= mx <= bx + bw and by <= my <= by + bh:
                        selected = idx

            # Grid placement
            elif selected is not None:
                row = my // CELL_SIZE
                col = mx // CELL_SIZE
                block = blocks[selected]
                if can_place(block['shape'], row, col):
                    place_block(block['shape'], row, col, block['color'])
                    blocks[selected] = generate_block()
                    selected = None

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

