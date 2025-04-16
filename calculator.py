import tkinter as tk
import math

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
    e.widget.config(bg="#ffe6f0")

def on_leave(e):
    e.widget.config(bg=btn_bg)

def toggle_mode():
    global bg_color, entry_bg, btn_bg, entry_fg, btn_fg
    if root.option_get('theme', 'light') == 'light':
        # Switch to dark mode
        bg_color = "#2d2d2d"
        entry_bg = "#444"
        btn_bg = "#555"
        entry_fg = "#ffffff"
        btn_fg = "#ffffff"
        root.option_add('*TButton*highlightBackground', '#333')  # Button border color
        root.option_add('*TButton*highlightColor', '#333')
        root.option_add('*TButton*highlightThickness', 0)
        root.option_add('*Button*background', '#555')
        root.option_add('*Button*foreground', '#ffffff')
        root.option_add('*Button*font', 'Comic Sans MS 16')
        mode_button.config(text="🌞 Day Mode")
        root.option_add('theme', 'dark')
    else:
        # Switch back to light mode
        bg_color = "#ffe6f0"
        entry_bg = "#fff0f6"
        btn_bg = "#f9d6e4"
        entry_fg = "#6a0572"
        btn_fg = "#6a0572"
        root.option_add('*TButton*highlightBackground', '#f8e1ff')
        root.option_add('*TButton*highlightColor', '#f8e1ff')
        root.option_add('*TButton*highlightThickness', 0)
        root.option_add('*Button*background', '#f9d6e4')
        root.option_add('*Button*foreground', '#6a0572')
        root.option_add('*Button*font', 'Comic Sans MS 16')
        mode_button.config(text="🌙 Night Mode")
        root.option_add('theme', 'light')
    
    root.configure(bg=bg_color)
    entry.config(bg=entry_bg, fg=entry_fg)

# Create main window
root = tk.Tk()
root.title("💖 Kawaii Scientific Calculator 💖")
root.resizable(False, False)

# Start with light mode
root.option_add('theme', 'light')
bg_color = "#ffe6f0"
entry_bg = "#fff0f6"
entry_fg = "#6a0572"
btn_bg = "#f9d6e4"
btn_fg = "#6a0572"
font_style = ("Comic Sans MS", 16)

root.configure(bg=bg_color)

# Entry Field
entry = tk.Entry(root, font=("Comic Sans MS", 22), width=25, bd=6, relief="groove",
                 bg=entry_bg, fg=entry_fg, insertbackground=entry_fg, justify='right')
entry.grid(row=0, column=0, columnspan=6, padx=10, pady=20)

# Buttons layout
buttons = [
    ['7', '8', '9', '÷', 'sin', 'cos'],
    ['4', '5', '6', 'x', 'tan', '√'],
    ['1', '2', '3', '-', 'log', 'ln'],
    ['0', '.', '^', '+', 'π', 'e'],
    ['C', '=', '(', ')', '', '']
]

# Create buttons
for r, row in enumerate(buttons, 1):
    for c, char in enumerate(row):
        if char:
            btn = tk.Button(root, text=char, font=font_style, width=4, height=2,
                            bg=btn_bg, fg=btn_fg, relief="raised", bd=3,
                            activebackground="#f5c6e0", activeforeground=btn_fg,
                            command=lambda ch=char: button_click(ch))
            btn.grid(row=r, column=c, padx=6, pady=6)
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

# Add Day/Night toggle button
mode_button = tk.Button(root, text="🌙 Night Mode", font=("Comic Sans MS", 16), command=toggle_mode)
mode_button.grid(row=6, column=0, columnspan=6, pady=10)

# Keyboard Bindings
root.bind('<Return>', evaluate_expression)
root.bind('<KP_Enter>', evaluate_expression)

# Launch the app
root.mainloop()

