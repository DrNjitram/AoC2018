from codecs import open


def checkio(data):
    return [i for i in data if data.count(i)>1]

def compare(word1, word2):
    differ = 0
    list_w1 = list(word1)
    list_w2 = list(word2)
    for i in range(0, len(word1)):
        if list_w1[i] != list_w2[i]:
            differ += 1
    return differ


def main1():
    file = open("G:\\24daysofcode\\input2.txt", 'r')
    inputs = file.readlines()



    doubles = 0
    triples = 0



    for word in inputs:
        word = word.strip()
        duplicates = checkio(word)
        uniques = list(set(duplicates))

        add_d = 0
        add_t = 0
        for letter in uniques:
            if duplicates.count(letter) == 2:
                add_d = 1
            else:
                add_t = 1

        doubles += add_d
        triples += add_t

    print(doubles*triples)


def main2():
    file = open("G:\\24daysofcode\\input2.txt", 'r')
    inputs = file.readlines()
    compares = set()
    for word in inputs:
        word = word.strip()

        for word2 in inputs:
            word2 = word2.strip()
            if word == word2:
                pass
            if compare(word, word2) == 1:
                print(word)
                print(word2)
                exit()




main1()
main2()