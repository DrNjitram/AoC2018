from time import time
d = 0
s = set()
part1 = False
time_to_run = 0.5
start_time = time()
while True:
    e = d | 0x10000
    d = 7902108
    d = 8586263
    while True:
        c = e & 0xFF
        d += c
        d &= 0xFFFFFF
        d *= 65899
        d &= 0xFFFFFF
        if 256 > e:
            if part1:
                print(d)
                exit(0)
            else:
                if d not in s:
                    print(d)
                    if d == 2341:
                        print("----------------------------------")
                s.add(d)
                if time() - start_time > 1:  # or d == 13338900:
                    print(time() - start_time)
                    exit()
                break
        # the following code was the optimised part
        e = e // 256