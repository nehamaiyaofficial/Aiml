import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# --- Constants ---
GRID_SIZE = 10
CELL_SIZE = 60
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE + 100
MARGIN = 4
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BG_COLOR = (30, 30, 60)
HIGHLIGHT = (100, 100, 100)
BLAST_COLOR = (255, 255, 0)
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

# --- Functions ---
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = GRAY if grid[row][col] == 0 else grid[row][col]
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN)
            pygame.draw.rect(screen, color, rect, border_radius=4)
            pygame.draw.rect(screen, HIGHLIGHT, rect, 1)

def draw_shape(shape, top_left, color):
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                x = top_left[0] + j * CELL_SIZE
                y = top_left[1] + i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE - MARGIN, CELL_SIZE - MARGIN)
                pygame.draw.rect(screen, color, rect, border_radius=4)

def generate_block():
    shape = random.choice(SHAPES)
    color = random.choice(BLOCK_COLORS)
    return {'shape': shape, 'color': color, 'pos': None, 'placed': False}

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
    full_rows = [r for r in range(GRID_SIZE) if all(grid[r])]
    full_cols = [c for c in range(GRID_SIZE) if all(grid[r][c] for r in range(GRID_SIZE))]

    for r in full_rows:
        for c in range(GRID_SIZE):
            grid[r][c] = BLAST_COLOR

    for c in full_cols:
        for r in range(GRID_SIZE):
            grid[r][c] = BLAST_COLOR

    pygame.display.update()
    pygame.time.delay(150)

    for r in full_rows:
        grid[r] = [0] * GRID_SIZE
    for c in full_cols:
        for r in range(GRID_SIZE):
            grid[r][c] = 0

    score += (len(full_rows) + len(full_cols)) * 50

def draw_score():
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, HEIGHT - 80))

def draw_blocks():
    for block in blocks:
        if not block['placed']:
            draw_shape(block['shape'], block['pos'], block['color'])

def all_blocks_placed():
    return all(block['placed'] for block in blocks)

# --- Setup initial blocks ---
blocks = [generate_block() for _ in range(3)]
for i, block in enumerate(blocks):
    block['pos'] = (20 + i * 180, HEIGHT - 80)

# --- Drag variables ---
dragging = None
offset_x = offset_y = 0

# --- Main Loop ---
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
            mx, my = event.pos
            for i, block in enumerate(blocks):
                if block['placed']:
                    continue
                x, y = block['pos']
                w = len(block['shape'][0]) * CELL_SIZE
                h = len(block['shape']) * CELL_SIZE
                if x <= mx <= x + w and y <= my <= y + h:
                    dragging = i
                    offset_x = mx - x
                    offset_y = my - y

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging is not None:
                mx, my = event.pos
                row = my // CELL_SIZE
                col = mx // CELL_SIZE
                block = blocks[dragging]
                if can_place(block['shape'], row, col):
                    place_block(block['shape'], row, col, block['color'])
                    block['placed'] = True
                else:
                    block['pos'] = (20 + dragging * 180, HEIGHT - 80)
                dragging = None

                if all_blocks_placed():
                    blocks = [generate_block() for _ in range(3)]
                    for i, block in enumerate(blocks):
                        block['pos'] = (20 + i * 180, HEIGHT - 80)

        elif event.type == pygame.MOUSEMOTION:
            if dragging is not None:
                mx, my = event.pos
                blocks[dragging]['pos'] = (mx - offset_x, my - offset_y)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

