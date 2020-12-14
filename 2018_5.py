from codecs import open
import time


def get_collapsed_length2(string):
    pairs = ['Aa', 'Bb', 'Cc', 'Dd', 'Ee', 'Ff', 'Gg', 'Hh', 'Ii', 'Jj', 'Kk', 'Ll', 'Mm', 'Nn', 'Oo', 'Pp', 'Qq', 'Rr', 'Ss', 'Tt' ,'Uu', 'Vv', 'Ww', 'Xx', 'Yy', 'Zz']
    last_length = len(string)
    new_length = 0

    while new_length != last_length:
        last_length = new_length
        for element in pairs:
            string = string.replace(element, "").replace(element[::-1], "")
        new_length = len(string)

    return len(string)-1

def main():
    file = open("G:\\24daysofcode\\input5.txt", 'r')
    inputs = file.read()

    start_time = time.time()

    print("Part 1:")
    print(get_collapsed_length2(inputs))
    print("Time taken:", round(time.time() - start_time, 3), "seconds")

    start_time = time.time()
    lengths = []
    pairs = ['Aa', 'Bb', 'Cc', 'Dd', 'Ee', 'Ff', 'Gg', 'Hh', 'Ii', 'Jj', 'Kk', 'Ll', 'Mm', 'Nn', 'Oo', 'Pp', 'Qq', 'Rr', 'Ss', 'Tt', 'Uu', 'Vv', 'Ww', 'Xx', 'Yy', 'Zz']

    for letters in pairs:
        cleaned = inputs.replace(letters, "").replace(letters[::-1], "")
        collapsed = get_collapsed_length2(cleaned)
        lengths.append(collapsed)


    print("Part 2:")
    print(min(lengths))
    print("Time taken:", round(time.time() - start_time, 3), "seconds")




main()