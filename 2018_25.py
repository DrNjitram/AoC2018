from codecs import open
import unittest

class TestStringMethods(unittest.TestCase):

    def test_1(self):
        self.assertEqual(part_1('G:\\24daysofcode\\25_1.txt'), 2)

    def test_2(self):
        self.assertEqual(part_1('G:\\24daysofcode\\25_2.txt'), 4)

    def test_3(self):
        self.assertEqual(part_1('G:\\24daysofcode\\25_3.txt'), 3)

    def test_4(self):
        self.assertEqual(part_1('G:\\24daysofcode\\25_4.txt'), 8)


def iterate(to_reduce):
    unique_const_2 = []
    for const in to_reduce:
        for const_2 in to_reduce:
            if const_2 != const:

                if len(const_2 & const) > 0:
                    unique_const_2.append(const_2 | const)
                else:
                    unique_const_2.append(const_2)
        break
    return set(frozenset(i) for i in unique_const_2)


def reduce(constellations):
    unique_const = []

    for i, const in enumerate(constellations):

        to_continue = False
        for const_3 in unique_const:
            if const.issubset(const_3):
                to_continue = True
        if to_continue:
            continue

        super_set = set()
        for const_2 in constellations:
            if const.isdisjoint(const_2) is False:
                super_set = const | const_2

        unique_const.append(super_set)

    unique_const = set(frozenset(i) for i in unique_const)

    #unique_const = iterate(unique_const)
    #unique_const = iterate(unique_const)

    return(len(unique_const), unique_const)

def part_1(file_name):
    with open(file_name) as file:
        inp = file.read().strip()

    inp = inp.split()

    points = {}
    for line in inp:
        line = tuple([int(i) for i in line.split(",")])
        points[line] = None


    def get_manattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2]) + abs(p1[3] - p2[3])

    for point in points:
        const = {point}
        for calc in points:
            if get_manattan(calc, point) < 4:
                const.add(calc)
        points[point] = const

    constellations = list(points.values())



    leng, cost = reduce(constellations)

    return(leng)


unittest.main()
#print(part_1("G:\\24daysofcode\\25_3.txt"))