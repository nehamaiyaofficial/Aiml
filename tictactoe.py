# Simple Tic Tac Toe Game (CLI Version)

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def tic_tac_toe():
    board = [[" "] * 3 for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        move = input(f"Player {current_player}, enter your move (row and column, e.g., 1 2): ")
        try:
            row, col = map(int, move.strip().split())
            if board[row][col] != " ":
                print("Cell already taken, try again!")
                continue
            board[row][col] = current_player

            if check_winner(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                break

            if is_full(board):
                print_board(board)
                print("It's a tie!")
                break

            current_player = "O" if current_player == "X" else "X"
        except (ValueError, IndexError):
            print("Invalid move. Please enter row and column between 0 and 2.")

if __name__ == "__main__":
    tic_tac_toe()
