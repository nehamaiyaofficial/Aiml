import tkinter as tk
import random

# --- Game Constants ---
WIDTH = 400
HEIGHT = 500
STAR_SIZE = 20
BASKET_WIDTH = 60
BASKET_HEIGHT = 20
STAR_SPEED = 10
MOVE_SPEED = 20

# --- Game Setup ---
root = tk.Tk()
root.title("🌟 Catch the Falling Stars")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="midnight blue")
canvas.pack()

# --- Draw Basket ---
basket = canvas.create_rectangle(WIDTH//2 - BASKET_WIDTH//2, HEIGHT - 40,
                                  WIDTH//2 + BASKET_WIDTH//2, HEIGHT - 40 + BASKET_HEIGHT,
                                  fill="sandy brown")

# --- Score Display ---
score = 0
score_text = canvas.create_text(10, 10, anchor='nw', fill='white', font=('Arial', 14),
                                text=f"Score: {score}")

# --- Create Star ---
def create_star():
    x = random.randint(0, WIDTH - STAR_SIZE)
    return canvas.create_oval(x, 0, x + STAR_SIZE, STAR_SIZE, fill="gold")

current_star = create_star()

# --- Move Basket ---
def move_left(event=None):
    canvas.move(basket, -MOVE_SPEED, 0)

def move_right(event=None):
    canvas.move(basket, MOVE_SPEED, 0)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)

# --- Game Loop ---
def update():
    global current_star, score
    canvas.move(current_star, 0, STAR_SPEED)
    pos = canvas.coords(current_star)

    if pos[3] >= HEIGHT - 40:  # Bottom reached
        basket_coords = canvas.coords(basket)
        if basket_coords[0] < pos[0] < basket_coords[2] or basket_coords[0] < pos[2] < basket_coords[2]:
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
        canvas.delete(current_star)
        current_star = create_star()

    root.after(50, update)

update()
root.mainloop()

