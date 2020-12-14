from codecs import open

def main1():
    file = open("G:\\24daysofcode\\input1_2017.txt", 'r')
    text = file.read().strip()
    numbers = [int(i) for i in list(text)]

    total = 0
    #1 for part 1, int(len(numbers)/2) for part 2
    steps = int(len(numbers)/2)
    for i in range(0, len(numbers)):
        if numbers[i] == numbers[i-steps]:
            total += numbers[i]

    print(total)


main1()
