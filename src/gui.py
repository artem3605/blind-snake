import tkinter as tk
from enum import Enum
import random
from time import sleep
from PIL import Image, ImageDraw, ImageGrab
from FastAlgorithm import FastAlgorithm
from src.SpiralAlgorithm import SpiralAlgorithm
import io
random.seed(0)

class PointType(Enum):
    EMPTY = 0
    FOOD = 1
    BODY = 2
    VISITED = 3

class Config:
    def __init__(self):
        self.window_width = 1600
        self.window_height = 900
        self.map_width = 900
        self.map_height = 900
        self.color_bg = "#202020"
        self.color_line = "#404040"
        self.color_food = "#FF0000"
        self.color_body = "#FFFFFF"
        self.color_visited = "#808080"
        self.show_grid_line = True

class GameMap:
    def __init__(self, rows, cols):
        self.num_rows = rows
        self.num_cols = cols
        self.data = [[PointType.EMPTY for _ in range(cols)] for _ in range(rows)]

    def set_point(self, row, col, point_type):
        self.data[row][col] = point_type

    def get_point(self, row, col):
        return self.data[row][col]

class GameWindow(tk.Tk):
    def __init__(self, title, conf, game_map):
        super().__init__()
        self.title(title)
        self.configure(background=conf.color_bg)
        self.geometry(f"{conf.window_width}x{conf.window_height}")

        self._conf = conf
        self._map = game_map
        sz = min(conf.map_width / game_map.num_cols, conf.map_height / game_map.num_rows)
        self._grid_width = sz
        self._grid_height = sz
        conf.map_width = sz * game_map.num_cols
        conf.map_height = sz * game_map.num_rows

        canvas_x = (conf.window_width - conf.map_width) // 2
        canvas_y = (conf.window_height - conf.map_height) // 2

        self._canvas = tk.Canvas(
            self,
            bg=self._conf.color_bg,
            width=self._conf.map_width,
            height=self._conf.map_height,
            highlightthickness=0,
        )
        self._canvas.place(x=canvas_x, y=canvas_y)

        self._step_counter = tk.StringVar()
        self._step_counter.set("Steps: 0")
        self._step_label = tk.Label(self, textvariable=self._step_counter, bg=self._conf.color_bg, fg="white",
                                    font=("Helvetica", 16))
        self._step_label.place(x=10, y=10)

        self._cell_count = tk.StringVar()
        self._cell_count.set(f"Cells: {game_map.num_rows * game_map.num_cols}")
        self._cell_label = tk.Label(self, textvariable=self._cell_count, bg=self._conf.color_bg, fg="white",
                                    font=("Helvetica", 16))
        self._cell_label.place(x=10, y=40)

        self.frames = []

    def draw_map(self):
        for i in range(self._map.num_rows):
            for j in range(self._map.num_cols):
                self._draw_cell(i, j, self._map.get_point(i, j))

        if self._conf.show_grid_line:
            self._draw_grid_lines()

    def update_cell(self, row, col, point_type):
        self._map.set_point(row, col, point_type)
        self._draw_cell(row, col, point_type)

    def update_step_counter(self, steps):
        self._step_counter.set(f"Steps: {steps}")

    def _draw_cell(self, row, col, point_type):
        x1 = col * self._grid_width
        y1 = row * self._grid_height
        x2 = x1 + self._grid_width
        y2 = y1 + self._grid_height

        if point_type == PointType.FOOD:
            color = self._conf.color_food
        elif point_type == PointType.BODY:
            color = self._conf.color_body
        elif point_type == PointType.VISITED:
            color = self._conf.color_visited
        else:
            color = self._conf.color_bg

        self._canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def _draw_grid_lines(self):
        for i in range(self._map.num_rows + 1):
            y = i * self._grid_height
            self._canvas.create_line(0, y, self._conf.map_width, y, fill=self._conf.color_line)

        for j in range(self._map.num_cols + 1):
            x = j * self._grid_width
            self._canvas.create_line(x, 0, x, self._conf.map_height, fill=self._conf.color_line)



    def capture_frame(self):
        self.update()
        self.update_idletasks()
        ps = self._canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        self.frames.append(img)

    def save_gif(self, filename="game.gif"):
        if self.frames:
            self.frames[0].save(
                filename,
                save_all=True,
                append_images=self.frames[1:],
                duration=100,
                loop=0
            )

def move_body(row, col, algorithm, game_map, window):
    sleep(3)
    window.capture_frame()
    steps = 0
    for cmd in algorithm.step():
        steps += 1
        prev_x = row
        prev_y = col
        if cmd == "ERROR":
            print("ERROR")
            break
        if cmd == "RIGHT":
            col = (col + 1) % game_map.num_cols
        elif cmd == "LEFT":
            col = (col - 1 + game_map.num_cols) % game_map.num_cols
        elif cmd == "UP":
            row = (row - 1 + game_map.num_rows) % game_map.num_rows
        elif cmd == "DOWN":
            row = (row + 1) % game_map.num_rows

        if game_map.get_point(row, col) == PointType.FOOD:
            game_map.set_point(row, col, PointType.BODY)
            window.update_cell(row, col, PointType.BODY)
            window.update_cell(prev_x, prev_y, PointType.VISITED)
            print("Game finished")
            window.capture_frame()
            # window.save_gif("game.gif")
            # print("GIF saved")
            return

        game_map.set_point(row, col, PointType.BODY)
        window.update_cell(row, col, PointType.BODY)
        window.update_cell(prev_x, prev_y, PointType.VISITED)
        window.capture_frame()

        sleep(0.0001)
        window.update_step_counter(steps)


def play_fast_algorithm(A, B, row, col, game_map, window):
    alg = FastAlgorithm(max_s=A * B, k=26)
    move_body(row, col, alg, game_map, window)


def play_spiral_algorithm(A, B, row, col, game_map, window):
    alg = SpiralAlgorithm()
    move_body(row, col, alg, game_map, window)


if __name__ == "__main__":
    config = Config()
    A = 2
    B = 20
    game_map = GameMap(rows=A, cols=B)
    row = random.randint(0, A - 1)
    col = random.randint(0, B - 1)
    row_finish = 0
    col_finish = 3

    game_map.set_point(row, col, PointType.BODY)
    game_map.set_point(row_finish, col_finish, PointType.FOOD)

    window = GameWindow("Game Window", config, game_map)
    window.draw_map()
    import threading
    threading.Thread(target=play_spiral_algorithm, args=(A, B, row, col, game_map, window), daemon=True).start()

    window.mainloop()
