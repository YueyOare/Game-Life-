import numpy as np
import tkinter as tk
from threading import Thread

n = 30
WIDTH = 1000  # ширина экрана
HEIGHT = 600  # высота экрана
GRID_SIZE = n  # Ширина и высота игрового поля
SQUARE_SIZE = HEIGHT / n  # Размер одной клетки на поле


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cells = np.zeros((n, n))
        self.to_stop = False
        self.title("Life")
        self.frame_1 = tk.Frame(master=self, width=WIDTH * 0.8, height=HEIGHT)
        self.frame_2 = tk.Frame(master=self)
        self.frame_1.grid(row=1, column=1, padx=50, pady=10)
        self.frame_2.grid(row=1, column=2, padx=50, pady=10)
        self.c = tk.Canvas(master=self.frame_1, relief=tk.SUNKEN, width=WIDTH * 0.8,
                           height=HEIGHT)  # Задаем область на которой будем рисовать
        self.c.pack(padx=10, pady=10)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.cells[j, i]:
                    self.c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                                            i * SQUARE_SIZE + SQUARE_SIZE,
                                            j * SQUARE_SIZE + SQUARE_SIZE, fill='black', tags="cell")
                else:
                    self.c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                                            i * SQUARE_SIZE + SQUARE_SIZE,
                                            j * SQUARE_SIZE + SQUARE_SIZE, fill='white', tags="cell")

        self.Obj = dict(run=False)

        self.btn_start = tk.Button(master=self.frame_2, text="Start", width=20, height=5, bg="yellow",
                                   command=lambda: Thread(target=self.start).start())
        self.btn_start_inf = tk.Button(master=self.frame_2, text="Start Infinite", width=20, height=5, bg="yellow",
                                   command=self.start_inf)
        self.btn_stop = tk.Button(master=self.frame_2, text="Stop", width=20, height=5, bg="yellow",
                                  command=lambda: Thread(target=self.stop).start())
        self.btn_end = tk.Button(master=self.frame_2, text="End", width=20, height=5, bg="yellow", command=self.end)
        self.btn_start.pack(padx=10, pady=10)
        self.btn_start_inf.pack(padx=10, pady=10)
        self.btn_stop.pack(padx=10, pady=10)
        self.btn_end.pack(padx=10, pady=10)

        self.dnd_item = None

        self.c.tag_bind("cell", "<ButtonPress-1>", self.button_press)

    def button_press(self, event):
        i = int(event.x // SQUARE_SIZE)
        j = int(event.y // SQUARE_SIZE)
        self.cells[j, i] = 1
        self.c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                                i * SQUARE_SIZE + SQUARE_SIZE,
                                j * SQUARE_SIZE + SQUARE_SIZE, fill='black', tags="cell")

    def next_generation(self):
        cells_new = np.zeros((n, n))
        for i in range(0, n):
            for j in range(0, n):
                if self.cells[i, j]:
                    if i > 0 and j > 0:
                        cells_new[i - 1, j - 1] += 1
                    if i > 0:
                        cells_new[i - 1, j] += 1
                    if i > 0 and j < n - 1:
                        cells_new[i - 1, j + 1] += 1
                    if j > 0:
                        cells_new[i, j - 1] += 1
                    if j < n - 1:
                        cells_new[i, j + 1] += 1
                    if i < n - 1 and j > 0:
                        cells_new[i + 1, j - 1] += 1
                    if i < n - 1:
                        cells_new[i + 1, j] += 1
                    if i < n - 1 and j < n - 1:
                        cells_new[i + 1, j + 1] += 1
        for i in range(0, n):
            for j in range(0, n):
                if self.cells[i, j]:
                    if cells_new[i, j] == 2 or cells_new[i, j] == 3:
                        cells_new[i, j] = 1
                    else:
                        cells_new[i, j] = 0
                else:
                    if cells_new[i, j] == 3:
                        cells_new[i, j] = 1
                    else:
                        cells_new[i, j] = 0
        return cells_new

    def start(self):
        self.Obj['run'] = not self.Obj['run']
        while self.Obj['run']:
            self.cells = self.next_generation()
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if self.cells[j, i]:
                        self.c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                                                i * SQUARE_SIZE + SQUARE_SIZE,
                                                j * SQUARE_SIZE + SQUARE_SIZE, fill='black', tags="cell")
                    else:
                        self.c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                                                i * SQUARE_SIZE + SQUARE_SIZE,
                                                j * SQUARE_SIZE + SQUARE_SIZE, fill='white', tags="cell")

    def start_inf(self):
        self.cells = self.next_generation()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.cells[j, i]:
                    self.c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                                            i * SQUARE_SIZE + SQUARE_SIZE,
                                            j * SQUARE_SIZE + SQUARE_SIZE, fill='black', tags="cell")
                else:
                    self.c.create_rectangle(i * SQUARE_SIZE, j * SQUARE_SIZE,
                                            i * SQUARE_SIZE + SQUARE_SIZE,
                                            j * SQUARE_SIZE + SQUARE_SIZE, fill='white', tags="cell")
        self.after(3, self.start_inf)

    def stop(self):
        self.Obj['run'] = False

    def end(self):
        self.quit()
        return


window = App()  # Основное окно программы
window.mainloop()  # Запускаем программу
