import tkinter as tk
import math
from tkinter import ttk

def evaluate_expression(event=None):
    try:
        expression = entry.get()
        expression = expression.replace('x', '*').replace('÷', '/').replace('^', '**').replace('√', 'math.sqrt')
        expression = expression.replace('π', str(math.pi)).replace('e', str(math.e))
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('log', 'math.log10')
        expression = expression.replace('ln', 'math.log')

        result = str(eval(expression))
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def button_click(symbol):
    if symbol == '=':
        evaluate_expression()
    elif symbol == 'C':
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, symbol)

def on_enter(e):
    e.widget.config(style="Hovered.TButton")

def on_leave(e):
    e.widget.config(style="TButton")

def toggle_mode():
    global btn_style_light, btn_style_dark, mode_button
    if root.option_get('theme', 'light') == 'light':
        # Switch to dark mode
        mode_button.config(text="🌞 Day Mode")
        root.option_add('theme', 'dark')
        style.configure("TButton", background="#555", foreground="#ffffff")
        style.configure("Hovered.TButton", background="#444")
    else:
        # Switch back to light mode
        mode_button.config(text="🌙 Night Mode")
        root.option_add('theme', 'light')
        style.configure("TButton", background="#f9d6e4", foreground="#6a0572")
        style.configure("Hovered.TButton", background="#f5c6e0")
    
    # Update all button styles
    for btn in buttons_list:
        btn.config(style="TButton")

# Create main window
root = tk.Tk()
root.title("💖 Kawaii Scientific Calculator 💖")
root.resizable(False, False)

# Start with light mode
root.option_add('theme', 'light')

root.configure(bg="#ffe6f0")

# Add custom style for rounded buttons and hover effects
style = ttk.Style()
style.configure("TButton",
                font=("Comic Sans MS", 16),
                relief="flat", 
                padding=10, 
                width=6,  # Increased width for bigger buttons
                background="#f9d6e4",  # Light mode background color
                foreground="#6a0572")  # Light mode foreground color
style.configure("Hovered.TButton", background="#f5c6e0")

# Entry Field
entry = tk.Entry(root, font=("Comic Sans MS", 22), width=25, bd=6, relief="groove",
                 bg="#fff0f6", fg="#6a0572", insertbackground="#6a0572", justify='right')
entry.grid(row=0, column=0, columnspan=6, padx=10, pady=20)

# Buttons layout
buttons = [
    ['7', '8', '9', '÷', 'sin', 'cos'],
    ['4', '5', '6', 'x', 'tan', '√'],
    ['1', '2', '3', '-', 'log', 'ln'],
    ['0', '.', '^', '+', 'π', 'e'],
    ['C', '=', '(', ')', '❤️', '⭐']
]

# Create buttons and keep track of them for night mode toggle
buttons_list = []
for r, row in enumerate(buttons, 1):
    for c, char in enumerate(row):
        if char:
            btn = ttk.Button(root, text=char, style="TButton",
                             command=lambda ch=char: button_click(ch))
            btn.grid(row=r, column=c, padx=6, pady=6)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
            buttons_list.append(btn)

# Add Day/Night toggle button
mode_button = ttk.Button(root, text="🌙 Night Mode", style="TButton", command=toggle_mode)
mode_button.grid(row=6, column=0, columnspan=6, pady=10)

# Keyboard Bindings
root.bind('<Return>', evaluate_expression)
root.bind('<KP_Enter>', evaluate_expression)

# Launch the app
root.mainloop()

