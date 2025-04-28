import os
from enum import Enum
import random

class GameFlow(Enum):
    MAIN_MENU = 0
    PLAYER_NAME = 1
    DIFICULTY = 2
    GAME = 3
    LEVEL_COMPLETE = 4
    GAME_OVER = 5

class GameState:

    def __init__(self, rows, cols, flow_state):
        self.rows = rows
        self.cols = cols
        self.flow_state = flow_state
        self.game_loop = True
        self.player_name = ""
        self.difficulty = 0
        self.level_complete = False
        self.game_over = False
        self.user_input = ""
        self.available_options = []
        self.board = self.build_board()

    # Build an empty sudoku board
    def build_board(self):
        board = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(random.randint(1, 9))
            board.append(row)
        return board
    
    def draw(self):
        pass

    def update(self, user_input=""):
        self.user_input = user_input
        self.process_input()
        self.available_options = self.calculate_available_options()

    # process the user input according to the current game state
    def process_input(self):
        pass

    # calculate available options for the current game state
    def calculate_available_options(self):
        pass

    # print the current game state options to the console
    def print_options(self):
        print("Menu")
        for i in range(len(self.available_options)):
            option = self.available_options[i]
            print(f"{i + 1}. {option}")


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def go():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    user_input = ""
    game_state = GameState(4, 4, 1, GameFlow.MAIN_MENU)
        
    while game_state.game_loop:
        clear_console()
        game_state.draw()
        user_input = input("Option: ")
        game_state.update(user_input)

go()