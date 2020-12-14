from collections import defaultdict

lines = open("G:\\24daysofcode\\input4.txt").read().split('\n')
lines.sort()


def parseTime(line):
    words = line.split()
    date, time = words[0][1:], words[1][:-1]
    return int(time.split(':')[1])


C = defaultdict(int)
CM = defaultdict(int)
guard = None
asleep = None
for line in lines:
    if line:
        time = parseTime(line)
        if 'begins shift' in line:
            guard = int(line.split()[3][1:])
            asleep = None
        elif 'falls asleep' in line:
            asleep = time
        elif 'wakes up' in line:
            for t in range(asleep, time):
                CM[(guard, t)] += 1
                C[guard] += 1


def argmax(d1, d):
    best_min = max(list(d1.values()))

    for guard in d1:
        if best_min == d1[guard]:
            max_guard = guard

    best = [0 for i in range(60)]

    for k, v in d.items():
        g, m = k
        if g == max_guard:
            best[m] = v
    return max_guard, best.index(max(best))


def argmax2(d):
    best = None
    for k, v in d.items():
        if best is None or v > d[best]:
            best = k
    return best


best_guard, best_min = argmax(C, CM)
print(best_guard, best_min)

print(best_guard * best_min)

best_guard, best_min = argmax2(CM)
print(best_guard, best_min)

print(best_guard * best_min)