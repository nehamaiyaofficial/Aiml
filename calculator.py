import tkinter as tk
import math
from tkinter import messagebox

def evaluate_expression(event=None):  # support keyboard Enter
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

def copy_to_clipboard(event=None):
    root.clipboard_clear()
    root.clipboard_append(entry.get())

def paste_from_clipboard(event=None):
    try:
        pasted = root.clipboard_get()
        entry.insert(tk.END, pasted)
    except:
        messagebox.showerror("Error", "Nothing to paste.")

# Create main window
root = tk.Tk()
root.title("Scientific Calculator")

# --- 🌙 DARK MODE ---
bg_color = "#1e1e1e"
fg_color = "#ffffff"
btn_color = "#333333"
btn_text = "#00ffcc"
entry_bg = "#2d2d2d"

root.configure(bg=bg_color)

# Entry field
entry = tk.Entry(root, width=25, font=('Arial', 24), bd=8, relief='flat',
                 bg=entry_bg, fg=fg_color, insertbackground=fg_color, justify='right')
entry.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

# Buttons layout
buttons = [
    ['7', '8', '9', '÷', 'sin', 'cos'],
    ['4', '5', '6', 'x', 'tan', '√'],
    ['1', '2', '3', '-', 'log', 'ln'],
    ['0', '.', '^', '+', 'π', 'e'],
    ['C', '=', '', '', '', '']
]

# Create and place buttons
for r, row in enumerate(buttons, 1):
    for c, char in enumerate(row):
        if char:
            btn = tk.Button(root, text=char, width=5, height=2, font=('Arial', 18),
                            bg=btn_color, fg=btn_text, activebackground="#444", activeforeground="white"

