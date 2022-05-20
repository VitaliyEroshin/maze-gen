import random


def correct(position):
    return position[0] < correct.height and position[0] >= 0 \
        and position[1] < correct.width and position[1] >= 0


def resize(width, height):
    correct.width = width
    correct.height = height


class DisjointSet2D:
    def __init__(self, width, height):
        self.set = []
        for i in range(height):
            self.set.append([])
            for j in range(width):
                self.set[i].append([i, j])

        self.num_sets = height * width


    def find(self, i, j):
        if self.set[i][j] != [i, j]:
            pos = self.find(self.set[i][j][0], self.set[i][j][1])
            self.set[i][j] = pos
            return pos
        else:
            return [i, j]


    def union(self, first, second):
        first_set = self.find(first[0], first[1])
        second_set = self.find(second[0], second[1])
        self.set[first_set[0]][first_set[1]] = second_set
        self.num_sets -= 1
        return


def algorithm(maze):
    height = len(maze)
    width = len(maze[0])
    dsu = DisjointSet2D(width, height)
    resize(width, height)

    vertices_set = []
    for i in range(height):
        for j in range(width):
            vertices_set.append([i, j])

    random.shuffle(vertices_set)

    while dsu.num_sets != 1:
        for vertex in vertices_set:
            delta = [[0, -1], [0, 1], [1, 0], [-1, 0]]
            random.shuffle(delta)
            for d in delta:
                neighbor = [vertex[0] + d[0], vertex[1] + d[1]]
                if not correct(neighbor):
                    continue

                if dsu.find(vertex[0], vertex[1]) != dsu.find(neighbor[0], neighbor[1]):
                    dsu.union(vertex, neighbor)
                    yield [2 * vertex[0], 2 * vertex[1]]
                    yield [2 * vertex[0] + d[0], 2 * vertex[1] + d[1]]
                    yield [2 * (vertex[0] + d[0]), 2 * (vertex[1] + d[1])]
                    break
