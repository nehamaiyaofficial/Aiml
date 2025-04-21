import random

# Define a 10x10 grid
GRID_SIZE = 10
grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Sample block shapes using 2D lists
blocks = {
    'O': [['O', 'O'],
          ['O', 'O']],
    
    'I': [['I', 'I', 'I', 'I']],
    
    'L': [['L', '.'],
          ['L', '.'],
          ['L', 'L']],
    
    'Z': [['Z', 'Z', '.'],
          ['.', 'Z', 'Z']],
}

def print_grid():
    print("\n   " + " ".join([str(i) for i in range(GRID_SIZE)]))
    for idx, row in enumerate(grid):
        print(f"{idx:2} " + " ".join(row))
    print()

def print_block(block):
    for row in block:
        print("  " + " ".join(row))
    print()

def can_place_block(block, x, y):
    for i in range(len(block)):
        for j in range(len(block[0])):
            if block[i][j] != '.':
                if (x+i >= GRID_SIZE or y+j >= GRID_SIZE or grid[x+i][y+j] != '.'):
                    return False
    return True

def place_block(block, x, y, char):
    for i in range(len(block)):
        for j in range(len(block[0])):
            if block[i][j] != '.':
                grid[x+i][y+j] = char

def game_loop():
    score = 0
    while True:
        print_grid()
        block_key = random.choice(list(blocks.keys()))
        block = blocks[block_key]
        print(f"🧱 Your block: {block_key}")
        print_block(block)

        try:
            x = int(input("Enter row to place block: "))
            y = int(input("Enter column to place block: "))
        except ValueError:
            print("⛔ Invalid input! Use numbers only.\n")
            continue

        if can_place_block(block, x, y):
            place_block(block, x, y, block_key)
            score += 10
            print(f"✅ Placed block! Score: {score}")
        else:
            print("❌ Can't place block there. Game Over.")
            break

if __name__ == "__main__":
    print("🎮 Welcome to ASCII Block Puzzle!")
    input("Press Enter to start...")
    game_loop()

