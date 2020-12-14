from collections import deque, defaultdict
import time

def play_game(max_players, last_marble):
    start_time = time.time()

    player_scores = defaultdict(int)
    marbles = deque([0])
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            marbles.rotate(7)
            player_scores[marble % max_players] += marble + marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(marble)
    print(time.time() - start_time)
    return max(player_scores.values()) if player_scores else 0


def slow(players, last_marble):
    start_time = time.time()

    marbles = [0, 2, 1]
    current_marble_index = 1
    current_player = 2
    player_scores = [0 for i in range(players)]
    for marble in range(3, last_marble + 1):
        current_player = current_player % players + 1
        new_index = (current_marble_index + 2) % len(marbles)
        if marble % 23 != 0:
            if new_index == 0:
                marbles.append(marble)
                current_marble_index = len(marbles) - 1
            else:
                marbles.insert(new_index, marble)
                current_marble_index = new_index
        else:
            player_scores[current_player-1] += marble + marbles.pop(new_index - 9)
            if new_index - 9 < 0:
                new_index += 1
            current_marble_index = new_index - 9

    print(time.time() - start_time)
    print(max(player_scores))

players = 418
last_marble = 71339 * 100

print(play_game(players, last_marble))
#slow(players, last_marble)