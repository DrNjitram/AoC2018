from codecs import open

def main1():

    instructions = [('P', 'O'), ('H', 'X'), ('M', 'Q'), ('E', 'U'), ('G', 'O'), ('W', 'F'), ('O', 'F'), ('B', 'X'), ('F', 'C'), ('A', 'L'), ('C', 'D'), ('D', 'Y'), ('V', 'R'), ('I', 'Y'), ('X', 'K'), ('T', 'S'), ('Y', 'J'), ('Z', 'R'), ('R', 'K'), ('K', 'N'), ('U', 'N'), ('Q', 'N'), ('N', 'J'), ('S', 'J'), ('L', 'J'), ('A', 'C'), ('S', 'L'), ('X', 'S'), ('T', 'J'), ('B', 'C'), ('G', 'N'), ('M', 'O'), ('Y', 'K'), ('B', 'Y'), ('Y', 'U'), ('F', 'J'), ('A', 'N'), ('W', 'Y'), ('C', 'R'), ('Q', 'J'), ('O', 'L'), ('Q', 'S'), ('H', 'E'), ('N', 'S'), ('A', 'T'), ('C', 'K'), ('Z', 'J'), ('U', 'Q'), ('B', 'F'), ('W', 'X'), ('H', 'Q'), ('B', 'V'), ('Z', 'U'), ('O', 'A'), ('C', 'I'), ('I', 'T'), ('E', 'D'), ('V', 'S'), ('F', 'V'), ('C', 'S'), ('I', 'U'), ('F', 'Z'), ('A', 'X'), ('C', 'N'), ('G', 'F'), ('O', 'R'), ('V', 'X'), ('E', 'A'), ('K', 'Q'), ('Z', 'K'), ('T', 'K'), ('Y', 'Z'), ('W', 'B'), ('E', 'V'), ('W', 'J'), ('I', 'S'), ('H', 'L'), ('G', 'I'), ('X', 'L'), ('H', 'G'), ('H', 'Z'), ('H', 'N'), ('D', 'I'), ('E', 'J'), ('X', 'R'), ('O', 'J'), ('N', 'L'), ('X', 'N'), ('V', 'Q'), ('P', 'Y'), ('H', 'U'), ('X', 'Z'), ('G', 'Q'), ('B', 'Q'), ('Y', 'L'), ('U', 'J'), ('W', 'V'), ('G', 'C'), ('G', 'B'), ('O', 'B'), ('R', 'N')]

    points = []
    graph = {}
    to_add = set()
    for instruction in instructions:
        requirment, target = instruction

        if graph.get(target, None) == None:
            graph[target] = requirment
        else:
            graph[target] += (requirment)

        if requirment not in points or target not in points:
            points.append(requirment)

    for p in points:
        if p not in graph.keys():
            to_add.add(p)

    for points in graph:
        graph[points] = list(graph[points])

    to_add = sorted(to_add)
    last_letter = to_add.pop(0)
    answer = last_letter

    while len(graph) > 0:
        to_remove = []
        for points in graph:
            reqs = graph[points]
            if last_letter in reqs:
                reqs.remove(last_letter)
                if len(reqs) == 0:
                    to_add.append(points)
                    to_remove.append(points)
                else:
                    graph[points] = reqs
        for removal in to_remove:
            del graph[removal]
        to_add = sorted(to_add)
        last_letter = to_add.pop(0)
        answer += last_letter


    print(answer)

def main2():

    instructions = [('P', 'O'), ('H', 'X'), ('M', 'Q'), ('E', 'U'), ('G', 'O'), ('W', 'F'), ('O', 'F'), ('B', 'X'), ('F', 'C'), ('A', 'L'), ('C', 'D'), ('D', 'Y'), ('V', 'R'), ('I', 'Y'), ('X', 'K'), ('T', 'S'), ('Y', 'J'), ('Z', 'R'), ('R', 'K'), ('K', 'N'), ('U', 'N'), ('Q', 'N'), ('N', 'J'), ('S', 'J'), ('L', 'J'), ('A', 'C'), ('S', 'L'), ('X', 'S'), ('T', 'J'), ('B', 'C'), ('G', 'N'), ('M', 'O'), ('Y', 'K'), ('B', 'Y'), ('Y', 'U'), ('F', 'J'), ('A', 'N'), ('W', 'Y'), ('C', 'R'), ('Q', 'J'), ('O', 'L'), ('Q', 'S'), ('H', 'E'), ('N', 'S'), ('A', 'T'), ('C', 'K'), ('Z', 'J'), ('U', 'Q'), ('B', 'F'), ('W', 'X'), ('H', 'Q'), ('B', 'V'), ('Z', 'U'), ('O', 'A'), ('C', 'I'), ('I', 'T'), ('E', 'D'), ('V', 'S'), ('F', 'V'), ('C', 'S'), ('I', 'U'), ('F', 'Z'), ('A', 'X'), ('C', 'N'), ('G', 'F'), ('O', 'R'), ('V', 'X'), ('E', 'A'), ('K', 'Q'), ('Z', 'K'), ('T', 'K'), ('Y', 'Z'), ('W', 'B'), ('E', 'V'), ('W', 'J'), ('I', 'S'), ('H', 'L'), ('G', 'I'), ('X', 'L'), ('H', 'G'), ('H', 'Z'), ('H', 'N'), ('D', 'I'), ('E', 'J'), ('X', 'R'), ('O', 'J'), ('N', 'L'), ('X', 'N'), ('V', 'Q'), ('P', 'Y'), ('H', 'U'), ('X', 'Z'), ('G', 'Q'), ('B', 'Q'), ('Y', 'L'), ('U', 'J'), ('W', 'V'), ('G', 'C'), ('G', 'B'), ('O', 'B'), ('R', 'N')]

    points = []
    graph = {}
    to_add = set()
    for instruction in instructions:
        requirment, target = instruction

        if graph.get(target, None) == None:
            graph[target] = requirment
        else:
            graph[target] += requirment

        if requirment not in points or target not in points:
            points.append(requirment)

    for p in points:
        if p not in graph.keys():
            to_add.add(p)

    for point in graph:
        graph[point] = list(graph[point])

    to_add = sorted(to_add)

    no_workers = 5
    workers = {}  # worker = (letter, time remaining)
    for i in range(no_workers):
        workers[i] = ('0', 0)

    for worker in workers:
        if len(to_add) < 1:
            break
        letter = to_add.pop(0)
        workers[worker] = (letter, 61 + ord(letter) - ord('A'))

    second = 0

    answer = ''
    while len(graph) > 0:

        # Advance all workers and collect done points
        done = []
        for worker in workers:
            letter, left = workers[worker]
            if left == 1:
                done.append(letter)
                letter = '0'

            workers[worker] = (letter, left - 1)

        # Remove all done letters from the points
        to_remove = []
        for points in graph:
            reqs = graph[points]
            for last_letter in done:
                if last_letter in reqs:
                    reqs.remove(last_letter)
                    if len(reqs) == 0:
                        to_add.append(points)
                        to_remove.append(points)
                    else:
                        graph[points] = reqs
        for removal in to_remove:
            del graph[removal]
        answer += "".join(done)

        # If workers are free, give them letters to do
        to_add = sorted(to_add)
        for worker in workers:
            if len(to_add) < 1:
                break
            letter, time = workers[worker]
            if letter == '0':
                letter = to_add.pop(0)
                workers[worker] = (letter, 61 + ord(letter) - ord('A'))

        # Advance time
        second += 1

    for worker in workers:
        letter, time = workers[worker]
        if letter != '0':
            second += time

    print(second)

#main1()
main2()