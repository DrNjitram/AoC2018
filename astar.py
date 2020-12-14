class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


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


def get_walled(area):
    return [[{"#": 1, "G": 1, "E": 1, ".": 0, "?": 0}[k] for k in i] for i in area]


def select_closest(distances, debug = False):
    if debug: print(distances)
    low_y = min([d[1][0] for d in distances])
    remaining = []
    for path in distances:
        y, x = path[1]
        if y == low_y:
            remaining.append(path)

    if len(remaining) == 1:
        return remaining[0][0]
    else:
        low_x = min([d[1][1] for d in remaining])
        for path in distances:
            y, x = path[1]
            if x == low_x:
                return path[0]


def get_pos(lst):
    return [node.position for node in lst]


def re_order(creatures):
    new_order = []
    positions = []

    for cr in creatures:
        positions.append((cr.position, cr.position))


    while len(positions) > 0:
        first = select_closest(positions)
        for cr in creatures:
            if first == cr.position:
                new_order.append(cr)
        positions.remove((first, first))

    return new_order


def check_for_holes(walk, field):
    """"Try to detect the pattern XX/.X/XX or rotations of it"""
    print(walk)
    min_x = 100
    max_x = -1
    min_y = 100
    max_y = -1
    for point in walk:
        y, x = point
        min_x = x if x < min_x else min_x
        max_x = x if y > max_x else max_x
        min_y = y if y < min_y else min_y
        max_y = y if y > max_y else max_y

    min_y -= 1
    for i in range(len(walk)):
        y, x = walk[i]
        walk[i] = (y - min_y -1, x - min_x)


    print(min_x, max_x, min_y, max_y)
    sub_field = []
    for i, line in enumerate(field):
        if min_y < i < max_y + 1:
            sub_field.append(line[min_x:max_x+1])

    print_field(sub_field, walk)
    # Pattern if:
    # X-
    # .X
    # X-

    exit()



def astar(maze, start, end, repeat = True, second = None, ori_maze = None):
    #print("----------------------")
    #print_field(maze)
    start = start[::-1]
    end = end[::-1]

    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    st_y, st_x = start
    en_y, en_x = end
    if (abs(st_x-en_x) + abs(st_y - en_y)) == 1:
        return [start, end]

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        cur_y, cur_x = current_node.position
        current_index = 0

        #print("---------------------------------------")
        #print("Parent:", current_node.position, current_node.f)
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                #print("Usurped:", current_node.position, current_node.f)
                current_index = index

        #print("Selected:", current_node.position)
        #print_field(second, [current_node.position[::-1]])
        #print("open", len(open_list))
        #print("closed", len(closed_list))
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            #print("Found it")
            path = []
            current = current_node

            while current is not None:
                path.append(current.position)
                current = current.parent
            path = path[::-1]
            first_node = path[0]
            second_node = path[1]
            #print_field(second, path)
            #path = check_for_holes(path, second)
            if repeat:
                to_compare = [(path[1], path[1])]
                to_compare_path = [path]
                for new_position in [(-1, 0), (0, -1), (0, 1), (1, 0)]:  # Adjacent squares
                    # Get node position
                    if maze[first_node[0] + new_position[0]][first_node[1] + new_position[1]] == 0:

                        for offset in ({(-1, 0), (0, -1), (0, 1), (1, 0)} - {new_position}):
                            x, y = first_node[0] + offset[0], first_node[1] + offset[1]
                            #print("setting", x, y, "to 1", new_position)
                            maze[x][y] = 1
                            #second[x][y] = '#'

                        second_path = astar(maze, start[::-1], end[::-1], False, second)

                        #if second_path is not None: print(len(second_path))
                        #print_field(second, second_path)

                        for offset in ({(-1, 0), (0, -1), (0, 1), (1, 0)} - {new_position}):
                            x, y = first_node[0] + offset[0], first_node[1] + offset[1]
                            maze[x][y] = ori_maze[x][y]
                            #second[x][y] = '.'

                        if second_path is not None and len(second_path) < len(path) + 1:
                            #print("found other viable path", second_path[1])
                            to_compare.append((second_path[1], second_path[1]))
                            to_compare_path.append(second_path)
                #print(to_compare)
                comparisons = select_closest(to_compare, False)
                #print(comparisons)
                for pt in to_compare_path:
                    if comparisons in pt:
                        #print("Found priority path", comparisons)
                        return pt

            #return check_for_holes(path, second)  # Return reversed path
            return path  # Return reversed path

        # Generate children
        children = []

        for new_position in [(-1, 0), (0, -1), (0, 1), (1, 0)]:  # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node

            new_node = Node(current_node, node_position)
            #print("child:", node_position)
            # Append
            children.append(new_node)

        #Order kids
        children = re_order(children)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child.position in get_pos(closed_list):
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            #child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.h = 0
            child.f = child.g + child.h

            if child.position in get_pos(open_list):
                continue

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

        #if len(open_list) > 100:
        #    return None


def main():

    from codecs import open
    from time import time
    maze = open('G:\\24daysofcode\\15_input_turn4.txt')
    maze = maze.read()
    maze = maze.split("\n")
    maze = [list(_) for _ in maze]

    ori = open('G:\\24daysofcode\\15_input_turn4.txt')
    ori = ori.read()
    ori = ori.split("\n")
    ori = [list(_) for _ in maze]
    maze = get_walled(maze)
    print()
    start = (6, 18)
    end = (12, 21)
    print_field(ori, [start[::-1], end[::-1]])

    start_time = time()
    path = astar(maze, start, end, True, ori, get_walled(ori))
    print("----------------------------")
    print(time()-start_time )
    print("from", start, "to", end)

    print_field(ori, path)
    print(path)
    print(len(path))
    #print(path[1])


#main()
