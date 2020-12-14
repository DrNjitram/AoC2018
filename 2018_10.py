import re

with open('G:\\24daysofcode\\input10.txt') as f:
    lines = [l.rstrip('\n') for l in f]
    lines = [[int(i) for i in re.findall(r'-?\d+', l)] for l in lines]

    ranges = []

    for i in range(20000):
        minx = min(x + i * vx for (x, y, vx, vy) in lines)
        maxx = max(x + i * vx for (x, y, vx, vy) in lines)
        miny = min(y + i * vy for (x, y, vx, vy) in lines)
        maxy = max(y + i * vy for (x, y, vx, vy) in lines)
        ranges.append(maxx - minx + maxy - miny)

    i = ranges.index(min(ranges))

    print(i)

    map = [[' '] * 200 for j in range(400)]
    for (x, y, vx, vy) in lines:
        map[y + i * vy][x + i * vx - 250] = '*'

    for m in map:
        line = ''.join(m)
        if line.strip() != "":
            print (line.strip())