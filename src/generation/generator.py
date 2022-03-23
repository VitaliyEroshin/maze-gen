import importlib


class Generator():
    def __init__(self, width, height):
        self.load_algorithm("dfs")
        self.resize(width, height)


    def resize(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[False] * (width // 2) for _ in range(height // 2)]
        self.algo.resize(width, height)


    def load_algorithm(self, path):
        try:
            self.algo = importlib.import_module("algorithms." + path)
            
        except ImportError:
            print("No module found")


    def generate(self):
        for x in self.algo.algorithm(self.maze):
            yield x


    def clear(self):
        for i in range(self.height // 2):
            for j in range(self.width // 2):
                self.maze[i][j] = False
