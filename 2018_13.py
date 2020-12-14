from codecs import open

class Cart:
    def __init__(self, pos, di):
        self.position = pos  # (x, y) tuple
        self.direction = di  # N, S, E, or W (0, 1, 2, 3)
        self.cross_mod = 3  # first left, then ,middle, then right (3, 0, 1)
        self.dead = False

def readmap(field):

    x = len(field[1])
    y = len(field)

    array = [[0 for _ in range(x)] for _ in range(y)]
    carts = []

    parts = {
        " ":0,
        "-":0,
        "|":0,
        "/":1,
        "\\":2,
        "+":3
    }
    directions = {
        "<": 3,
        "v": 2,
        ">": 1,
        "^": 0,
    }

    for i in range(len(field)):
        j = 0
        line = field[i]
        for character in list(line):
            if character in [">", "<", "^", "v"]:
                carts.append(Cart((j, i), directions[character]))
                array[i][j] = 0
            else:
                array[i][j] = parts[character]
            j += 1

    return array, carts


def iterate(field, carts):
    collide = False
    col_xy = (0, 0)
    pos = []
    for cart in carts:
        x, y = cart.position

        direction = cart.direction # N, W, S, E (0, 1, 2, 3), # first left, then ,middle, then right (3, 0, 1)
        new_x, new_y = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}[direction]

        new_x += x
        new_y += y

        next_spot = field[new_y][new_x]
        cart.position = (new_x, new_y)

        if next_spot == 1:  # /
            cart.direction = 2 if direction == 3 else 0 if direction == 1 else 3 if direction == 2 else 1
        elif next_spot == 2:  # \
            cart.direction = 2 if direction == 1 else 1 if direction == 2 else 0 if direction == 3 else 3
        elif next_spot == 3:  # +
            cross = cart.cross_mod
            cart.direction = (cart.direction+cross)%4
            cart.cross_mod = 3 if cross == 1 else 0 if cross == 3 else 1

        pos.append((x, y))
        pos.append((new_x, new_y))

    remaining = []

    for x, y in pos:
        if pos.count((x, y)) > 1:
            for cart in carts:
                if cart.position != (x, y):
                    remaining.append(cart)
            carts = remaining
            remaining = []

    if len(carts) < 2:
        collide = True
        col_xy = carts[0].position

    return field, carts, collide, col_xy


field, carts = readmap([line.replace("\n", "") for line in open("G:\\24daysofcode\\input13.txt").readlines()])

collision = False
while collision is not True:
    field, carts, collision, col_xy = iterate(field, carts)

print(str(col_xy[0])+","+str(col_xy[1]))