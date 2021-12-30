from random import randint
import os 

class Board:
    """
    Main Board class. Sets ship size vertically or horizontally.
    Contains methods to fill the board with ships, to check coordinates
    for existing ships in location and to tell the user when they destroyed
    a multi-cell ship.
    """
    def __init__(self, size, orientation, location):
        self.size = size
        if orientation == 'horizontal' or orientation == 'vertical':
            self.orientation = orientation
        else:
            raise ValueError("Value must be 'horizontal' or 'vertical'.")
        
        #Set coordinates of ship on board
        if orientation == 'horizontal':
            if location['row'] in range(row_length):
                self.coordinates = []
                for index in range(size):
                    if location['col'] + index in range(col_length):
                        self.coordinates.append({'row': location['row'], 'col': location['col'] + index})
                    else:
                        raise IndexError("Column is out of range.")
            else:
                raise TypeError("Row is out of range.")
        elif orientation == 'vertical':
            if location['col'] in range(col_length):
                self.coordinates = []
                for index in range(size):
                    if location['row'] + index in range(row_length):
                        self.coordinates.append({'row': location['row'] + index, 'col': location['col']})
                    else:
                        raise IndexError("Row is out of range.")
            else:
                raise IndexError("Column is out of range.")

        if self.filled():
            print_board(board)
            print(" ".join(str(coords) for coords in self.coordinates))
            raise IndexError("A ship already occupies that space.")
        else:
            self.fillBoard()
    
    def filled(self): #method to determine if position is filled by a ship
        for coords in self.coordinates:
            if board[coords['row']][coords['col']] == 1:
                return True
        return False
    
    def fillBoard(self):#method that assigns ship to coordinate
        for coords in self.coordinates:
            board[coords['row']][coords['col']] = 1

    def contains(self, location): #method checks for data validation
        for coords in self.coordinates:
            if coords == location:
                return True
        return False
  
    def destroyed(self): #method checks for status of ships
        for coords in self.coordinates:
            if board_display[coords['row']][coords['col']] == '.':
                return False
            elif board_display[coords['row']][coords['col']] == '#':
                raise RuntimeError("Board display inaccurate")
        return True

#Variables for board and game set up
turns = 40 #number of turns

row_length = 9 #number of rows
col_length = 9 #number of columns

board = [[0] * col_length for x in range(row_length)]
board_display = [["."] * col_length for x in range(row_length)] #list comprehension to display 0's as board that will be passed as argument

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

def search_locations(size, orientation):
    """
    function to return ship locations
    """
    locations = []

    if orientation != 'horizontal' and orientation != 'vertical':
        raise ValueError("Orientation must have a value of either 'horizontal' or 'vertical'.")

    if orientation == 'horizontal':
        if size <= col_length:
            for r in range(row_length):
                for c in range(col_length - size + 1):
                    if 1 not in board[r][c:c+size]:
                        locations.append({'row': r, 'col': c})
    elif orientation == 'vertical':
        if size <= row_length:
            for c in range(col_length):
                for r in range(row_length - size + 1):
                    if 1 not in [board[i][c] for i in range(r, r+size)]:
                        locations.append({'row': r, 'col': c})

    if not locations:
        return 'None'
    else:
        return locations

def random_location():
    """
    function to randomly place ships on board
    """
    size = randint(min_ships_size, max_ships_size)
    orientation = 'horizontal' if randint(0, 1) == 0 else 'vertical'

    locations = search_locations(size, orientation)
    if locations == 'None':
        return 'None'
    else:
        return {'location': locations[randint(0, len(locations) - 1)], 'size': size,\
     'orientation': orientation}

def validate_user_row_choice(choice):
    valid_choices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    if choice.upper() in valid_choices:
        return True
    try:
        number_choice = int(choice)
        print('Numbers are not valid choice, Please choose a letter')
    except ValueError:
        print(f"Please select a valid char from: A, B, C, D, E, F, G, H or I.")
    finally:
        return False


def user_get_row():
    """
    function to get user input for row coordinate
    """
    while True:
        choice = input("Row Guess: ").upper()
        if validate_user_row_choice(choice):
            guess = ord(choice) - 64
            return guess - 1

def user_get_col():
    """
    function to get user input for column coordinate
    """
    while True:
        try:
            guess = int(input("Column Guess: "))
            if guess in range(1, col_length + 1):
                return guess - 1
            else:
                print("\nAre you sure that's on the board?")
        except ValueError:
            print("\nPlease enter a number")

temp = 0
while temp < ships_to_destroy:
    ship_info = random_location()
    if ship_info == 'None':
        continue
    else:
        ship_list.append(Board(ship_info['size'], ship_info['orientation'], ship_info['location']))
        temp += 1
del temp   

def main():
    """
    Run all program functions and active states
    """         
    os.system('clear')
    print('-'*35)
    print('Welcome to Battleships on Python!')
    print(f'Board size is {row_length} rows by {col_length} columns')
    print('For reference, the top left corner is row: 0 and column: 0')
    print(f'You have {turns} turns to seek and destroy all 4 enemy ships ')
    print(f'You will have to guess the row and column coordinates of each ship')
    print(f'Ships can be more than one in length horizontally or vertically.')
    print(f'# means you missed. @ means you hit.')
    print('-'*35)
    player_name = input('Enter your player name to start the game: \n')
    print('-'*35)
    print('-'*35)
    print_board(board_display)
    
    for turn in range(turns):
        print("Turn:", turn + 1, "of", turns)
        print("Ships left:", len(ship_list))
        print()

        guess_coords = {}
        while True:
            guess_coords['row'] = user_get_row()
            guess_coords['col'] = user_get_col()
            if board_display[guess_coords['row']][guess_coords['col']] == '@' or \
                board_display[guess_coords['row']][guess_coords['col']] == '#':
                print("\nYou guessed that one already.")
            else:
                break

        os.system('clear')

        ship_hit = False
        for ship in ship_list:
            if ship.contains(guess_coords):
                print("Hit!")
                ship_hit = True
                board_display[guess_coords['row']][guess_coords['col']] = '@'
                if ship.destroyed():
                    print("Ship Destroyed!")
                    ship_list.remove(ship)
                break
        if not ship_hit:
            board_display[guess_coords['row']][guess_coords['col']] = '#'
            print("You missed!")
        
        print_board(board_display)

        if not ship_list:
            break
    
    if ship_list:
        print("You lose!")
    else:
        print("-" * 35)
        print("All the ships are sunk. You win!")
        print("You have bested a machine!")
        print("-" * 35)

main()

