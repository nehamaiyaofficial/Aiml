import tkinter as tk

def button_click(symbol):
    current = entry.get()
    if symbol == '=':
        try:
            # Replace user-friendly symbols before evaluating
            expression = current.replace('x', '*').replace('÷', '/').replace('^', '**')
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
root.title("Simple Calculator")

# Entry field
entry = tk.Entry(root, width=20, font=('Arial', 24), bd=8, relief='ridge', justify='right')
entry.grid(row=0, column=0, columnspan=4)

# Button layout
buttons = [
    ['7', '8', '9', '÷'],
    ['4', '5', '6', 'x'],
    ['1', '2', '3', '-'],
    ['0', '.', '^', '+'],
    ['C', '=', '', '']
]

# Create and place buttons
for r, row in enumerate(buttons, 1):
    for c, char in enumerate(row):
        if char:
            btn = tk.Button(root, text=char, width=5, height=2, font=('Arial', 20),
                            command=lambda ch=char: button_click(ch))
            btn.grid(row=r, column=c, padx=5, pady=5)

# Start the app
root.mainloop()

