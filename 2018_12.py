import time

lines = open('G:\\24daysofcode\\input12.txt').read().split('\n')

start_time = time.time()
state = lines[0].split(': ')[1].strip()
start_len = len(state)
rules = {}
for line in lines[2:]:
    if line:
        before, after = line.split('=>')
        rules[before.strip()] = after.strip()


def score(state, zero):
    ans = 0
    for i in range(len(state)):
        if state[i] == '#':
            ans += i - zero
    return ans


zero_idx = 0
amount = 200
prev_score = 0

for t in range(amount):
    state = '..'+state+'..'
    new_state = ['.' for _ in range(len(state))]
    read_state = '..'+state+'..'
    zero_idx += 2
    for i in range(len(state)):
        pat = read_state[i:i+5]
        new_state[i] = rules.get(pat, '.')

    start = 0
    end = len(new_state)-1
    while new_state[start] == '.':
        start += 1
        zero_idx -= 1
    while new_state[end] == '.':
        end -= 1
    state = ''.join(new_state[start:end+1])
    now_score = score(state, zero_idx)
    delta = now_score - prev_score
    #print(t+1, zero_idx, now_score,delta , state)
    prev_score = now_score

print(score(state, zero_idx) + ((50000000000 - t + 1)* delta ))
print(time.time()-start_time)