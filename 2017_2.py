from codecs import open

def main1():
    file = open("G:\\24daysofcode\\input2_2017.txt", 'r')
    text = file.readlines()

    total = 0
    for i in range(0, len(text)):
        text[i] = text[i].strip().split('\t')
        text[i] = [int(i) for i in text[i]]
        text[i] = sorted(text[i], key = int)[::-1]

    for lines in text:
        total += max(lines) - min(lines)

    print(total)

    total = 0
    for lines in text:
        print(lines, "aaaaaaaaaaaaaaaa")
        for item in lines:
            print(item, "aaaaa")
            for item2 in lines:
                if item%item2 == 0 and item2 != item:
                    print(item, item2, item/item2)
                    total += item/item2

    print(total)


main1()
