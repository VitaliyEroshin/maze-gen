import random

def correct(x, y):
    return x < correct.height and x >= 0 and y < correct.width and y >= 0

def resize(width, height):
    correct.width = width
    correct.height = height

def algorithm(maze, x=0, y=0, seed=0):
    maze[x // 2][y // 2] = True
    yield [x, y]

    delta = [[0, -1], [0, 1], [1, 0], [-1, 0]]

    # random.Random(seed).shuffle(delta)

    random.shuffle(delta)
    for d in delta:
        new_x = x + 2 * d[0]
        new_y = y + 2 * d[1]

        if correct(new_x, new_y):
            if not maze[new_x // 2][new_y // 2]:
                yield [x + d[0], y + d[1]]
                for t in algorithm(maze, x=new_x, y=new_y):
                    yield t