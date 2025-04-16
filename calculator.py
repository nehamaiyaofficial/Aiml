def calculator():
    print("🧮 Simple Calculator")
    print("Enter math expressions like: 2 x 3 + 4 or 10 ÷ 2")
    print("Use '^' for power. Type 'exit' to quit.\n")

    while True:
        expr = input(">>> ")
        if expr.lower() == "exit":
            print("Goodbye!")
            break

        # Replace user-friendly symbols with Python operators
        expr = expr.replace('x', '*')
        expr = expr.replace('X', '*')
        expr = expr.replace('÷', '/')
        expr = expr.replace('^', '**')

        try:
            result = eval(expr)
            print("= ", result)
        except:
            print("Invalid expression. Please try again.")

# Run the calculator
calculator()

