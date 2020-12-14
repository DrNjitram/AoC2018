from codecs import open
import numpy


def field_check(field_d, size):
    patches = 0
    for i in range(0, size):
        for j in range(0, size):
            if field_d[i][j] > 1:
                patches += 1
    return patches


def reverse_check(pieces, size, original, no):

    field = create_field(pieces)

    x, y, x_size, y_size = pieces[no]
    for i in range(x_size):
        for j in range(y_size):
            field[x + i][y + j] -= 1
    print(original, field_check(field, size))
    return original == field_check(field, size)


def create_field(pieces):
    test = [[0 for i in range(0, 1000)] for j in range(0, 1000)]
    for piece in pieces:
        x, y, x_size, y_size = piece
        for i in range(x_size):
            for j in range(y_size):
                test[x + i][y + j] += 1

    return test

def main1():
    file = open("G:\\24daysofcode\\input3.txt", 'r')
    inputs = file.readlines()

    size = 1000

    pieces = []

    for line in inputs:

        values = line.split('@')[1]
        x = int(values.split(',')[0].strip())
        y = int(values.split(',')[1].split(':')[0].strip())
        x_size = int(values.split(':')[1].split('x')[0].strip())
        y_size = int(values.split(':')[1].split('x')[1].strip())

        pieces.append((x, y, x_size, y_size))


    field = create_field(pieces)

    original = field_check(field, size)

    print(original)

    for z in range(len(pieces)-1, 0, -1):
        print(z)
        if reverse_check(pieces, size, original, z):
            print(z)
            exit()


main1()
