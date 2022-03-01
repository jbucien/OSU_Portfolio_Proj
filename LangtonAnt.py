#Author: Jenna Bucien
#Date: 08/12/2021
#Description: A class "Ant" that simulates Langton's Ant, given user inputs of a board size (square),
#the ant's starting position and direction, and number of steps the simulation should run. main()
#calls run_simulation() that uses methods in the Ant class to run the simulation. main() calls print_board
#to display the final board once simulation is complete.

class Ant:
    """
    A class that represents a Langton's Ant simulation. Initialize based on user input.

    ...

    Attributes (Private)
    __________
    _board_size : int
        total number of rows/columns in a square board
    _row : int
        current row of the board the ant is in
    _column : int
        current column of the board the ant is in
    _orientation : int
        the ant's current orientation on the board, where 0 is up, 1 is right, 2 is down, 3 is left
    _steps: int
        the total number of steps that the simulation will run based on user input
    _counter: int
        the current step number in the simulation
    _board_layout: dict
        a pictorial representation of the board, where each key is a row number and each value is a list of the
        row's spaces ('#' for black, '_' for white, '8' for the ant)

    Methods (Public)
    __________
    get_board_layout()
        Return current board layout.
    get_steps()
        Return total number of steps for simulation to run.
    initial_board()
        Initialize beginning state of board based on user input (assume board starts with all white spaces).
    determine_next_orientation()
        Determine which orientation the ant will move based on whether the ant's current position is on a
        white or black space. Call _determine_next_move().
    place_ant()
        Replace the '_' or '#' at the ant's final position with an '8' to represent the ant.
    """

    def __init__(self, board_size, row, column, orientation, steps):
        """
        Initialize all necessary attributes for the ant object. All attributes are private.

        Parameters
        __________
        board_size : int
            total number of rows/columns in a square board
        row : int
            current row of the board the ant is in
        column : int
            current column of the board the ant is in
        orientation : int
            the ant's current orientation on the board, where 0 is up, 1 is right, 2 is down, 3 is left
        steps: int
            the total number of steps that the simulation will run based on user input
        counter: int
            the current step number in the simulation
        board_layout: dict
            a pictorial representation of the board, where each key is a row number and each value is a list of the
            row's spaces
        """
        self._board_size = board_size
        self._row = row
        self._column = column
        self._orientation = orientation
        self._steps = steps
        self._counter = 0
        self._board_layout = {}

    def get_board_layout(self):
        """Return current board layout"""
        return self._board_layout

    def get_steps(self):
        """Return total steps"""
        return self._steps

    def initial_board(self):
        """
        Set up blank board based on user input. Take no additional parameters. Each key is a row
        in the board (starting at 0). Each value is a list of len(row). Each list element is a
        single-character string '_', which represents a white space.
        """
        row_list = ["_" for space in range(0, self._board_size)]
        for row in range(self._board_size):
            self._board_layout[row] = row_list[:]       #makes shallow copy of row_list

    def determine_next_orientation(self):
        """
        Call at the beginning of each step. Take no additional parameters. If user requests 0 steps,
        call ._place_ant() to begin process of displaying board. Otherwise, check if ant is on
        white ('_') or black ('#') space and turn ant orientation 90 degrees right or left, respectively.
        Change current space to opposite color, then call ._determine_next_move() to change ant's position.
        """
        if self._steps == 0:
            self._place_ant()
        elif self._board_layout[self._row][self._column] == '_':
            if self._orientation == 3:
                self._orientation = 0
            else:
                self._orientation += 1
            self._board_layout[self._row][self._column] = '#'
            self._determine_next_move()
        else:
            if self._orientation == 0:
                self._orientation = 3
            else:
                self._orientation -= 1
            self._board_layout[self._row][self._column] = '_'
            self._determine_next_move()

    def _determine_next_move(self):
        """
        Call after ant's orientation is updated. Take no additional parameters. Change ant's current
        row or column position by one space, based on the ant's orientation. If Ant will hit end of board,
        wrap ant to other side of the board. Update step counter.
        """
        if self._orientation == 0 or self._orientation == 2:
            if self._row == 0 and self._orientation == 0:
                self._row = self._board_size - 1
            elif self._row == (self._board_size - 1) and self._orientation == 2:
                self._row = 0
            else:
                if self._orientation == 0:
                    self._row = self._row - 1
                else:
                    self._row = self._row + 1
        else:
            if self._column == 0 and self._orientation == 3:
                self._column = self._board_size - 1
            elif self._column == (self._board_size - 1) and self._orientation == 1:
                self._column = 0
            else:
                if self._orientation == 3:
                    self._column = self._column - 1
                else:
                    self._column = self._column + 1
        self._counter += 1

    def place_ant(self):
        """
        Call after all steps of simulation are complete. Take no additional parameters. Rebind value of
        _board_layout[_row][_column], which represents the ant's current position, from '#' or '_' to '8'.
        Now '8' will represent the ant in print of board_layout. Call self._convert_row_to_string() to
        continue process of displaying final board.
        """
        self._board_layout[self._row][self._column] = '8'
        self._convert_row_to_string()

    def _convert_row_to_string(self):
        """
        Call after the '8' representing the ant is placed in the board. Take no additional parameters.
        Convert each key value in the board_layout dict from a list into a str to prep board_layout
        for printing line-by-line. Return self._board_layout.
        """
        for row in self._board_layout:
            row_str = ""
            for space in self._board_layout[row]:
                row_str += space
            self._board_layout[row] = row_str
        return self._board_layout

def run_simulation(ant_obj):
    """
    Take ant_obj as the parameter. Call ant method .initial_board() to initialize board with 0 steps. Then
    call ant method determine_next_orientation(), which will iterate through every step based on conditions
    of Langton's Ant. Once all steps have been completed, call ant_obj.place_ant() to place ant on current
    space of board. Return the final layout of the board in form of dict.
    """
    ant_obj.initial_board()
    for step in range(ant_obj.get_steps()):
        ant_obj.determine_next_orientation()
    ant_obj.place_ant()
    return ant_obj.get_board_layout()

def print_board(ant_obj):
    """
    Take ant_obj as the parameter. Print each row of final board successively on a separate line to
    display an accurate pictorial representation of the board.
    """
    for row in ant_obj.get_board_layout():
        print(ant_obj.get_board_layout()[row])

def main():
    """
    Collect user input for the information needed to run the Langton Ant's simulation. Information includes:
    number of rows/columns in a square board, ant's starting row/column, ant's starting orientation, and number
    of steps for simulation to run. Use this information to initialize an ant object. Call run_simulation() and
    print_board() functions. Final output is print of final board, where each row of the board is printed on
    its own line.
    Input limitations: (as there is no error handling)
        board_size: int in range(1, 101)
        row: int in range(0,board_size)
        column: int in range(0, board_size)
        orientation: int in range(0,4)
        steps: int
    """
    print("Welcome to Langton’s ant simulation!")
    print("First, please enter a number no larger than 100 for the size of the square board:")
    board_size = int(input())
    print("Now, choose the ant’s starting location. Enter a number as the starting row number (where 0 is the first row from the top):")
    row = int(input())
    print("Please enter a number as the starting column number (where 0 is the first column from the left):")
    column = int(input())
    print("Please choose the ant’s starting orientation, 0 for up, 1 for right, 2 for down, 3 for left:")
    orientation = int(input())
    print("Please enter the number of steps for the simulation:")
    steps = int(input())
    ant_obj = Ant(board_size, row, column, orientation, steps)
    run_simulation(ant_obj)
    print_board(ant_obj)

main()