import tkinter as tk
import random

# --- Game Constants ---
WIDTH = 500
HEIGHT = 600
STAR_SIZE = 30
BASKET_WIDTH = 80
BASKET_HEIGHT = 25
STAR_SPEED = 7
MOVE_SPEED = 25

# --- Setup Window ---
root = tk.Tk()
root.title("🌟 Catch the Falling Stars — Cute Edition 🌈")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# --- Background Gradient (DIY style) ---
for i in range(0, HEIGHT, 10):
    color = f'#{"%02x"%(15+i//3)}{"%02x"%(20+i//5)}80'
    canvas.create_rectangle(0, i, WIDTH, i + 10, fill=color, outline='')

# --- Emoji Basket ---
basket_emoji = "🧺"
basket = canvas.create_text(WIDTH//2, HEIGHT - 40, text=basket_emoji, font=("Arial", 30))

# --- Score Display ---
score = 0
score_label = canvas.create_text(10, 10, anchor='nw', fill='white', font=('Comic Sans MS', 16, 'bold'),
                                 text=f"Score: {score} ⭐")

# --- Star Spawning ---
def create_star():
    x = random.randint(30, WIDTH - 30)
    emoji = random.choice(["⭐", "🌟", "✨", "💫"])
    return canvas.create_text(x, 0, text=emoji, font=("Arial", 25))

current_star = create_star()

# --- Basket Movement ---
def move_basket(dx):
    x, y = canvas.coords(basket)
    if 30 < x + dx < WIDTH - 30:
        canvas.move(basket, dx, 0)

def move_left(event): move_basket(-MOVE_SPEED)
def move_right(event): move_basket(MOVE_SPEED)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# --- Catch Animation ---
def sparkle(x, y):
    for _ in range(5):
        emoji = random.choice(["✨", "💖", "💫"])
        sparkle = canvas.create_text(x + random.randint(-10, 10), y - random.randint(5, 15),
                                     text=emoji, fill="white", font=("Arial", 10))
        canvas.after(300, lambda s=sparkle: canvas.delete(s))

# --- Game Loop ---
def update():
    global current_star, score

    canvas.move(current_star, 0, STAR_SPEED)
    star_x, star_y = canvas.coords(current_star)

    if star_y >= HEIGHT - 60:
        basket_x, basket_y = canvas.coords(basket)
        if abs(star_x - basket_x) < 40:
            score += 1
            sparkle(star_x, star_y)
            canvas.itemconfig(score_label, text=f"Score: {score} ⭐")
        canvas.delete(current_star)
        current_star = create_star()

    root.after(50, update)

update()
root.mainloop()

