from importlib import import_module
from importlib.machinery import SourceFileLoader

class Generator():
    def __init__(self, width, height):
        self.resize(width, height)
        self.algo = import_module('algorithms.dfs')
        self.algo.resize(self.width, self.height)


    def resize(self, width, height):
        self.width = width // 2
        self.height = height // 2
        self.maze = [[False] * (width // 2) for _ in range(height // 2)]
        print(len(self.maze), 'x', len(self.maze[0]))


    def load_algorithm(self, path):
        try:
            self.algo = SourceFileLoader("algo", path).load_module()
            self.algo.resize(self.width, self.height)
            
        except ImportError:
            print("No module found")


    def generate(self):
        for x in self.algo.algorithm(self.maze):
            yield x


    def clear(self):
        for i in range(self.height // 2):
            for j in range(self.width // 2):
                self.maze[i][j] = False
