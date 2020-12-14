import numpy

def calculate_pos(x, y, serial):
    id = (x + 1) + 10
    power = id * (y + 1)
    power += serial
    power *= id
    return (power // 100 % 10) - 5

input = int(3999)
grid = numpy.fromfunction(calculate_pos, (300, 300, input))

for width in range(3, 37):
    windows = sum(grid[x:x-width+1 or None, y:y-width+1 or None] for x in range(width) for y in range(width))
    maximum = int(windows.max())
    location = numpy.where(windows == maximum)
    print(width, maximum, location[0][0] + 1, location[1][0] + 1)