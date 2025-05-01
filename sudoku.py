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
        self.best_score = self.load_best_score()

    def load_best_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_best_score(self):
        if self.puntaje > self.best_score:
            with open("highscore.txt", "w") as file:
                file.write(str(self.puntaje))
            self.best_score = self.puntaje
            print("🎉 ¡Nuevo récord personal!")

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
            print("\nResuelve el tablero ingresando: fila columna valor")
            self.print_board()
            print(f"\nPuntaje actual: {self.puntaje} | Racha actual: {self.racha} | Récord personal: {self.best_score}")
            print("Si quieres probar otro tablero escribe 1, si quieres salir escribe 2.")
        elif self.flow_state == GameFlow.RETRY_OR_EXIT:
            print("\nHas perdido la racha.")
            print("1. Intentar otro tablero\n2. Salir")

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
                self.board, self.solution = self.build_board()
                return
            elif self.user_input == "2":
                print("¡Perdiste o saliste! Se reinicia tu racha.")
                self.racha = 0
                self.flow_state = GameFlow.RETRY_OR_EXIT
                return
            try:
                coords = self.user_input.split()
                if len(coords) != 3:
                    print("Entrada inválida. Usa el formato: fila columna valor")
                    return
                row, col = map(int, coords[:2])
                val_raw = coords[2].strip().upper()

                if not (1 <= row <= 4 and 1 <= col <= 4):
                    print("Fila o columna fuera de rango (1 a 4).")
                    return

                if self.visualization == "numbers":
                    val = int(val_raw)
                else:
                    try:
                        val = VISUALIZATIONS[self.visualization].index(val_raw) + 1
                    except ValueError:
                        print("Valor inválido para la visualización seleccionada.")
                        return

                if not (1 <= val <= 4):
                    print("Valor fuera de rango.")
                    return

                if self.board[row - 1][col - 1] != 0:
                    print("Esa celda ya fue completada.")
                    return

                if self.solution[row - 1][col - 1] != val:
                    print("❌ Valor incorrecto. Se reinicia la racha.")
                    self.racha = 0
                    self.flow_state = GameFlow.RETRY_OR_EXIT
                    return
                else:
                    self.board[row - 1][col - 1] = val
                    print("✔️ Valor correcto. Celda actualizada.")

                if all(cell != 0 for row in self.board for cell in row):
                    bono = 2 ** self.racha
                    puntos_a_sumar = 10 + (bono if self.racha > 0 else 0)
                    self.puntaje += puntos_a_sumar
                    self.racha += 1
                    print(f"\n🎯 ¡Felicidades! Tablero completo y correcto.")
                    print(f"Sumaste {puntos_a_sumar} puntos. Puntaje total: {self.puntaje}")
                    self.save_best_score()
                    input("\nPresiona Enter para continuar...")
                    self.board, self.solution = self.build_board()

            except ValueError:
                print("Entrada inválida. Asegúrate de usar formato correcto.")

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
