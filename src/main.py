from generation.generator import Generator
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import time
from queue import Queue
import colors

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
            width=(self.root.winfo_width() - self.frame.winfo_width() - 6), 
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


    def init_buttons(self, background_color, font_color):
        def make_button(text, command):
            return tk.Button(
                self.button_frame,
                text=text,
                command=command,
                highlightbackground=background_color,
                height=1,
                width=7,
                fg='black',
                background='black'
            ).pack(side="top")


        self.button_frame = tk.Frame(self.frame, pady=32, background=background_color)

        make_button("Run", self.start)
        make_button("Stop", self.stop)
        make_button("Reset", self.reset)
        make_button("Save", self.save)
        make_button("Play", self.play)
        make_button("Algorithm", self.change_algorithm)
        make_button("Path", self.find_path)
        make_button("Paint", self.start_painting)
        
        self.button_frame.pack()


    def init_scales(self, background_color, font_color):
        def make_scaler(minimum, maximum, frame):
            return tk.Scale(
                frame,
                from_=minimum,
                to=maximum,
                orient="horizontal",
                resolution=1,
                length=90,
                background=background_color,
                fg=font_color,
                width=8,
                showvalue=0
            )


        def make_label(text, frame):
            return tk.Label(
                frame, 
                text=text, 
                font=('', 11, ''), 
                fg=font_color, 
                background=background_color,
                padx=0
            ).pack()


        def init_scale(label, minimum, maximum):
            frame = tk.Frame(self.frame, pady=8, background=background_color)
            scaler = make_scaler(minimum, maximum, frame)
            make_label(label, frame)
            scaler.pack()
            frame.pack()
            return scaler
            

        self.wall_thick = init_scale("wall thickness", 2, 32)
        self.way_thick = init_scale("way thickness", 2, 32)
        self.speed_scale = init_scale("speed", 0, 10)


    def setup_window(self):
        background_color = '#242424'
        font_color = 'white'
        maze_background_color = '#333333'
        border_color = 'black'

        self.root = tk.Tk()
        self.root.title("Maze generator")
        self.root.configure(background=background_color)

        self.canvas = tk.Canvas(
            self.root, 
            height=self.window_height, 
            width=self.window_width,
            background=maze_background_color,
            highlightbackground=border_color
        )

        self.canvas.pack(side="right")

        self.frame = tk.Frame(self.root, padx=2, pady=0, background=background_color)
        
        self.init_buttons(background_color, font_color)
        self.init_scales(background_color, font_color)
        
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
        self.finish_x = 0
        self.finish_y = 0
        self.init_settings(self.wall_thick.get(), self.way_thick.get())
        self.resize_canvas(self.window_width, self.window_height)
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
            for _ in range(2 ** self.speed_scale.get()):
                pos = next(self.it)
                self.draw_cell(pos[1], pos[0])
                self.finish_x = max(self.finish_x, pos[0])
                self.finish_y = max(self.finish_y, pos[1])
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


    def find_path(self, x=0, y=0):
        
        delta = [[0, -1], [0, 1], [1, 0], [-1, 0]]

        cells_stack = []
        stack = []

        cells_stack.append(self.draw_cell(x, y, "#00ad37"))
        stack.append((x, y))
        visited = set()

        while len(stack):
            pos = stack[-1]
            cell = cells_stack[-1]
            
            visited.add(pos)

            if pos[0] == self.finish_y and pos[1] == self.finish_x:
                return
            
            processed = True
            for d in delta:
                nx = pos[0] + d[0]
                ny = pos[1] + d[1]
                
                if (nx, ny) in visited:
                    continue

                if ny > self.finish_x or nx > self.finish_y or ny < 0 or nx < 0:
                    continue
                
                if not self.level[ny + 1][nx + 1]:
                    continue
                
                stack.append((nx, ny))
                cells_stack.append(self.draw_cell(nx, ny, "#00ad37"))
                processed = False
                break

            if processed:
                stack.pop()
                cells_stack.pop()
                self.canvas.delete(cell)


    def start_painting(self):
        self.status = 'painting'
        self.paint_it = self.paintGenerator()
        self.paint()


    def paint(self):
        if self.status != 'painting':
            return

        try:
            pos, time = next(self.paint_it)
            self.draw_cell(pos[0], pos[1], colors.get_color(time))
            current_time = time
            while current_time == time:
                pos, current_time = next(self.paint_it)
                self.draw_cell(pos[0], pos[1], colors.get_color(current_time))

            self.canvas.update()
            self.root.after(5, self.paint)
        except:
            self.canvas.update()
            self.status = 'idle'


    def paintGenerator(self, x=0, y=0):
        delta = [[0, -1], [0, 1], [1, 0], [-1, 0]]

        bfs = Queue()
        bfs.put(((x, y), 0))
        visited = [[False] * (self.finish_x + 2) for _ in range(self.finish_y + 2)]

        while not bfs.empty():
           
            pos, time = bfs.get()

            yield (pos, time)
            
            for d in delta:
                nx = pos[0] + d[0]
                ny = pos[1] + d[1]
                
                if visited[nx][ny]:
                    continue

                if ny > self.finish_x or nx > self.finish_y or ny < 0 or nx < 0:
                    continue

                if not self.level[ny + 1][nx + 1]:
                    continue

                bfs.put(((nx, ny), time + 1))
                visited[nx][ny] = True


g = MazeGenerator(640, 480, 8)
