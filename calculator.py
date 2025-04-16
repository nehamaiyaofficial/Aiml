def calculator():
    print("🧮 Simple Calculator")
    print("Type a math expression like 2 + 3 * 4")
    print("Type 'exit' to quit\n")

    while True:
        expr = input(">>> ")
        if expr.lower() == "exit":
            print("Goodbye!")
            break
        try:
            result = eval(expr)
            print("= ", result)
        except:
            print("Invalid expression. Please try again.")

# Run the calculator
calculator()

