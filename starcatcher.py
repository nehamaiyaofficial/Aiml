import tkinter as tk
import random
import pygame
import os

# --- Init Pygame Mixer for Sound ---
pygame.mixer.init()
catch_sound = pygame.mixer.Sound("catch.wav")
powerup_sound = pygame.mixer.Sound("powerup.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# --- Constants ---
WIDTH, HEIGHT = 500, 600
MOVE_SPEED = 25
MAX_LIVES = 3
SCORE_FILE = "highscore.txt"

# --- Tkinter Setup ---
root = tk.Tk()
root.title("🌟 Catch the Falling Stars — Ultimate Cute Edition 🌈")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# --- Game State ---
score = 0
high_score = 0
lives = MAX_LIVES
star_speed = 7
basket = None
current_star = None
score_label = None
lives_label = None
high_label = None
running = False
is_powerup = False

# --- High Score Handling ---
def load_high_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as f:
            return int(f.read())
    return 0

def save_high_score(new_score):
    with open(SCORE_FILE, 'w') as f:
        f.write(str(new_score))

high_score = load_high_score()

# --- Drawing & Utility ---
def draw_background():
    for i in range(0, HEIGHT, 10):
        color = f'#{"%02x"%(15+i//3)}{"%02x"%(20+i//5)}80'
        canvas.create_rectangle(0, i, WIDTH, i + 10, fill=color, outline='')

def create_star():
    global is_powerup
    x = random.randint(30, WIDTH - 30)
    is_powerup = random.randint(1, 10) == 1  # 10% chance
    emoji = "💎" if is_powerup else random.choice(["⭐", "🌟", "✨", "💫"])
    return canvas.create_text(x, 0, text=emoji, font=("Arial", 25))

def sparkle(x, y):
    for _ in range(4):
        emoji = random.choice(["✨", "💖", "💫"])
        s = canvas.create_text(x + random.randint(-10, 10), y - random.randint(5, 15),
                               text=emoji, fill="white", font=("Arial", 10))
        canvas.after(300, lambda s=s: canvas.delete(s))

def update_labels():
    canvas.itemconfig(score_label, text=f"Score: {score} ⭐")
    canvas.itemconfig(lives_label, text=f"Lives: {'❤️' * lives}")
    canvas.itemconfig(high_label, text=f"High Score: {high_score} 🏆")

# --- Movement ---
def move_basket(dx):
    if not running: return
    x, y = canvas.coords(basket)
    if 30 < x + dx < WIDTH - 30:
        canvas.move(basket, dx, 0)

def move_left(event): move_basket(-MOVE_SPEED)
def move_right(event): move_basket(MOVE_SPEED)

# --- Game Over ---
def game_over():
    global running, high_score
    running = False
    pygame.mixer.Sound.play(gameover_sound)
    canvas.delete("all")
    draw_background()
    canvas.create_text(WIDTH//2, HEIGHT//2 - 30, text="💔 Game Over 💔",
                       font=("Comic Sans MS", 26, "bold"), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT//2, text=f"Your Score: {score}",
                       font=("Arial", 18), fill="gold")
    canvas.create_text(WIDTH//2, HEIGHT//2 + 40, text=f"High Score: {high_score} 🏆",
                       font=("Arial", 14), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT//2 + 80, text="Click to Play Again 🎮",
                       font=("Arial", 14), fill="white")
    canvas.bind("<Button-1>", start_game)

# --- Game Loop ---
def game_loop():
    global current_star, score, lives, star_speed, is_powerup, high_score

    if not running:
        return

    canvas.move(current_star, 0, star_speed)
    star_x, star_y = canvas.coords(current_star)

    if star_y >= HEIGHT - 60:
        basket_x, _ = canvas.coords(basket)
        if abs(star_x - basket_x) < 40:
            if is_powerup:
                score += 3
                pygame.mixer.Sound.play(powerup_sound)
            else:
                score += 1
                pygame.mixer.Sound.play(catch_sound)

            sparkle(star_x, star_y)
            canvas.delete(current_star)
            star_speed = 7 + score // 5
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            update_labels()
        else:
            lives -= 1
            update_labels()
            canvas.delete(current_star)
            if lives == 0:
                game_over()
                return

        current_star = create_star()

    root.after(50, game_loop)

# --- Game Start ---
def start_game(event=None):
    global score, lives, star_speed, running, basket, current_star
    global score_label, lives_label, high_label

    canvas.delete("all")
    draw_background()

    score = 0
    lives = MAX_LIVES
    star_speed = 7
    running = True

    basket = canvas.create_text(WIDTH//2, HEIGHT - 40, text="🧺", font=("Arial", 30))
    current_star = create_star()

    score_label = canvas.create_text(10, 10, anchor='nw', fill='white',
                                     font=('Comic Sans MS', 16, 'bold'), text="")
    lives_label = canvas.create_text(WIDTH - 10, 10, anchor='ne', fill='red',
                                     font=('Comic Sans MS', 16, 'bold'), text="")
    high_label = canvas.create_text(WIDTH//2, 10, anchor='n', fill='gold',
                                    font=('Comic Sans MS', 14), text="")

    update_labels()
    game_loop()

# --- Splash Screen ---
def splash_screen():
    canvas.delete("all")
    draw_background()
    canvas.create_text(WIDTH//2, HEIGHT//2 - 50, text="🌟 Catch the Falling Stars 🌟",
                       font=("Comic Sans MS", 26, "bold"), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT//2, text="Use ← and → to move the basket 🧺",
                       font=("Arial", 14), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT//2 + 30, text="💎 Catch gems for bonus points!",
                       font=("Arial", 12), fill="lightblue")
    canvas.create_text(WIDTH//2, HEIGHT//2 + 60, text="Click to Start ✨",
                       font=("Arial", 16), fill="gold")
    canvas.bind("<Button-1>", start_game)

# --- Bindings ---
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# --- Start Game ---
splash_screen()
root.mainloop()

