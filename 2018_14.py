

def check_pos(index, all_recipes):
    if index + all_recipes[index] + 1 > len(all_recipes):
        new_index = index + all_recipes[index] + 1 - len(all_recipes)
        if new_index > len(all_recipes):
            new_index = (index + all_recipes[index] + 1) % len(all_recipes)
    else:
        new_index = (index + all_recipes[index] + 1) % len(all_recipes)
    return new_index



def get_answer(start, uno, duos, exit):
    for _ in range(exit + 10):
        result = str(start[uno] + start[duos])
        start.extend(map(int, result))
        uno += start[uno] + 1
        duos += start[duos] + 1
        uno %= len(start)
        duos %= len(start)

    print(*start[exit:exit + 10], sep="")


def get_answer2(start, uno, duos, inp):

    while True:
        result = str(start[uno] + start[duos])
        start.extend(map(int, result))
        uno += start[uno] + 1
        duos += start[duos] + 1
        uno %= len(start)
        duos %= len(start)

        if start[-len(inp):] == inp or start[-len(inp)-1:-1] == inp:
            break

    if start[-len(inp):] == inp:
        print(len(start) - len(inp))
    else:
        print(len(start) - len(inp) - 1)


recipes = [3, 7]
answer = "077201"


print(get_answer(recipes, 0, 1, 2018))

print(get_answer2(recipes, 0, 1, answer))
