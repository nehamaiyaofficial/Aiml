import tkinter as tk
import math

def button_click(symbol):
    current = entry.get()
    if symbol == '=':
        try:
            expression = current.replace('x', '*').replace('÷', '/').replace('^', '**').replace('√', 'math.sqrt')
            expression = expression.replace('π', str(math.pi)).replace('e', str(math.e))

            # Add math. before functions
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
    elif symbol == 'C':
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, symbol)

# Create main window
root = tk.Tk()
root.title("Scientific Calculator")

# Entry field
entry = tk.Entry(root, width=25, font=('Arial', 24), bd=8, relief='ridge', justify='right')
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
                            command=lambda ch=char: button_click(ch))
            btn.grid(row=r, column=c, padx=5, pady=5)

# Run the app
root.mainloop()

