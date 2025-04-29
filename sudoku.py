import os
import random
from enum import Enum

class GameFlow(Enum):
    MAIN_MENU = 0
    PLAYER_NAME = 1
    VISUALIZATION = 2
    DIFICULTY = 3
    GAME = 4
    RETRY_OR_EXIT = 5 

VISUALIZATIONS = {
    "numbers": ["1", "2", "3", "4"],
    "letters": ["A", "B", "C", "D"],
    "symbols": ["■", "◆", "♥", "♠"]
}

SUDOKU_SOLUTIONS = [
    [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [4, 3, 2, 1],
        [2, 1, 4, 3]
    ],
    [
        [4, 3, 2, 1],
        [2, 1, 4, 3],
        [1, 4, 3, 2],
        [3, 2, 1, 4]
    ]
]

class GameState:
    def __init__(self, rows, cols, flow_state=GameFlow.MAIN_MENU):
        self.rows = rows
        self.cols = cols
        self.flow_state = flow_state
        self.game_loop = True
        self.player_name = ""
        self.difficulty = "easy"
        self.board = []
        self.solution = []
        self.visualization = "numbers"
        self.puntaje = 0  
        self.racha = 0    

    def build_board(self):
        solution = random.choice(SUDOKU_SOLUTIONS)
        board = [row.copy() for row in solution]
        empty_cells = 6 if self.difficulty == "easy" else 10
        while empty_cells > 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            if board[row][col] != 0:
                board[row][col] = 0
                empty_cells -= 1
        return board, solution

    def print_board(self):
        symbols = VISUALIZATIONS[self.visualization]
        border = "*" if self.difficulty == "easy" else "-"
        print(border * 20)
        for row in self.board:
            row_display = " | ".join(symbols[val - 1] if val != 0 else " " for val in row)
            print(f"{border} {row_display} {border}")
        print(border * 20)

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        if self.flow_state == GameFlow.MAIN_MENU:
            print("==== BIENVENIDO AL SUDOKU 4x4 ====")
            print("1. Iniciar juego")
            print("2. Salir")
        elif self.flow_state == GameFlow.PLAYER_NAME:
            print("Ingresa tu nombre:")
        elif self.flow_state == GameFlow.VISUALIZATION:
            print("Selecciona la visualización:")
            print("1. Numérico (1-4)")
            print("2. Letras (A-D)")
            print("3. Símbolos (■, ◆, ♥, ♠)")
        elif self.flow_state == GameFlow.DIFICULTY:
            print(f"Hola {self.player_name} 😊. Selecciona la dificultad:")
            print("1. Fácil (6 casillas vacías)")
            print("2. Difícil (10 casillas vacías)")
        elif self.flow_state == GameFlow.GAME:
            print(f"Jugador: {self.player_name} | Dificultad: {self.difficulty}")
            self.print_board()
            print(f"\nEste es el tablero {self.difficulty}.")
            print(f"Puntaje: {self.puntaje}")
            print(f"Racha: {self.racha}")
            print("Si quieres probar otro escribe 1, si quieres salir escribe 2.")
        elif self.flow_state == GameFlow.RETRY_OR_EXIT:
            print("¿Qué quieres hacer?")
            print("1. Generar otro tablero")
            print("2. Salir")

    def update(self, user_input=""):
        self.user_input = user_input.strip()
        self.process_input()

    def process_input(self):
        if self.flow_state == GameFlow.MAIN_MENU:
            if self.user_input == "1":
                self.flow_state = GameFlow.PLAYER_NAME
            elif self.user_input == "2":
                self.game_loop = False
        elif self.flow_state == GameFlow.PLAYER_NAME:
            if not self.user_input:  
                print("¡El nombre no puede estar vacío! Inténtalo de nuevo.")
                return  
            self.player_name = self.user_input
            self.flow_state = GameFlow.VISUALIZATION  
        elif self.flow_state == GameFlow.VISUALIZATION:
            if self.user_input == "1":
                self.visualization = "numbers"
            elif self.user_input == "2":
                self.visualization = "letters"
            elif self.user_input == "3":
                self.visualization = "symbols"
            else:
                print("Selección inválida. Elige 1, 2 o 3.")
                return  
            self.flow_state = GameFlow.DIFICULTY  
        elif self.flow_state == GameFlow.DIFICULTY:
            if self.user_input == "1":
                self.difficulty = "easy"
            elif self.user_input == "2":
                self.difficulty = "hard"
            else:
                print("Selección inválida. Elige 1 o 2.")
                return  
            self.board, self.solution = self.build_board()
            self.flow_state = GameFlow.GAME
        elif self.flow_state == GameFlow.GAME:
            if self.user_input == "1":
                bono = 2 ** self.racha  
                puntos_a_sumar = 10 + (bono if self.racha > 0 else 0)
                self.puntaje += puntos_a_sumar
                self.racha += 1
                print(f"¡Tablero solucionado! Sumaste {puntos_a_sumar} puntos.")
                print(f"Puntaje total: {self.puntaje}")
                self.board, self.solution = self.build_board()
                self.flow_state = GameFlow.GAME
            elif self.user_input == "2":
                print("¡Perdiste o saliste! Se reinicia tu racha.")
                self.racha = 0  
                self.flow_state = GameFlow.RETRY_OR_EXIT
        elif self.flow_state == GameFlow.RETRY_OR_EXIT:
            if self.user_input == "1":
                self.flow_state = GameFlow.VISUALIZATION  
            elif self.user_input == "2":
                self.game_loop = False

def go():
    game_state = GameState(4, 4)
    while game_state.game_loop:
        game_state.draw()
        user_input = input(">> ")
        game_state.update(user_input)

if __name__ == "__main__":
    go()
