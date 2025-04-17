import tkinter as tk
import random

# --- Constants ---
MOVE_SPEED = 20
STAR_SPEED = 6
MAX_LIVES = 3

# --- Tkinter Setup ---
root = tk.Tk()
root.title("🌌 Catch the Falling Stars 🌟")
canvas = tk.Canvas(root, bg="#0a0a23")
canvas.pack(fill=tk.BOTH, expand=True)

# --- Global Variables ---
score = 0
lives = MAX_LIVES
basket = None
star = None
score_label = None
lives_label = None
running = False
exit_button = None
fullscreen = False

# --- Utility Functions ---
def get_dimensions():
    return canvas.winfo_width(), canvas.winfo_height()

def draw_background():
    canvas.delete("bg")
    stars = ["✨", "🌟", "💫", "⭐"]
    width, height = get_dimensions()
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        emoji = random.choice(stars)
        canvas.create_text(x, y, text=emoji, font=("Arial", 8), fill="#444", tags="bg")

def create_star():
    width, _ = get_dimensions()
    x = random.randint(30, width - 30)
    return canvas.create_text(x, 0, text=random.choice(["⭐", "🌟", "✨", "💫"]), font=("Arial", 25), fill="white")

def update_labels():
    canvas.itemconfig(score_label, text=f"Score: {score} ⭐")
    canvas.itemconfig(lives_label, text=f"Lives: {'❤️' * lives}")

def move_basket(dx):
    if basket is None or not canvas.coords(basket):
        return
    x, y = canvas.coords(basket)
    width, _ = get_dimensions()
    if 30 < x + dx < width - 30:
        canvas.move(basket, dx, 0)

def move_left(event): move_basket(-MOVE_SPEED)
def move_right(event): move_basket(MOVE_SPEED)

def return_to_menu():
    global running
    running = False
    canvas.delete("all")
    splash_screen()

def game_over():
    global running
    running = False
    canvas.delete("all")
    draw_background()
    w, h = get_dimensions()
    canvas.create_text(w//2, h//2 - 40, text="💔 Game Over 💔",
                       font=("Comic Sans MS", 26), fill="white")
    canvas.create_text(w//2, h//2, text=f"Final Score: {score}",
                       font=("Arial", 16), fill="gold")
    canvas.create_text(w//2, h//2 + 50, text="Click to Try Again ✨",
                       font=("Arial", 14), fill="white")
    canvas.bind("<Button-1>", start_game)

def game_loop():
    global star, score, lives

    if not running:
        return

    canvas.move(star, 0, STAR_SPEED)
    star_x, star_y = canvas.coords(star)

    if star_y >= canvas.winfo_height() - 60:
        basket_x, _ = canvas.coords(basket)
        if abs(star_x - basket_x) < 40:
            score += 1
        else:
            lives -= 1

        update_labels()
        canvas.delete(star)

        if lives == 0:
            game_over()
            return
        star = create_star()

    root.after(50, game_loop)

def start_game(event=None):
    root.after(100, setup_game)

def setup_game():
    global basket, star, score_label, lives_label, score, lives, running, exit_button

    canvas.delete("all")
    draw_background()
    score, lives = 0, MAX_LIVES
    running = True
    canvas.focus_set()

    width, height = get_dimensions()
    basket = canvas.create_text(width//2, height - 40, text="🧺", font=("Arial", 30))
    star = create_star()
    score_label = canvas.create_text(10, 10, anchor='nw', fill='white', font=('Comic Sans MS', 16, 'bold'))
    lives_label = canvas.create_text(width - 10, 10, anchor='ne', fill='red', font=('Comic Sans MS', 16, 'bold'))
    update_labels()

    if exit_button:
        exit_button.destroy()
    exit_button = tk.Button(root, text="✖ Exit Game", command=return_to_menu,
                            bg="red", fg="white", font=("Arial", 10, "bold"))
    exit_button.place(x=width - 120, y=50)

    game_loop()

def splash_screen():
    root.after(100, setup_splash)

def setup_splash():
    canvas.delete("all")
    draw_background()
    w, h = get_dimensions()
    canvas.create_text(w//2, h//2 - 50, text="🌌 Catch the Falling Stars 🌌",
                       font=("Comic Sans MS", 28, "bold"), fill="white")
    canvas.create_text(w//2, h//2 + 10, text="Move the 🧺 using arrow keys ← →",
                       font=("Arial", 14), fill="lightblue")
    canvas.create_text(w//2, h//2 + 50, text="Click to Begin Your Star Adventure ✨",
                       font=("Arial", 14), fill="white")
    canvas.bind("<Button-1>", start_game)

def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

# --- Key Bindings ---
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<Escape>", return_to_menu)
root.bind("<F11>", toggle_fullscreen)

# --- Start the Game ---
splash_screen()
root.mainloop()

