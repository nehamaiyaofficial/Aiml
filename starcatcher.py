import tkinter as tk
import random

# --- Constants ---
MOVE_SPEED = 20
MAX_LIVES = 5
POWER_UPS = ["💖", "🕒", "💣"]

# --- Tkinter Setup ---
root = tk.Tk()
root.title("🌌 Catch the Falling Stars 🌟")
canvas = tk.Canvas(root, bg="#0a0a23")
canvas.pack(fill=tk.BOTH, expand=True)

# --- Global Variables ---
score = 0
lives = MAX_LIVES
level = 1
basket = None
star = None
falling_items = []
running = False
paused = False
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

def create_item():
    width, _ = get_dimensions()
    x = random.randint(30, width - 30)
    is_power = random.random() < 0.1  # 10% chance
    if is_power:
        symbol = random.choice(POWER_UPS)
        tag = "powerup"
    else:
        symbol = random.choice(["⭐", "🌟", "✨", "💫"])
        tag = "star"
    item = canvas.create_text(x, 0, text=symbol, font=("Arial", 25), fill="white", tags=tag)
    falling_items.append(item)

def update_labels():
    canvas.itemconfig("score_label", text=f"Score: {score} ⭐  Level: {level}")
    canvas.itemconfig("lives_label", text=f"Lives: {'❤️' * lives}")

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

def apply_powerup(symbol):
    global lives, falling_items
    if symbol == "💖" and lives < MAX_LIVES:
        lives += 1
    elif symbol == "🕒":
[O        root.after(2000, lambda: None)  # placeholder slowdown
    elif symbol == "💣":
        for item in falling_items:
            if canvas.gettags(item)[0] == "star":
                canvas.delete(item)
        falling_items = [i for i in falling_items if canvas.gettags(i)[0] != "star"]

def game_loop():
    global score, lives, level

    if not running or paused:
        return

    width, height = get_dimensions()

    # Adjust speed based on level
    speed = 5 + level

    for item in falling_items[:]:
[I        canvas.move(item, 0, speed)
        x, y = canvas.coords(item)
        basket_x, basket_y = canvas.coords(basket)

        if y >= height - 60 and abs(x - basket_x) < 40:
            tag = canvas.gettags(item)[0]
            symbol = canvas.itemcget(item, "text")
            if tag == "star":
                score += 1
            elif tag == "powerup":
                apply_powerup(symbol)
            canvas.delete(item)
            falling_items.remove(item)

            # Level up every 10 points
            new_level = score // 10 + 1
            if new_level != level:
                level = new_level

        elif y > height:
            tag = canvas.gettags(item)[0]
            if tag == "star":
                lives -= 1
                if lives == 0:
                    update_labels()
                    game_over()
                    return
            canvas.delete(item)
            falling_items.remove(item)

    if random.random() < 0.05 + level * 0.01:
        create_item()

    update_labels()
    root.after(50, game_loop)

def start_game(event=None):
    root.after(100, setup_game)

def setup_game():
    global basket, score, lives, level, running, exit_button, paused, falling_items

    canvas.delete("all")
    draw_background()
    score, lives, level = 0, MAX_LIVES, 1
    running = True
    paused = False
    falling_items = []
    canvas.focus_set()

    width, height = get_dimensions()
    basket = canvas.create_text(width//2, height - 40, text="🧺", font=("Arial", 30))
    canvas.create_text(10, 10, anchor='nw', fill='white',
                       font=("Comic Sans MS", 16, 'bold'), text="", tags="score_label")
    canvas.create_text(width - 10, 10, anchor='ne', fill='red',
                       font=("Comic Sans MS", 16, 'bold'), text="", tags="lives_label")
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
    canvas.create_text(w//2, h//2 + 10, text="Move 🧺 with ← → | Catch stars ✨",
                       font=("Arial", 14), fill="lightblue")
    canvas.create_text(w//2, h//2 + 40, text="Power-ups: 💖 Extra Life, 🕒 Slow Time, 💣 Boom!",
                       font=("Arial", 12), fill="white")
    canvas.create_text(w//2, h//2 + 80, text="Click to Begin Adventure 🎮",
                       font=("Arial", 14), fill="white")
    canvas.bind("<Button-1>", start_game)

def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

def toggle_pause(event=None):
    global paused
    paused = not paused
    if paused:
        show_pause_message()
    else:
        canvas.delete("pause_msg")
        game_loop()

def show_pause_message():
    w, h = get_dimensions()
    canvas.create_text(w//2, h//2, text="⏸️ Paused", font=("Comic Sans MS", 30, "bold"),
                       fill="white", tags="pause_msg")
    canvas.create_text(w//2, h//2 + 40, text="Press R to Resume",
                       font=("Arial", 16), fill="lightblue", tags="pause_msg")

# --- Key Bindings ---
root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("<Escape>", return_to_menu)
root.bind("<F11>", toggle_fullscreen)
root.bind("<p>", toggle_pause)
root.bind("<r>", toggle_pause)

# --- Start the Game ---
splash_screen()
root.mainloop()

