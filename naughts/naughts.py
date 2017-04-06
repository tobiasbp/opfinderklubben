#!/usr/bin/python3

# Tobias mega fede kryds og bolle


# What length is needed to win
length_to_win = 3

# Size of the (square) board
board_size = 3

# 2 dimensional list holding the game board
#board = board_size * [board_size * "."]

def get_square_board(size):
  board = []
  for row in range(size):
    board.append(size * ["."])
  return board

# Print board to screen
def print_board():
    for row in board:
        for col in row:
            print(col, end="")
        print()
        

# Check if board contains a winning length for pawn type t
def check_win(length, pawn):

    # Check rows
    for row in board:
        # Only works if length == board size!!
        if row.count(pawn) == length:
            return True
    
    # Check cols (No of cols must be = no of rows)
    for col in range(len(board)):
      # Build collumn as list
      this_col = []
      for row in range(len(board)):
        this_col.append(board[row][col])
      if this_col.count(pawn) == length:
        return True
        
    # Top left to buttom right
    this_diag = []
    for pos in range(len(board)):
      this_diag.append(board[pos][pos])
    if this_diag.count(pawn) == length:
        return True

    # bottom left to top right
    this_diag = []
    for pos in range(len(board)):
      this_diag.append(board[pos][2-pos])
    #print("Diag2: " + str(this_diag))
    if this_diag.count(pawn) == length:
        return True
    


# x or o (Immutable tuple!!)
players = ("o","x")

# Whos turn it is
current_player = 0

# Get an empty board
board = get_square_board(board_size)

# Keep track of empty positions on board
empty_positions = board_size * board_size

##################
# Her fra kører programmet
print_board()

#while check_win() != True:
while True:
    
    # Who's turn is it?
    print("Place your pawn player " + players[current_player])
    
    # Get user's input as 1 index coordinates
    # Keep asking while position is not empty
    while True:
      # Keep asking while position is not on board
      while True:
        x = int(input("Input X: "))-1
        y = int(input("Input Y: "))-1
        # Move on if position is on board
        if x >= 0 and x < board_size and y >= 0 and y < board_size:
          break
        else:
          print("Invalid move: Position not on board")
      
      # FIX ME: Check input is an int
      
      # Move on if a players pawn is not at position
      if (board[y][x] not in players):
        break
      else:
        print("Invalid move. Position not empty")

    
    # Update board for current player
    board[y][x] = players[current_player]
    
    # Print board to terminal
    print_board()

    # Did players move end the game?
    if check_win(length_to_win, players[current_player]):
       print("Amazing win for player " + players[current_player])
       # Exit game
       break

    # Keep track of empty positions on board
    empty_positions -= 1

    # Get new empty board of no empty positions left
    if empty_positions == 0:
      board = get_square_board(board_size)
    
    # change turns. Last thing to happen in main loop
    if current_player == 0:
      current_player = 1
    else:
      current_player = 0
    
