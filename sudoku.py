import os
import random
from enum import Enum
from datetime import datetime

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

def save_score(player_name, score, record_type="final"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scores_path = "scores.txt"
    entry = f"{now} - Puntaje: {score}"

    # Leer archivo existente
    existing_lines = []
    if os.path.exists(scores_path):
        with open(scores_path, "r") as f:
            existing_lines = f.readlines()

    # Revisar si ya existe el puntaje idéntico para ese jugador
    player_section = False
    for line in existing_lines:
        if line.strip() == f"=== {player_name} ===":
            player_section = True
        elif player_section:
            if line.strip().startswith("==="):  # fin de sección
                player_section = False
            elif line.strip().endswith(f"Puntaje: {score}"):
                return  # Ya existe → no agregar

    # Si no existe, agregar
    found = any(line.strip() == f"=== {player_name} ===" for line in existing_lines)
    lines = existing_lines.copy()
    if not found:
        lines.append(f"=== {player_name} ===\n")
    lines.append(f"{entry}\n")

    with open(scores_path, "w") as f:
        f.writelines(lines)

    # Crear highscores.txt si no existe
    highscores_path = "highscores.txt"
    if not os.path.exists(highscores_path):
        with open(highscores_path, "w") as f:
            pass  # archivo vacío

    # Guardar en highscores solo si record_type == "final"
    if record_type == "final":
        scores = []
        with open(highscores_path, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    name = parts[0].strip().split(".")[-1].strip()
                    date = parts[1].strip()
                    try:
                        pts = int(parts[2].replace("Puntaje:", "").strip())
                        scores.append((name, date, pts))
                    except ValueError:
                        continue
        scores.append((player_name, now, score))
        scores.sort(key=lambda x: x[2], reverse=True)
        with open(highscores_path, "w") as f:
            for i, (name, date, pts) in enumerate(scores[:5], 1):
                f.write(f"{i}. {name} | {date} | Puntaje: {pts}\n")

def show_scores(player_name="", game_state=None):
    print("\n📊 Mostrar puntajes:")
    print("1. Ver mis puntajes")
    print("2. Ver puntajes más altos")
    choice = input(">> ")

    if choice == "1":
        path = "scores.txt"
        if not os.path.exists(path):
            print("Aún no hay puntajes registrados.")
            return
        print(f"\n📄 Puntajes de {player_name}:\n")
        with open(path, "r") as f:
            lines = f.readlines()
            player_section = False
            for line in lines:
                if line.strip() == f"=== {player_name} ===":
                    player_section = True
                    continue
                elif player_section:
                    if line.strip().startswith("==="):  # fin de sección
                        break
                    print(line.strip())
        input("Presiona Enter para continuar...")

    elif choice == "2":
        path = "highscores.txt"
        if not os.path.exists(path):
            print("Aún no hay puntajes altos registrados.")
            input("Presiona Enter para continuar...")
            return
        print("\n🏆 Puntajes más altos:\n")
        with open(path, "r") as f:
            print(f.read())
        input("Presiona Enter para continuar...")

    else:
        print("Opción inválida.")

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
        self.max_puntaje = 0
        self.racha = 0
        self.intentos_restantes = 5

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
        self.intentos_restantes = 5 if self.difficulty == "easy" else 3
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
            print(f"\nPuntaje actual: {self.puntaje} | Racha actual: {self.racha} | Intentos restantes: {self.intentos_restantes}")
            print(f"Máximo puntaje alcanzado: {self.max_puntaje}")
            print("Ingresa: fila columna valor (ej: 1 2 A)")
            print("Escribe 1 para reiniciar, 2 para salir.")
        elif self.flow_state == GameFlow.RETRY_OR_EXIT:
            print("\nHas perdido la racha.")
            print("1. Probar otro tablero con el mismo jugador")
            print("2. Cambiar de jugador")
            print("3. Mostrar puntajes")
            print("4. Salir")

    def update(self, user_input=""):
        self.user_input = user_input.strip()
        self.process_input()

    def process_input(self):
        if self.flow_state == GameFlow.MAIN_MENU:
            if self.user_input == "1":
                self.flow_state = GameFlow.PLAYER_NAME
            elif self.user_input == "2":
                if self.player_name:
                    save_score(self.player_name, self.puntaje, record_type="final")
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
                self.draw()
                return
            elif self.user_input == "2":
                self.racha = 0
                self.flow_state = GameFlow.RETRY_OR_EXIT
                self.draw()
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
                    self.intentos_restantes -= 1
                    print(f"\n❌ Valor incorrecto. Intentos restantes: {self.intentos_restantes}")
                    if self.intentos_restantes == 0:
                        print("🚫 ¡Se acabaron los intentos! Se reinicia la racha.")
                        self.racha = 0
                        self.flow_state = GameFlow.RETRY_OR_EXIT
                        input("Presiona Enter para continuar...")
                    else:
                        input("Presiona Enter para continuar...")
                    self.draw()
                    return

                self.board[row - 1][col - 1] = val

                if all(cell != 0 for row in self.board for cell in row):
                    bono = 2 ** self.racha
                    puntos_a_sumar = 10 + (bono if self.racha > 0 else 0)
                    self.puntaje += puntos_a_sumar
                    self.racha += 1
                    self.max_puntaje = max(self.max_puntaje, self.puntaje)
                    # ✅ ahora pasamos record_type="final" para actualizar highscores
                    save_score(self.player_name, self.puntaje, record_type="final")
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"\n✅ ¡Felicidades! Tablero completo y correcto. ({current_time})")
                    print(f"Sumaste {puntos_a_sumar} puntos. Puntaje total: {self.puntaje}")
                    input("\nPresiona Enter para continuar...")
                    self.board, self.solution = self.build_board()
                    self.draw()
            except ValueError:
                print("Entrada inválida. Asegúrate de usar formato correcto.")
        elif self.flow_state == GameFlow.RETRY_OR_EXIT:
            if self.user_input == "1":
                self.racha = 0
                self.flow_state = GameFlow.VISUALIZATION
            elif self.user_input == "2":
                save_score(self.player_name, self.puntaje, record_type="final")
                self.__init__(self.rows, self.cols)
                self.flow_state = GameFlow.PLAYER_NAME
            elif self.user_input == "3":
                show_scores(self.player_name, self)
                self.draw()
            elif self.user_input == "4":
                save_score(self.player_name, self.puntaje, record_type="final")
                self.game_loop = False
            else:
                print("Opción inválida. Elige 1, 2, 3 o 4.")

def go():
    game_state = GameState(4, 4)
    while game_state.game_loop:
        game_state.draw()
        user_input = input(">> ")
        game_state.update(user_input)

if __name__ == "__main__":
    go()
