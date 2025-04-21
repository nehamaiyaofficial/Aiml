import random
import os
import time

# Define blocks and initial settings
blocks = ['🟥', '🟦', '🟩', '🟨', '🟪']  # Cute emoji blocks
score = 0
lives = 3

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

print("🎮 Welcome to Block Blast!")
print("Press the correct key to blast the block!")
input("Press Enter to start...")

try:
    while lives > 0:
        clear_screen()
        current_block = random.choice(blocks)
        print(f"\n💣 Blast this block: {current_block}")
        print(f"Type the symbol exactly: {current_block}")
        print(f"Score: {score} | Lives: {lives}\n")

        user_input = input("👉 Your input: ")

        if user_input == current_block:
            print("🎉 Boom! You blasted it!")
            score += 1
        else:
            print("💔 Oops! Missed it!")
            lives -= 1
        
        time.sleep(1.5)

    clear_screen()
    print("\n😵 Game Over!")
    print(f"Your final score: {score}")
except KeyboardInterrupt:
    print("\n👋 Game exited.")

