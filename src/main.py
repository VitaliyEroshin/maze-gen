from generation.generator import Generator
import tkinter as tk
import tkinter.filedialog
import time


class MazeGenerator():
    def __init__(self, window_width, window_height, scale):
        self.status ='idle'

        self.generator = Generator()

        self.init_settings(16, 32)
        self.resize_canvas(window_width, window_height)

        self.setup_window()

        self.canvas.bind("<Configure>", self.on_resize)
        self.root.mainloop()


    def on_resize(self, event):
        self.canvas.config(
            width=(self.root.winfo_width() - 93), 
            height=(self.root.winfo_height() - 6)
        )

        self.resize_canvas(
            self.canvas.winfo_width(), 
            self.canvas.winfo_height()
        )
        
        self.reset()


    def resize_canvas(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.cells_width = (window_width + self.wall_thickness) // self.scale
        self.cells_height = (window_height + self.wall_thickness) // self.scale

        self.generator.resize(self.cells_width - 2, self.cells_height - 2)


    def init_settings(self, wall_thickness, way_thickness):
        self.wall_thickness = wall_thickness
        self.way_thickness = max(way_thickness, wall_thickness)
        self.scale = (self.wall_thickness + self.way_thickness) // 2


    def setup_window(self):
        def make_button(text, command):
            return tk.Button(
                self.frame,
                text=text,
                command=command,
                highlightbackground="#242424",
                height=1,
                width=7
            ).pack(side="top")


        def make_scaler(minimum, maximum):
            return tk.Scale(
                self.frame,
                from_=minimum,
                to=maximum,
                orient="horizontal",
                resolution=1,
                length=64,
                background="#242424",
                width=8
            )


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

        make_button("Run", self.start)
        make_button("Stop", self.stop)
        make_button("Reset", self.reset)
        make_button("Save", self.save)
        make_button("Play", self.play)
        make_button("Algorithm", self.change_algorithm)
        make_button("Path", self.find_path)

        self.wall_thick = make_scaler(2, 32)
        self.way_thick = make_scaler(2, 32)
        self.speed_scale = make_scaler(0, 10)

        self.wall_thick.pack()
        self.way_thick.pack()
        self.speed_scale.pack()

        self.frame.bind('<KeyPress>', self.key_handler)
        self.frame.focus_set()
        self.frame.pack(side="top")


    def draw_cell(self, x, y, color="#ffffff"):
        return self.canvas.create_rectangle(
            (x + 1) * self.scale, (y + 1) * self.scale, 
            (x + 3) * self.scale - self.wall_thickness, 
            (y + 3) * self.scale - self.wall_thickness, 
            outline=color, 
            fill=color
        )


    def start(self):
        self.init_settings(self.wall_thick.get(), self.way_thick.get())
        self.resize_canvas(self.window_width, self.window_height)
        self.status = 'running'
        self.level = [[False] * (self.cells_width - 2) for _ in range(self.cells_height - 2)]
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
            for _ in range(2 ** self.speed_scale.get()):
                pos = next(self.it)
                self.draw_cell(pos[1], pos[0])
                self.level[pos[0] + 1][pos[1] + 1] = True
                
            self.canvas.update()
            self.root.after(1, self.go)
        except:
            self.status = 'idle'


    def move_player(self, x, y):
        if not self.level[y + 1][x + 1]:
            return

        if self.icon:
            self.canvas.delete(self.icon)

        self.draw_cell(x, y, "#362700")
        
        self.icon = self.draw_cell(x, y, "#fcba03")

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
        way = self.draw_cell(x - 1, y - 1, "#00ad37")

        if x == self.cells_width - 3 and y == self.cells_height - 3:
            return True

        delta = [[0, -1], [0, 1], [1, 0], [-1, 0]]
        for d in delta:
            nx = x + d[0]
            ny = y + d[1]

            if nx == parentx and ny == parenty:
                continue

            if ny == len(self.level) or nx == len(self.level[0]):
                continue
            
            if not self.level[ny][nx]:
                continue
            
            if (self.find_path(nx, ny, x, y)):
                return True
    
        self.canvas.delete(way)
        return False


g = MazeGenerator(640, 480, 8)
