import random

def correct(x, y):
    return x < correct.height and x >= 0 and y < correct.width and y >= 0


def resize(width, height):
    correct.width = width
    correct.height = height


def algorithm(maze):
    stack = []
    stack.append([0, 0])
    while stack != []:
        pos = stack[-1]
        yield pos
        x = pos[0]
        y = pos[1]

        maze[x // 2][y // 2] = True

        delta = [[0, -1], [0, 1], [1, 0], [-1, 0]]

        random.shuffle(delta)
        
        processed = True

        for d in delta:
            new_x = x + 2 * d[0]
            new_y = y + 2 * d[1]

            if correct(new_x // 2, new_y // 2):
                if not maze[new_x // 2][new_y // 2]:
                    yield [x + d[0], y + d[1]]
                    stack.append([new_x, new_y])
                    processed = False
                    break
            
        if processed:
            stack.pop()
                    