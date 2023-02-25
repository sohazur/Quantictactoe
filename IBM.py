import pygame as pg
import sys
from random import randint
import json
import qiskit
from qiskit import *
from qiskit.tools.monitor import job_monitor

TOKEN = "API-TOKEN"
IBMQ.save_account(TOKEN)

WIN_SIZE = 450
CELL_SIZE = WIN_SIZE // 3
INF = float('inf')
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)
SCREEN_SIZE = [WIN_SIZE, WIN_SIZE * 4/3]
qturn = 0
loc1 = 0
quantum_move_count = 0

class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.field_image = self.get_scaled_image(path='resources/field.png', res=[WIN_SIZE] * 2)
        self.O_image = self.get_scaled_image(path='resources/owhite.png', res=[CELL_SIZE] * 2)
        self.X_image = self.get_scaled_image(path='resources/xwhite.png', res=[CELL_SIZE] * 2)
        self.bottom = self.get_scaled_image(path='resources/bottom.png', res=[CELL_SIZE*3, CELL_SIZE])
        self.O_green = self.get_scaled_image(path='resources/ogreen.png', res=[CELL_SIZE] * 2)
        self.X_green = self.get_scaled_image(path='resources/xgreen.png', res=[CELL_SIZE] * 2)
        self.O_red = self.get_scaled_image(path='resources/ored.png', res=[CELL_SIZE] * 2)
        self.X_red = self.get_scaled_image(path='resources/xred.png', res=[CELL_SIZE] * 2)
        self.O_blue = self.get_scaled_image(path='resources/oblue.png', res=[CELL_SIZE] * 2)
        self.X_blue = self.get_scaled_image(path='resources/xblue.png', res=[CELL_SIZE] * 2)
        self.O_yellow = self.get_scaled_image(path='resources/oyellow.png', res=[CELL_SIZE] * 2)
        self.X_yellow = self.get_scaled_image(path='resources/xyellow.png', res=[CELL_SIZE] * 2)
        self.qturn = qturn
        self.loc1 = loc1
        self.quantum_move_count = quantum_move_count

        self.game_array = {'1': [INF, 0, ''], '2': [INF, 0, ''], '3': [INF, 0, ''],
                            '4': [INF, 0, ''], '5': [INF, 0, ''], '6': [INF, 0, ''],
                            '7': [INF, 0, ''], '8': [INF, 0, ''], '9': [INF, 0, '']}

        self.player = randint(0, 1)

        self.line_indices_array = [[(0, 0), (0, 1), (0, 2)],
                                   [(1, 0), (1, 1), (1, 2)],
                                   [(2, 0), (2, 1), (2, 2)],
                                   [(0, 0), (1, 0), (2, 0)],
                                   [(0, 1), (1, 1), (2, 1)],
                                   [(0, 2), (1, 2), (2, 2)],
                                   [(0, 0), (1, 1), (2, 2)],
                                   [(0, 2), (1, 1), (2, 0)]]

        self.location_dict = {
            (0, 0): 1,
            (1, 0): 2,
            (2, 0): 3,
            (0, 1): 4,
            (1, 1): 5,
            (2, 1): 6,
            (0, 2): 7,
            (1, 2): 8,
            (2, 2): 9
        }

        self.location_dict_1 = {
            (0, 0): 1,
            (1, 0): 2,
            (2, 0): 3,
            (0, 1): 4,
            (1, 1): 5,
            (2, 1): 6,
            (0, 2): 7,
            (1, 2): 8,
            (2, 2): 9,
            (0, 3): False,
            (1, 3): False,
            (2, 3): False
        }
        self.winner = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Verdana', CELL_SIZE // 4, True)

        # initialise quantum circuit with 9 qubits (all on OFF = 0)
        self.circuit = qiskit.QuantumCircuit(9, 9)

    def check_winner(self):
        for line_indices in self.line_indices_array:
            # sum_line = sum([self.game_array[i][j] for i, j in line_indices])
            sum_line = sum([self.game_array[str(self.location_dict[(i, j)])][0] if self.game_array[str(self.location_dict[(i, j)])][1] == 0 else INF for i, j in line_indices])
            if sum_line in {0, 3}:
                self.winner = 'XO'[sum_line == 0]
                # self.winner_line = [vec2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER,
                # vec2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER]

    def run_game_process(self, mode):

        if mode == 0 or (self.game_steps == 8 and self.quantum_move_count % 2 == 1):
            if self.quantum_move_count % 2 == 0:
                self.classic_run()
            else:
                self.quantum_run2()
        elif mode == 1:
            if self.qturn == 0:
                self.quantum_run1()
            else:
                self.quantum_run2()
        elif (mode == 2 and self.quantum_move_count % 2 == 0) or self.game_steps >= 8:
            self.measure()
            print(self.circuit.draw())

    def quantum_run1(self):
        current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]
        self.loc1 = self.location_dict_1[(col, row)]

        if self.loc1:
            if left_click and self.game_array[str(self.location_dict[(col, row)])][0] == INF and not self.winner:
                self.game_array[str(self.location_dict[(col, row)])][0] = self.player
                self.game_array[str(self.location_dict[(col, row)])][1] = 1
                # self.player = not self.player
                self.game_steps += 1
                self.quantum_move_count += 1
                if self.quantum_move_count <= 2:
                    self.game_array[str(self.location_dict[(col, row)])][2] = 'red'
                elif self.quantum_move_count <= 4:
                    self.game_array[str(self.location_dict[(col, row)])][2] = 'blue'
                elif self.quantum_move_count <= 6:
                    self.game_array[str(self.location_dict[(col, row)])][2] = 'yellow'
                elif self.quantum_move_count <= 8:
                    self.game_array[str(self.location_dict[(col, row)])][2] = 'green'
                # self.quantum_run2()
                self.circuit.h(int(self.loc1) - 1)
                # self.circuit.x(int(location) - 1)
                # self.check_winner()
                self.qturn = 1

    def quantum_run2(self):
        current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]
        location2 = self.location_dict_1[(col, row)]
        if location2:
            if left_click and self.game_array[str(self.location_dict[(col, row)])][0] == INF and not self.winner:
                self.game_array[str(self.location_dict[(col, row)])][0] = self.player
                self.game_array[str(self.location_dict[(col, row)])][1] = 1
                self.player = not self.player
                self.game_steps += 1
                self.quantum_move_count += 1
                if self.quantum_move_count <= 2:
                    self.game_array[str(self.location_dict[(col, row)])][2] = 'red'
                elif self.quantum_move_count <= 4:
                    self.game_array[str(self.location_dict[(col, row)])][2] = 'blue'
                elif self.quantum_move_count <= 6:
                    self.game_array[str(self.location_dict[(col, row)])][2] = 'yellow'
                elif self.quantum_move_count <= 8:
                    self.game_array[str(self.location_dict[(col, row)])][2] = 'green'
                self.circuit.x(int(location2) - 1)
                self.qturn = 0
                # cnot gate
                self.circuit.cx(int(self.loc1) - 1, int(location2) - 1)

    def measure(self):
        IBMQ.load_account()
        provider = IBMQ.get_provider('ibm-q')
        qcomp = provider.get_backend('ibmq_16_melbourne')
        self.circuit.measure(0, 0)
        self.circuit.measure(1, 1)
        self.circuit.measure(2, 2)
        self.circuit.measure(3, 3)
        self.circuit.measure(4, 4)
        self.circuit.measure(5, 5)
        self.circuit.measure(6, 6)
        self.circuit.measure(7, 7)
        self.circuit.measure(8, 8)

        # Execute the circuit on quantum simulator
        job = qiskit.execute(self.circuit, backend=qcomp, shots=1)

        job_monitor(job)
        # Grab results from the job
        result = job.result()

        out = json.dumps(result.get_counts()) # Converts the result.get_counts() into a string
        string = out[2:11]  # Removes unnecessary data from string, leaving us with board

        for i in range(9):
            if string[i] == '1':
                # cement value in the board
                self.game_array[str(9 - i)][1] = 0
            else:
                # make square empty
                self.game_array[str(9 - i)][1] = 0
                self.game_array[str(9 - i)][0] = INF

        # update count (total number of markers on the board)
        self.game_steps = 0
        for i in range(1, 10):
            self.game_array[str(i)][1] = 0
            if self.game_array[str(i)][0] != INF:
                self.game_steps += 1

        # reset qubits
        self.circuit.reset(0)
        self.circuit.reset(1)
        self.circuit.reset(2)
        self.circuit.reset(3)
        self.circuit.reset(4)
        self.circuit.reset(5)
        self.circuit.reset(6)
        self.circuit.reset(7)
        self.circuit.reset(8)

        for i in range(9):
            if string[8 - i] == '1':
                # add pauli x gate
                self.circuit.x(i)

        self.quantum_move_count = 0

        return self.circuit, string, self.game_array, self.game_steps

    def classic_run(self):
        current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]
        location = self.location_dict_1[(col, row)]
        if location:
            if left_click and self.game_array[str(self.location_dict[(col, row)])][0] == INF and not self.winner:
                self.game_array[str(self.location_dict[(col, row)])][0] = self.player
                self.player = not self.player
                self.game_steps += 1
                self.circuit.x(int(location) - 1)
                self.check_winner()

    def draw_objects(self):
        for i in self.location_dict.values():
            obj = self.game_array[str(i)][0]
            cor = list(self.location_dict.keys())[list(self.location_dict.values()).index(i)]
            if obj == 0 or obj == 1:
                if self.game_array[str(i)][1] == 0:
                    self.game.screen.blit(self.X_image if obj else self.O_image, vec2(cor) * CELL_SIZE)
                else:
                    if self.game_array[str(i)][2] == 'red':
                        self.game.screen.blit(self.X_red if obj else self.O_red, vec2(cor) * CELL_SIZE)
                    elif self.game_array[str(i)][2] == 'green':
                        self.game.screen.blit(self.X_green if obj else self.O_green, vec2(cor) * CELL_SIZE)
                    elif self.game_array[str(i)][2] == 'blue':
                        self.game.screen.blit(self.X_blue if obj else self.O_blue, vec2(cor) * CELL_SIZE)
                    elif self.game_array[str(i)][2] == 'yellow':
                        self.game.screen.blit(self.X_yellow if obj else self.O_yellow, vec2(cor) * CELL_SIZE)

    def draw_winner(self):
        if self.winner:
            # pg.draw.line(self.game.screen, 'red', *self.winner_line, CELL_SIZE // 8)
            label = self.font.render(f'Player "{self.winner}" wins!', True, 'white', 'black')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.game.screen.blit(self.bottom, (0, CELL_SIZE*3))
        self.draw_objects()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def print_caption(self):
        pg.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pg.display.set_caption(f'Player "{self.winner}" wins! Press Space to Restart')
        elif self.game_steps == 9:
            pg.display.set_caption(f'Game Over! Press Space to Restart')

    def run(self, mode):
        self.print_caption()
        self.draw()
        self.run_game_process(mode)


class Game:
    def __init__(self, mode):
        self.mode = mode
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()
                if event.key == pg.K_c:
                    self.mode = 0
                elif event.key == pg.K_q:
                    self.mode = 1
                elif event.key == pg.K_m:
                    self.mode = 2

    def run(self):
        while True:
            self.tic_tac_toe.run(self.mode)
            self.check_events()
            pg.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game(0)
    game.run()