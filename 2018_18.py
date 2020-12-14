from codecs import open
from time import time

key = {".": 0, "|": 1, "#": 2}
with open('G:\\24daysofcode\\input_18.txt') as file:
    field = [[key[char] for char in list(line.strip())]  for line in file.readlines()]


def print_field(area):
    key = { 0: '.', 1: '|', 2: '#'}
    for line in area:
        line = [key[_] for _ in line]
        print("".join(line))


def get_adjecent(acres, co_ordinate):
    Y = len(acres) - 1
    X = len(acres[0]) - 1

    x, y = co_ordinate

    if y == 0:
        if x == 0:
            return (1, 1), (1, 0), (0, 1)
        elif x == X:
            return (1, 0), (0, -1), (1, -1)
        else:
            return (0, -1), (1, -1), (1, 0), (1, 1), (0, 1)
    elif y == Y:
        if x == 0:
            return (-1, 0), (-1, 1), (0, 1)
        elif x == X:
            return (0, -1), (-1, -1), (-1, 0)
        else:
            return (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)

    if x == 0:
        return (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)
    if x == X:
        return (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)

    return (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)


def simulate(acres):
    return_field = [[0 for x in range(len(acres[0]))] for y in range(len(acres))]
    for y in range(len(acres)):
        for x in range(len(acres[0])):
            point = acres[y][x]
            to_check = get_adjecent(acres, (x, y))
            adjecent = [acres[y + co[0]][x + co[1]] for co in to_check]
            #print(y, x, adjecent)
            if point == 0 and adjecent.count(1) > 2:
                return_field[y][x] = 1
            elif point == 1 and adjecent.count(2) > 2:
                return_field[y][x] = 2
            elif point == 2 and (adjecent.count(1) < 1 or adjecent.count(2) < 1):
                return_field[y][x] = 0
            else:
                return_field[y][x] = point
    return return_field


def get_score(acres):
    lumber = 0
    trees = 0
    for line in field:
        trees += line.count(1)
        lumber += line.count(2)
    return trees * lumber

start_time = time()
#print_field(field)

print()
# 412 to 439: 27
cycle = [0 for _ in range(28)]

for _ in range(439):
    field = simulate(field)
    if _ > 410:
        cycle[_ - 411] = get_score(field)
# 0 = 412
# 27 = 439
target = 1000000000

target = (target - 412) % 28

score = cycle[target]
print(cycle)
print(score)
#print_field(field)

print(time() - start_time)