from generation.generator import Generator
import tkinter as tk
import time

class MazeGenerator():
    def __init__(self, window_width, window_height, scale):
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.cells_width = window_width // scale
        self.cells_height = window_height // scale

        self.generator = Generator(self.cells_width, self.cells_height)

        self.setup_window()

        self.it = self.generator.generate()
        self.go()
        self.root.mainloop()


    def setup_window(self):
        self.root = tk.Tk()
        self.root.title("Maze generator")
        self.canvas = tk.Canvas(
            self.root, 
            height=self.window_height, 
            width=self.window_width,
            background="#333333"
        )
        self.canvas.pack()


    def draw_cell(self, x, y):
        self.canvas.create_rectangle(
            x, y, x + self.scale, y + self.scale, 
            outline="#a3fff6", 
            fill="#a3fff6"
        )


    def go(self):
        try:
            pos = next(self.it)
            self.draw_cell(pos[1] * self.scale, pos[0] * self.scale)
            self.canvas.update()
            self.root.after(5, self.go)
        except StopIteration:
            self.it = self.generator.generate()
            self.generator.clear()
            self.canvas.delete('all')
            self.root.after(5, self.go)


g = MazeGenerator(640, 480, 16)