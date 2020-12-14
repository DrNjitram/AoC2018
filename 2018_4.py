from codecs import open


def main():
    file = open("G:\\24daysofcode\\input4.txt", 'r')
    inputs = file.readlines()

    inputs = sorted(inputs)

    guards = {} #guard_id : [(sleep_start, sleep_end), ...]

    minute = 0
    start = 0
    end = 0
    guard_id = 0

    for records in inputs:
        minute = int(records.split(':')[1].split(']')[0])
        if 'Guard' in records:
            guard_id = int(records.split('#')[1].split(' ')[0])
        elif 'falls' in records:
            start = minute
        else:
            end = minute
            entry = guards.get(guard_id, None)
            if entry is None:
                guards[guard_id] = [(start, end)]
            else:
                entry.append((start, end))
                guards[guard_id] = entry
                entry = []

    guard_sleepy = {}

    for guard in guards:
        sleepy = guards[guard]
        guard_sleepy[guard] = 0
        for sleep in sleepy:
            a, b = sleep
            guard_sleepy[guard] += b-a

        print(guard, guard_sleepy[guard])


    sleep = max(guard_sleepy.values())
    max_guard = 0

    for guard in guards:
        if sleep == guard_sleepy[guard]:
            max_guard = guard

    max_sleep = guards[max_guard]

    mins = [0 for i in range(60)]
    for i in range(0, 60):
        for sleeps in max_sleep:
            a, b = sleeps
            if a < i and i < b:
                mins[i] += 1

    print(max_sleep)



main()