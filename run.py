from random import randint

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
            if location['row'] in range(row_size):
                self.coordinates = []
            for index in range(size):
                if location['col'] + index in range(col_size):
                    self.coordinates.append({'row': location['row'], 'col': location['col'] + index})
                else:
                    raise IndexError("Column is out of range.")
            else:
                raise IndexError("Row is out of range.")
        elif orientation == 'vertical':
            if location['col'] in range(col_size):
                self.coordinates = []
                for index in range(size):
                    if location['row'] + index in range(row_size):
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
            if board_display[coords['row']][coords['col']] == 'O':
                return False
            elif board_display[coords['row']][coords['col']] == '#':
                raise RuntimeError("Board display inaccurate")
        return True

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

def main():
    """
    Run all program functions
    """
    print_board(board_display)
    
    for turn in range(turns):
        print("Turn:", turn + 1, "of", turns)
        print("Ships left:", len(ship_list))
        print()

main()