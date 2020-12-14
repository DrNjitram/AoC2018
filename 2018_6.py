from codecs import open
import time
from PIL import Image


def print_image(area, mode = 0):
    palette = [(159, 168, 218), (179, 157, 219), (206, 147, 216), (244, 143, 177), (239, 154, 154), (120, 144, 156), (189, 189, 189), (141, 110, 99), (255, 112, 67), (255, 167, 38), (255, 202, 40), (255, 238, 88), (212, 225, 87),
               (156, 204, 101), (102, 187, 106), (38, 166, 154), (38, 198, 218), (41, 182, 246), (66, 165, 245), (92, 107, 192), (126, 87, 194), (171, 71, 188), (236, 64, 122), (239, 83, 80), (55, 71, 79), (66, 66, 66), (78, 52, 46),
               (216, 67, 21), (239, 108, 0), (255, 143, 0), (249, 168, 37), (158, 157, 36), (85, 139, 47), (46, 125, 50), (0, 105, 92), (0, 131, 143), (2, 119, 189), (21, 101, 192), (40, 53, 147), (69, 39, 160), (106, 27, 154),
               (173, 20, 87), (198, 40, 40), (213, 0, 0), (197, 17, 98), (170, 0, 255), (98, 0, 234), (48, 79, 254), (41, 98, 255), (0, 145, 234), (0, 184, 212), (0, 191, 165), (0, 200, 83), (100, 221, 23), (174, 234, 0), (255, 214, 0),
               (255, 171, 0), (255, 109, 0), (221, 44, 0)]
    image = Image.new('RGB', (len(area), len(area[0])), "black")
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if isinstance(area[i][j], int) and mode == 0:
                pixels[i, j] = palette[area[i][j]]
            if area[i][j] == '#' and mode == 1:
                pixels[i, j] = (255, 255, 255)

    image.show()


def print_field(field):
    for lines in field:
        print(lines)


def calculate_manhattan(point, sources):
    distances = []
    i, j = point
    for z in range(0, len(sources)):
        y, x = sources[z]
        distance = abs(i-x) + abs(j-y)
        distances.append(distance)

    to_return = distances.index(min(distances)) + 1 if distances.count(min(distances)) == 1 else '.'
    return to_return


def calculate_manhattan2(point, sources, limit):
    distances = []
    i, j = point
    for z in range(0, len(sources)):
        y, x = sources[z]
        distance = abs(i-x) + abs(j-y)
        distances.append(distance)
    to_return = '#' if sum(distances) < limit else '.'
    return to_return


def main():
    file = open("G:\\24daysofcode\\input6.txt", 'r')
    inputs = file.readlines()

    start_time = time.time()

    size_x = 0
    size_y = 0
    sources = []
    for points in inputs:
        x = int(points.split(',')[0])
        y = int(points.split(',')[1].strip())
        if x > size_x:
            size_x = x + 20
        if y > size_y:
            size_y = y + 20

        sources.append((x, y))

    field = [['.' for i in range(size_y)] for j in range(size_x)]

    for i in range(0, len(sources)):
        y, x = sources[i]
        field[x][y] = str(chr(i+ord('A')))

    for i in range(size_x):
        for j in range(size_y):
            field[i][j] = calculate_manhattan((i, j), sources)

    print_image(field)


    elegible = set(list(range(1, len(sources))))
    counts = [0 for i in range(len(elegible)+2)]

    for i in range(size_y):
        elegible -= set([field[0][i]])
        elegible -= set([field[size_x-1][i]])
    for i in range(size_x):
        elegible -= set([field[i][0]])
        elegible -= set([field[i][size_y - 1]])

    for i in range(size_x):
        for j in range(size_y):
            element = field[i][j]
            if isinstance(element, int):
                counts[element] += 1

    max_size = 0
    for elements in elegible:
        size = counts[elements]
        if size > max_size:
            max_size = size

    print("Part 1:")
    print(max_size)
    print("Time taken:", round(time.time() - start_time, 2), "seconds")
    start_time = time.time()
    for i in range(size_x):
        for j in range(size_y):
            field[i][j] = calculate_manhattan2((i, j), sources, 10000)

    #print_field(field)
    #print_image(field, 1)

    area = 0
    for i in range(size_x):
        for j in range(size_y):
            element = field[i][j]
            if element == '#':
                area += 1


    print("Part 2:")
    print(area)
    start_time = time.time() - start_time
    print("Time taken:", round(start_time, 2), "seconds")

main()