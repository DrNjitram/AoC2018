import networkx

def print_field(area):
    for line in area:
        line = [{0: ".", 1: "=", 2: "|"}[char%3] for char in line]
        print("".join(line))


def create_field(depth, target, padding = 0):
    x, y = target

    field = [[0 for _ in range(x + 1 + padding)] for _ in range(y + 1 + padding)]

    for i in range(y+1 + padding):
        for j in range(x+1 + padding):
            if y == i and x == j:
                geo_index = (0 + depth) % 20183
            elif i == 0:
                if j == 0:
                    geo_index = (0 + depth) % 20183
                else:
                    geo_index = ((j * 16807) + depth) % 20183
            elif j == 0:
                geo_index = ((i * 48271) + depth) % 20183
            else:
                geo_index = ((field[i][j-1] * field[i-1][j]) + depth) % 20183

            field[i][j] = geo_index

    return field


def neighbours(x, y):
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

# get a set of allowed tools for a given erosion level
# 0 = nothing, 1 = climbing gear, 2 = torch


def allowed_tools(erosion_level):
    erosion_level = erosion_level % 3
    if erosion_level == 0:
        return {1, 2}
    if erosion_level == 1:
        return {0, 1}
    if erosion_level == 2:
        return {0, 2}


def solve(grid, target):
    tx, ty = target

    # create a graph and add edges for switching tools
    network = networkx.DiGraph()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            allowed = allowed_tools(grid[y][x])
            for t1 in allowed:
                for t2 in allowed:
                    if t1 == t2:
                        continue
                    network.add_edge((x, y, t1), (x, y, t2), weight=7)

    # add edges for travelling between squares
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            for nx, ny in neighbours(x, y):
                if nx < 0 or nx >= len(grid[0]):
                    continue
                if ny < 0 or ny >= len(grid):
                    continue
                from_erosion = grid[y][x]
                to_erosion = grid[ny][nx]

                # get tools that can be used when travelling between these cells
                tools = allowed_tools(from_erosion).intersection(allowed_tools(to_erosion))

                for tool in tools:
                    network.add_edge((x, y, tool), (nx, ny, tool), weight=1)

    total = 0
    for y in range(ty + 1):
        for x in range(tx + 1):
            total += grid[y][x] % 3
    print("Part 1", total)

    shortest_path_length = networkx.dijkstra_path_length(network, (0, 0, 2), (tx, ty, 2))
    print("Part 2", shortest_path_length)


depth = 3339
target = (10, 715)

field = create_field(depth, target, 15)
print_field(field)

solve(field, target)