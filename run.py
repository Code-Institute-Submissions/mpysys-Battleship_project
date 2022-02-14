from random import randint
import os


class Ship:
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

        # Set coordinates of ship on board
        if orientation == 'horizontal':
            if location['row'] in range(board_size):
                self.coordinates = []
                for index in range(size):
                    if location['col'] + index in range(board_size):
                        self.coordinates.append(
                            {'row': location['row'],
                             'col': location['col'] + index})
                    else:
                        raise IndexError("Column is out of range.")
            else:
                raise TypeError("Row is out of range.")
        elif orientation == 'vertical':
            if location['col'] in range(board_size):
                self.coordinates = []
                for index in range(size):
                    if location['row'] + index in range(board_size):
                        self.coordinates.append(
                            {'row': location['row'] +
                             index, 'col': location['col']})
                    else:
                        raise IndexError("Row is out of range.")
            else:
                raise IndexError("Column is out of range.")

        if self.is_already_taken():
            print_board(sea)
            print(" ".join(str(coords) for coords in self.coordinates))
            raise IndexError(
                f"A ship already occupies that space."
                f"{orientation} en {chr(location['row']+65)}"
                f"{location['col']+1} taille {size}")
        else:
            self.add_to_the_sea()

    def is_already_taken(self):  # method to determine if pos filled by a ship
        for coords in self.coordinates:
            if sea[coords['row']][coords['col']] > 0:
                return True

        return False

    def add_to_the_sea(self):  # method that assigns ship to coordinate
        first = self.coordinates[0]
        last = self.coordinates[len(self.coordinates)-1]
        for coords in self.coordinates:
            if self.orientation == 'vertical':
                sea[coords['row']][coords['col']] = 1
            else:
                sea[coords['row']][coords['col']] = 2
        if len(self.coordinates) == 1:
            sea[first['row']][first['col']] = 7
        elif self.orientation == 'vertical':
            sea[first['row']][first['col']] = 3
            sea[last['row']][last['col']] = 4
        else:
            sea[first['row']][first['col']] = 5
            sea[last['row']][last['col']] = 6

    def contains(self, location):  # method checks for data validation
        for coords in self.coordinates:
            if coords == location:
                return True
        return False

    def destroyed(self):  # method checks for status of ships
        for coords in self.coordinates:
            if board_display[coords['row']][coords['col']] == '.':
                return False
            elif board_display[coords['row']][coords['col']] == '#':
                raise RuntimeError("Board display inaccurate")
        return True


# Variables for board and game set up
player_name = ""  # Current player name
turns = 40  # number of turns

board_size = 9    # board size
sea = [[0] * board_size for x in range(board_size)]
# list comprehension to display .'s as board that will be passed as argument
board_display = [["."] * board_size for x in range(board_size)]

asked_ship_number = 4  # number of ships to destroy
max_ships_size = 5  # max length of ships
min_ships_size = 3    # min length of ships
ship_list = []  # List that stores ship data
not_possible = []  # list of already occupied positions


def print_board(board_array):
    """
    Function that prints the board with alphabetical rows and numerical columns
    """
    print("\n " + "".join(("  "+str(x))[-2:]
          for x in range(1, board_size + 1)))
    for r in range(board_size):
        print(str(chr(r + 65)) + "".join(("  "+display_status(c))
              [-2:] for c in board_array[r]))
    print()


def display_status(value):
    """
    Function adding unicode characters
    """
    if value == 0:
        return " ."
    if value == 1:
        return "\u2588"
    if value == 2:
        return "\u25FC"
    if value == 3:
        return "\u25B2"
    if value == 4:
        return "\u25BC"
    if value == 5:
        return " \u25C0"
    if value == 6:
        return "\u25B6 "
    if value == 7:
        return "\u25C6"
    return value


def find_all_possible_locations(size, orientation):
    """
    function to return ship locations
    """
    locations = []

    if orientation != 'horizontal' and orientation != 'vertical':
        raise ValueError(
            "Orientation must have a value of 'horizontal' or 'vertical'.")

    if size <= board_size:
        if orientation == 'horizontal':
            for r in range(board_size):
                for c in range(board_size - size + 1):
                    if sum(sea[r][c:c + size]) == 0:
                        locations.append({'row': r, 'col': c})
        else:
            for c in range(board_size):
                for r in range(board_size - size + 1):
                    if sum([sea[i][c] for i in range(r, r + size)]) == 0:
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

    locations = find_all_possible_locations(size, orientation)
    if locations == 'None':
        index = size*10
        index = index + 1 if orientation == 'horizontal' else 2
        not_possible.append(index)
        return 'None'
    else:
        random_index = randint(0, len(locations) - 1)
        return {'location': locations[random_index],
                'size': size, 'orientation': orientation}


def analyse_choice(choice):
    if choice == "SURRENDER":
        return True
    return validate_user_row_choice(choice)


def validate_user_row_choice(choice):
    valid_choices = []
    for x in range(board_size):
        valid_choices.append(chr(x+65))
    if choice.upper() in valid_choices:
        return True
    try:
        number_choice = int(choice)
        print('Numbers are not valid choice, Please choose a letter')
    except ValueError:
        print("Please select a valid char from:" +
              " ".join(c+", " for c in valid_choices)+".")
    finally:
        return False


def ask_player_name():
    """
    function to validate user name
    """
    global player_name
    try:
        player_name = input('Enter your player name to start the game: \n')
        while not player_name.isalpha():
            print("You name must only include alphabetic characters.")
            player_name = input('Enter your player name : \n')
    except EOFError as e:
        print(e)


def ask_total_ships():
    """
    function to validate how many ships are on the board
    """
    global asked_ship_number
    try:
        asked_ship_number = input(
            'Enter how many ships to place on the board: \n')
        while not asked_ship_number.isdigit():
            print("Please enter a number")
            asked_ship_number = input(
                'Enter how many ships to place on the board: \n')
    except EOFError as e:
        print(e)


def user_get_row():
    """
    function to get user input for row coordinate and add surrender
    """
    choice = input("Row Guess: ").upper()
    while not analyse_choice(choice):
        choice = input("Row Guess: ").upper()
    if choice == "SURRENDER":
        return -1
    guess = ord(choice) - 64
    return guess - 1


def user_get_col():
    """
    function to get user input for column coordinate
    """
    while True:
        try:
            guess = int(input("Column Guess: "))
            if guess in range(1, board_size + 1):
                return guess - 1
            else:
                print("\nAre you sure that's on the board?")
        except ValueError:
            print("\nPlease enter a number")


def generate_ships():
    """
    Create function to generate ships onto the board and check if valid
    """
    global asked_ship_number
    possible_count = (max_ships_size - min_ships_size + 1) * \
        2  # 2 because vertical or horizontal
    while len(ship_list) < int(asked_ship_number) and len(not_possible) != possible_count:
        location = random_location()
        if location == 'None':
            continue
        else:
            ship_list.append(
                Ship(location['size'],
                     location['orientation'], location['location']))


def main():
    """
    Run all program functions and active states
    """
    os.system('clear')
    print('-'*35)
    print('Welcome to Battleships on Python!')
    print(f'Board size is {board_size} rows by {board_size} columns')
    print(f'You have {turns} turns to beat all enemy ships ')
    print('-'*35)
    print(f'You will have to guess the rows and columns each ship')
    print(f'Ships can be more than one in length horizontally or vertically.')
    print('-'*35)
    print(f'# means you missed. @ means you hit.')
    print('-'*35)
    print(f'You can type "surrender" only once the game has started')
    print('-'*35)
    ask_player_name()
    print(f"Hello {player_name}")
    print('-'*35)
    ask_total_ships()
    print('-'*35)
    generate_ships()
    if len(ship_list) != asked_ship_number:
        print(f'I filled the board with {len(ship_list)}')
        print(f"... playing with {len(ship_list)} ships...")
        input("Press Enter to continue...")
    os.system('clear')
    print('GAME START')
    print_board(board_display)

    for turn in range(turns):
        print("Turn:", turn + 1, "of", turns)
        print("Ships left:", len(ship_list))
        print()

        guess_coords = {}
        surrendered = False

        while True:
            r = user_get_row()
            if r >= 0:
                guess_coords['row'] = r
                guess_coords['col'] = user_get_col()
                if board_display[guess_coords['row']][guess_coords['col']] == '@' or \
                   board_display[guess_coords['row']][guess_coords['col']] == '#':
                    print("\nYou guessed that one already.")
                else:
                    break
            else:
                surrendered = True
                break

        os.system('clear')

        if surrendered:
            print_board(sea)
        else:
            ship_hit = False
            for ship in ship_list:
                if ship.contains(guess_coords):
                    print("Hit!")
                    ship_hit = True
                    board_display[guess_coords['row']
                                  ][guess_coords['col']] = '@'
                    if ship.destroyed():
                        print("Ship Destroyed!")
                        ship_list.remove(ship)
                    break
            if not ship_hit:
                board_display[guess_coords['row']][guess_coords['col']] = '#'
                print("You missed!")

            print_board(board_display)

        if not ship_list or surrendered:
            break

    if ship_list:
        print("You lose!")
    else:
        print("-" * 35)
        print("All the ships are sunk. You win!")
        print("You have bested a machine!")
        print("-" * 35)


main()
