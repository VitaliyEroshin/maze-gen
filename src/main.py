from generation.generator import Generator
import tkinter as tk
import tkinter.filedialog
import time


class MazeGenerator():
    def __init__(self, window_width, window_height, scale):
        self.status ='idle'
        self.scale = scale
        self.window_width = window_width
        self.window_height = window_height
        self.cells_width = window_width // scale
        self.cells_height = window_height // scale

        self.generator = Generator(self.cells_width - 2, self.cells_height - 2)

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
        ).pack(side="top")


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
        self.make_button(self.frame, "Run", self.start)
        self.make_button(self.frame, "Stop", self.stop)
        self.make_button(self.frame, "Reset", self.reset)
        self.make_button(self.frame, "Save", self.save)
        self.make_button(self.frame, "Play", self.play)
        self.make_button(self.frame, "Algorithm", self.change_algorithm)
        self.make_button(self.frame, "Path", self.find_path)

        self.frame.bind('<KeyPress>', self.key_handler)
        self.frame.focus_set()
        self.frame.pack(side="top")


    def draw_cell(self, x, y):
        self.canvas.create_rectangle(
            (x + 1) * self.scale, (y + 1) * self.scale, 
            (x + 2) * self.scale, (y + 2) * self.scale, 
            outline="#a3fff6", 
            fill="#a3fff6"
        )


    def start(self):
        self.status = 'running'
        self.level = [[False] * (self.cells_width - 1) for _ in range(self.cells_height - 1)]
        self.reset()
        self.go()


    def stop(self):
        self.status = 'idle'


    def reset(self):
        self.it = self.generator.generate()
        self.generator.clear()
        self.canvas.delete('all')


    def save(self):
        path = tk.filedialog.asksaveasfilename(
            defaultextension='.txt', filetypes=[("txt file", '*.txt')],
            initialdir='./',
            title="Choose filename"
        )

        with open(path, 'w') as f:
            for row in self.level:
                pretty_row = []
                for x in row:
                    if x:
                        pretty_row.append(' ')
                    else:
                        pretty_row.append('#')
                f.write(''.join(pretty_row) + '\n')


    def go(self):
        if self.status != 'running':
            return

        try:
            pos = next(self.it)
            self.draw_cell(pos[1], pos[0])
            self.level[pos[0] + 1][pos[1] + 1] = True
            self.canvas.update()
            self.root.after(5, self.go)
        except StopIteration:
            self.running = False


    def move_player(self, x, y):
        if not self.level[y + 1][x + 1]:
            return

        if self.icon:
            self.canvas.delete(self.icon)

        self.canvas.create_rectangle(
            (x + 1) * self.scale, (y + 1) * self.scale, 
            (x + 2) * self.scale, (y + 2) * self.scale, 
            outline="#362700", 
            fill="#362700"
        )
        
        self.icon = self.canvas.create_rectangle(
            (x + 1) * self.scale, (y + 1) * self.scale, 
            (x + 2) * self.scale, (y + 2) * self.scale, 
            outline="#fcba03", 
            fill="#fcba03"
        )

        self.player = [x, y]


    def play(self):
        self.status = 'playing'
        self.player = None
        self.icon = None
        self.move_player(0, 0)


    def key_handler(self, key):
        if self.status == 'playing':
            self.player_move_handler(key)


    def player_move_handler(self, key):
        if key.keysym == 'Left':
            self.move_player(self.player[0] - 1, self.player[1])
        elif key.keysym == 'Right':
            self.move_player(self.player[0] + 1, self.player[1])
        elif key.keysym == 'Up':
            self.move_player(self.player[0], self.player[1] - 1)
        elif key.keysym == 'Down':
            self.move_player(self.player[0], self.player[1] + 1)

    
    def change_algorithm(self):
        filenames = tkinter.filedialog.askopenfilename()
        if not filenames:
            return
        
        self.generator.load_algorithm(filenames)
        self.reset()


    def find_path(self, x=1, y=1, parentx=0, parenty=0):
        way = self.canvas.create_rectangle(
            (x) * self.scale, (y) * self.scale, 
            (x + 1) * self.scale, (y + 1) * self.scale, 
            outline="#00ad37", 
            fill="#00ad37"
        )

        if x == self.cells_width - 3 and y == self.cells_height - 3:
            return True

        delta = [[0, -1], [0, 1], [1, 0], [-1, 0]]
        for d in delta:
            nx = x + d[0]
            ny = y + d[1]

            if nx == parentx and ny == parenty:
                continue

            if not self.level[ny][nx]:
                continue
            
            if (self.find_path(nx, ny, x, y)):
                return True
    
        self.canvas.delete(way)
        return False


g = MazeGenerator(640, 480, 16)