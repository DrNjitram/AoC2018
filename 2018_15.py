from astar import astar
import unittest
from time import time

class TestStringMethods(unittest.TestCase):

    def test_1(self):
        self.assertEqual(compute('G:\\24daysofcode\\15_2.txt'), (47, 590, 27730))

    def test_2(self):
        self.assertEqual(compute('G:\\24daysofcode\\15.txt'), (37, 982, 36334))

    def test_3(self):
        self.assertEqual(compute('G:\\24daysofcode\\15_3.txt'), (46, 859, 39514))

    def test_4(self):
        self.assertEqual(compute('G:\\24daysofcode\\15_4.txt'), (54, 536, 28944))

    def test_5(self):
        self.assertEqual(compute('G:\\24daysofcode\\15_5.txt'), (20, 937, 18740))

    def test_6(self):
        self.assertEqual(compute('G:\\24daysofcode\\15_6.txt'), (35, 793, 27755))


class Creature:
    def __init__(self, cr, position, health = 200, attack = 3):
        self.t = cr
        self.h = health
        if self.t == 'E':
            self.a = attack
        else:
            self.a = 3
        self.pos = position
        self.id = cr + str(id(self))
        self.attacking = False
        self.alive = True

    def get_hit(self, attack):
        self.h -= attack
        #print("remaining health:", self.h)
        if self.h < 1:
            self.alive = False
            return True
        return False

    def move(self, new_pos):
        self.pos = new_pos

    def get_x(self):
        x, y = self.pos
        return x

    def get_y(self):
        x, y = self.pos
        return y


def initiate(area, att):
    with open(area) as area:
        area = area.read()
        area = area.split("\n")
        area = [list(_.strip()) for _ in area]
        creatures = []

        for y in range(len(area)):
            for x in range(len(area[0])):
                char = area[y][x]
                if char in "EG":
                    creatures.append(Creature(char, (x, y), attack=att))

    return area, creatures


def get_walled(area):
    return [[{"#": 1, "G": 1, "E": 1, ".": 0, "?": 0}[k] for k in i] for i in area]


def print_field(area, special = None):
    if special is None:
        for line in area:
            line = [str(_) for _ in line]
            print("".join(line))
    else:
        x = [d[1] for d in special]
        y = [d[0] for d in special]

        for i, line in enumerate(area):
            line = [str(_) for _ in line]
            if i in y:
                for z in range(len(x)):
                    if y[z] == i:
                        line[x[z]] = 'X'
            print("".join(line))


def load_pl():
    with open('G:\\24daysofcode\\15_players.txt') as file:
        new_pl = [line.strip().split(' ') for line in file.readlines()]
        new_proper = []
        for thing in new_pl:
            id = thing[0]
            gob = id[0]
            x = int(thing[1][1:].split(',')[0])
            y = int(thing[2].split(')')[0])
            hp = int(thing[3])
            new_proper.append(Creature(gob, (x, y), hp))
    return new_proper


def print_players(creatures, mode = 0):
    if type(creatures) == type([]):
        for cr in creatures:
            print(cr.id,cr.pos, cr.h)
    else:
        if mode == 0:
            print(creatures.id, creatures.pos, creatures.h)
        else:
            return creatures.id, creatures.pos, creatures.h


def select_enemy(opponents):
    health = [a.h for a in opponents]

    for i in range(len(health)):
        health[i] = 201 if health[i] < 0 else health[i]

    select_on_health = []
    for enemy in opponents:
        if enemy.h == min(health):
            select_on_health.append(enemy)

    if len(select_on_health) > 1:
        positions = []
        for cr in select_on_health:
            positions.append((cr.pos, cr.pos))
        positions = select_closest(positions)
        for enemy in select_on_health:
            if enemy.pos == positions:
                return enemy
    else:
        return select_on_health[0]


def select_closest(distances):
    low_y = min([d[1][1] for d in distances])
    remaining = []
    for path in distances:
        x, y = path[1]
        if y == low_y:
            remaining.append(path)

    if len(remaining) == 1:
        return remaining[0][0]
    else:
        low_x = min([d[1][0] for d in remaining])
        for path in distances:
            x, y = path[1]
            if x == low_x:
                return path[0]


def del_by_id(id, cre):
    to_return = []
    for thing in cre:
        if thing.id != id:
            to_return.append(thing)
    return to_return


def re_order(creatures, debug = False):
    new_order = []
    positions = []
    types = []
    for cr in creatures:
        if cr.alive or cr.h > 1:
            positions.append((cr.pos, cr.pos))
            types.append(cr.t)
        elif cr.t == 'E':
            print("An elf died with attack", cr.a)
            exit()

    if 'E' not in types or 'G' not in types:
        sum_health = 0
        for cr in creatures:
            if cr.alive:
                sum_health += cr.h
        if debug is False: print_players(creatures)
        return -1, sum_health

    while len(positions) > 0:
        first = select_closest(positions)
        for cr in creatures:
            if first == cr.pos and cr.alive:
                new_order.append(cr)
                break
        positions.remove((first, first))

    return new_order


def act(area, creature, enemies, debug, monitor = None):
    if monitor is not None: print("Turn:", creature.id, creature.pos, creature.h)

    x_cr, y_cr = creature.pos
    target_creature = "G" if creature.t == "E" else "E"

    creature.attacking = False
    for x_d, y_d in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if area[y_cr + y_d][x_cr + x_d] == target_creature:
            creature.attacking = True

    if creature.attacking:
        to_attack = []
        for enemy in enemies:
            if enemy.t == target_creature:
                enemy_x, enemy_y = enemy.pos
                if abs(enemy_x-x_cr) + abs(enemy_y - y_cr) == 1:
                    to_attack.append(enemy)

        to_attack_2 = select_enemy(to_attack)

        result = to_attack_2.get_hit(creature.a)
        #print(result)
        if result:
            enemies = del_by_id(to_attack_2.id, enemies)
            area[to_attack_2.pos[1]][to_attack_2.pos[0]] = '.'

        #print_field(area, [creature.pos[::-1], to_attack_2.pos[::-1]])
        #print("Attacking immediately:", print_players(to_attack_2, 1))
    else:
        #if debug:
        if (x_cr, y_cr) == monitor:
           print_field(area, [creature.pos[::-1]])
        targets = []
        binary_area = get_walled(area)
        for cr in enemies:
            if cr.alive is False:
                continue
            char = cr.t
            x, y = cr.pos
            if char == target_creature:
                for x_d, y_d in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    if area[y + y_d][x + x_d] == "." and (x + x_d, y + y_d) != creature.pos:
                        targets.append((x + x_d, y + y_d))
            if char == creature.t and cr.id != creature.id:
                binary_area[y][x] = 1
            if cr.id == creature.id:
                binary_area[y][x] = 0
                area[y][x] = "."


        access = []
        length = [10000]
        #print("own pos:", creature.pos)
        #print_field(binary_area)
        if (x_cr, y_cr) == monitor: print(targets)
        for target in targets:
            #if debug: print("aiming for:", target, "from", creature.pos)
            distance = astar(binary_area, creature.pos, target, True, area, get_walled(area))
            if distance is not None:
                if len(distance) > min(length) + 1 or len(distance) < 2:
                    if (x_cr, y_cr) == monitor: print("too long", len(distance))
                    #if (x_cr, y_cr) == monitor: print_field(area, distance)
                    continue
                if (x_cr, y_cr) == monitor: print("aiming for:", target, "dist", len(distance), "path", distance)
                if (x_cr, y_cr) == monitor: print_field(area, distance)
                length.append(len(distance)-1)
                access.append((target, len(distance)-1, distance[1][::-1]))
            else:
                #print("No Path", target)
                pass
        #print(access)
        #print_field(binary_area)
        if len(access) == 0:
            new_x, new_y = creature.pos
            area[new_y][new_x] = creature.t
            #print_field(area)
            if debug: print("Did nothing due to no available accesible targets")
            return None

        length = min(length)
        closest = []
        target_print = 0
        for point in access:
            target_point, dist, next_move = point
            if dist == length:
                target_print = target_point
                closest.append((next_move, target_point))

        new_x, new_y = select_closest(closest)
        creature.move((new_x, new_y))
        area[new_y][new_x] = creature.t

        for x_d, y_d in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if area[new_y + y_d][new_x + x_d] == target_creature:
                creature.attacking = True

        if creature.attacking:
            to_attack = []
            for enemy in enemies:
                if enemy.t == target_creature:
                    enemy_x, enemy_y = enemy.pos
                    if abs(enemy_x-new_x) + abs(enemy_y - new_y) == 1:
                        to_attack.append(enemy)

            to_attack_2 = select_enemy(to_attack)
            result = to_attack_2.get_hit(creature.a)
            #print(result)
            if result:
                enemies = del_by_id(to_attack_2.id, enemies)
                area[to_attack_2.pos[1]][to_attack_2.pos[0]] = '.'

            #print_field(area, [creature.pos[::-1], to_attack_2.pos[::-1]])
            #print("Attacking after moving:", print_players(to_attack_2, 1))
        #print_field(area, [(new_x, new_y)[::-1], (x_cr, y_cr)[::-1]])
        #print("Moved to:", (new_x, new_y), "from", (x_cr, y_cr), "with target:", target_print)
        if (x_cr, y_cr) == monitor:
            print_field(area, [(new_x, new_y)[::-1], (x_cr, y_cr)[::-1]])
            print("yeet")
            exit()


def compute(file, printing = False, load_players = False, attack = 3):
    #printing = True
    field, players = initiate(file, attack)
    if load_players:
        players = load_pl()
        print_players(players)
    if printing: print_players(players)

    if printing: print("Round: 0")
    print_field(field)
    if printing: print()

    i = 0
    start_time = time()
    start_time_2 = time()
    while True:
        print("Round:", i)

        for player in players:
            if player.alive:
                act(field, player, players, printing)
            elif printing:
                print("Turn:", player.id, player.pos)
                print("But they are dead")
        print("Time for turn:", time() - start_time, time() - start_time_2)
        start_time = time()
        print_field(field)
        players = re_order(players, True)
        #print(len(players))
        if -1 == players[0]:
            #if printing is False: print_field(field)
            #print(i, players[1])
            #print(i*players[1])
            return i, players[1], i*players[1]
        else:
            print_players(players)
        #if i == 2:
        #    exit()
        i += 1

        if printing: print("_________________")



#unittest.main()
#print(compute('G:\\24daysofcode\\15_6.txt'))
#print(compute('G:\\24daysofcode\\15_special_2.txt', True))

print(compute('G:\\24daysofcode\\15_input', False, False, 25))
#print(compute('G:\\24daysofcode\\15_input_turn4.txt', False, True))

#print(compute('G:\\24daysofcode\\15_input_test.txt', False))
#print(compute('G:\\24daysofcode\\15_special.txt', False))

# Own script:
# Attempt 1: 91, 2676, 243516
# Attempt 2: 93, 2675, 248775
# Attempt 3: 92, 2677, 246284
# Attempt 4: 96, 2258, 216768
# Attempt 5: 97, 2025, 196425
# Attempt 6: 96, 2613, 250848
# Done
# Other's scripts:
# Answer 1: 95, 2613, 248235
# Answer 2: 95, 2613, 248235

# Part 2:
# Own script:
# Attempt 1:
# (34, 1376, 46784)
# Done
# Other's scripts:
# Answer 1: