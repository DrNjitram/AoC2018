from codecs import open
from PIL import Image
from time import time

def print_image(field):
    X = len(field[0])
    Y = len(field)

    image = Image.new('RGB', (X, Y), "black")
    pixels = image.load()
    for x in range(X):
        for y in range(Y):
            if field[y][x] == 1:
                pixels[x, y] = 255, 255, 255
            elif field[y][x] == 3:
                pixels[x, y] = 0, 0, 255
            elif field[y][x] == 2 or field[y][x] == 4:
                pixels[x, y] = 0, 255, 255
    image.show()


def print_field(area, limit = 1000000000, start = 0):
    key = {4: '+', 0: '.', 1: '#', 2: '|', 3: '~'}
    print("    0" + " "*49 + "50" + " " * 48 + "100" + " "*47 +"150"+ " "*47 + "200"+ " "*47 + "250")
    for index, line in enumerate(area):
        if index < start:
            continue
        elif index > limit:
            break
        line = [key[_] for _ in line]
        index = "0" + str(index) if index < 10 else index
        print(index, "".join(line))
    print()


with open('G:\\24daysofcode\\17_input2.txt') as file:
    read = [[x.strip() for x in line.split(',')] for line in file.readlines()]
    items = set()
    for line in read:
        type_1 = line[0].split("=")[0]
        value_1 = int(line[0].split("=")[1])

        type_2 = line[1].split("=")[0]
        value_2 = (int(line[1].split("=")[1].split("..")[0]), int(line[1].split("=")[1].split("..")[1]))

        items.add((type_1, value_1, type_2, value_2))

y_bottom = 0
x_min = 490
x_max = 510

for type_1, value_1, type_2, value_2 in items:
    start, end = value_2
    if type_1 == 'x':
        x_min = value_1 if value_1 < x_min else x_min
        x_max = value_1 if value_1 > x_max else x_max
        y_bottom = end if end > y_bottom else y_bottom
    else:
        y_bottom = value_1 if value_1 > y_bottom else y_bottom
        x_min = start if start < x_min else x_min
        x_max = end if end > x_max else x_max


field = [[0 for x in range(x_min - 1, x_max + 1)]for y in range(y_bottom + 2)]
sources = [(0, 500 - x_min)] # y, x ya dork

field[sources[0][0]][sources[0][1]] = 4

for type_1, value_1, type_2, value_2 in items:
    start, end = value_2
    if type_1 == 'x':
        for y in range(start, end + 1):
            field[y][value_1 - x_min] = 1
    else:
        for y in range(start - x_min, end - x_min + 1):
            field[value_1][y] = 1

begin = 1700
limit = 1750

start_time = time()
#print_field(field)
#print(sources)
turns = 762

turn = 0
to_add = []
while len(sources) > 0 or turns > 0:
    #print()
    print("Round:", turn)
    #print(len(sources))
    #print(sources)
    #y_s = [source[0] for source in sources]
    #print(len(sources), min(y_s), max(y_s), 100*max(y_s)//len(field))
    turns -= 1
    turn += 1
    #print("--------------")
    for index, source in enumerate(sources):
        y, x = source
        #print("Going off of:", source)
        #print_field(field, limit, begin)
        if field[y][x] in [1, 3]:
            sources[index] = (-1, -1)

            left_part = "".join([str(_) for _ in field[y][:x]])
            right_part = "".join([str(_) for _ in field[y][x:]])

            start = len(left_part) - len(left_part.split('1')[::-1][0])
            end = len(left_part) + len(right_part.split('1')[0])
            if '4' not in left_part[start:] + right_part[:(end-len(left_part))]:
                y -= 1
        else:
            #print("Going down down")
            while True:
                try:
                    point = field[y+1][x]
                except IndexError:
                    sources[index] = (-1, -1)
                    break
                if point == 3:
                    #print("ended due to found water")
                    break
                if point == 1:
                    #print("ended due to found block")
                    if field[y+1][x-1] == 0:
                        #print("Found peak and creating source", y, x - 1)
                        #print("Removing source", source)
                        field[y][x - 1] = 4
                        to_add.append((y, x - 1))
                        sources[index] = (-1, -1)
                    if field[y+1][x+1] == 0:
                        #print("Found peak and creating source", y, x + 1)
                        #print("Removing source", source)
                        field[y][x + 1] = 4
                        to_add.append((y, x + 1))
                        sources[index] = (-1, -1)

                    break
                y += 1
                field[y][x] = 2
            if sources[index] == (-1, -1):
                continue

        left_part = "".join([str(_) for _ in field[y][:x]])
        right_part = "".join([str(_) for _ in field[y][x:]])
        #print(left_part)
        #print(right_part)
        start = len(left_part) - len(left_part.split('1')[::-1][0])
        end = len(left_part) + len(right_part.split('1')[0])
        total = 0
        for z in range(start, end):
            if field[y + 1][z] in [1, 3]:
                total += 1
        #print("start", start, "end", end)
        #print("total:", total)
        #print("target:", end - start)
        if total == (end - start):
            #print("filling an entire row")
            for z in range(start, end):
                field[y][z] = 3
                if (field[y - 1][z] == 2 or field[y - 1][z] == 4) and (field[y -2][z] == 2 or field[y -2][z] == 4):
                    #print("adding a source due to filled row and no source", y - 1, z)
                    #print("Removing source", source)
                    sources[index] = (-1, -1)
                    to_add.append((y-1, z))
                    field[y-1][z] = 4
            continue
        #print("Filling non-capped row:", y)
        for j in range(start, end):
            if field[y + 1][j] != 3 and field[y + 1][j] != 1:
                try:  off_x = field[y + 1][j - 1]
                except IndexError: off_x = 0
                try: off_y = field[y + 1][j + 1]
                except IndexError: off_y = 0
                if off_x or off_y:
                    for i in range(start, end):
                        if (field[y + 1][i] == 3 or field[y + 1][i] == 1):
                            #Might break
                            if field[y + 1][i + 1] + field[y + 1][i - 1] != 0 or field[y - 1][i] == 2:
                                field[y][i] = 2
                                #print("Setting", y, i,  "to a | with", field[y + 1][i],  "underneath ")
                        elif (y, i) not in sources and (y, i) not in to_add:
                            try:  off_1 = field[y + 1][i - 1]
                            except IndexError: off_1 = -1
                            try: off_3 = field[y][i - 1]
                            except: off_3 = -1
                            try: off_44 = field[y + 1][i - 2]
                            except IndexError: off_44 = -1

                            try: off_2 = field[y + 1][i + 1]
                            except IndexError: off_2 = -1
                            try: off_4 = field[y][i + 1]
                            except: off_4 = -1
                            try: off_22 = field[y + 1][i + 2]
                            except IndexError: off_22 = -1

                            if (off_1 == 1 and off_3 in [2, 3] and off_44 in [3, 1]) or (off_2 == 1and off_4 in [2, 3] and off_22 in [3, 1]):
                                #print("Removing source", source)
                                sources[index] = (-1, -1)
                                to_add.append((y, i))
                                field[y][i] = 4
                                #print("adding a source due to overhang", y, i, "with left, right, (below row) left, below, right", field[y][i - 1], field[y][i + 1], field[y + 1][i - 1], field[y + 1][i], field[y + 1][i + 1])

    sources = [source for source in sources if source != (-1, -1)]
    sources += to_add
    sources = list(set(sources))
    to_add = []
    #print_field(field, limit, begin)
    #print(sources)
    #print()
    #print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------")


print(time()- start_time)
#print_field(field, limit, begin)
#print_image(field)
total = 0
for i in range(y_bottom):
    line = field[i]
    total = total + line.count(2) + line.count(3) + line.count(4)
print(total-1)
total = 0
for i in range(y_bottom):
    line = field[i]
    total = total + line.count(3)
print(total)
#34775

#34777
#34780

#part 2
#27086
