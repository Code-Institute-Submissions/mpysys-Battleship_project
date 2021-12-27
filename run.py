from random import randint

#Variables for board and game set up
turns = 40 #number of turns

row_length = 9 #number of rows
col_length = 9 #number of columns

board = [[0] * col_length for x in range(row_length)]
board_display = [["O"] * col_length for x in range(row_length)] #list comprehension to display 0's as board that will be passed as argument

ships_to_destroy = 4 #number of ships to destroy
max_ships_size= 5 #max length of ships
min_ships_size = 2 #min length of ships
ship_list = [] #List that stores ship data

def print_board(board_array):
    """
    Function that prints the board with alphabetical rows and numerical columns
    """
    print("\n  " + " ".join(str(x) for x in range(1, col_length + 1)))
    for r in range(row_length):
        print(str(chr(r + 65)) + " " + " ".join(str(c) for c in board_array[r]))
    print()

print_board(board_display)