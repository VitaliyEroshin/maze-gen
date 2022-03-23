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
        self.root.mainloop()

    def make_button(self, frame, text, command):
        return tk.Button(
            frame,
            text=text,
            command=command,
            highlightbackground="#242424",
            height=1,
            width=7
        )

    def setup_window(self):
        self.root = tk.Tk()
        self.root.title("Maze generator")
        self.root.configure(background="#242424")
        self.canvas = tk.Canvas(
            self.root, 
            height=self.window_height, 
            width=self.window_width,
            background="#333333",
            highlightbackground="black"
        )
        self.canvas.pack(side="right")
        self.frame = tk.Frame(self.root, padx=10, pady=10, background="#242424")
        self.make_button(self.frame, "Run", self.start).pack(side="top")
        self.make_button(self.frame, "Stop", self.stop).pack(side="top")
        self.make_button(self.frame, "Reset", self.reset).pack(side="top")

        self.frame.pack(side="top")

    def draw_cell(self, x, y):
        self.canvas.create_rectangle(
            x, y, x + self.scale, y + self.scale, 
            outline="#a3fff6", 
            fill="#a3fff6"
        )

    def start(self):
        self.running = True
        self.go()

    def stop(self):
        self.running = False

    def reset(self):
        self.it = self.generator.generate()
        self.generator.clear()
        self.canvas.delete('all')

    def go(self):
        if not self.running:
            return

        try:
            pos = next(self.it)
            self.draw_cell(pos[1] * self.scale, pos[0] * self.scale)
            self.canvas.update()
            self.root.after(5, self.go)
        except StopIteration:
            self.running = False


g = MazeGenerator(640, 480, 16)