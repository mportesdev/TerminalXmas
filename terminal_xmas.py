import os
import random
import threading
import time

BULB_CHAR = '\N{BLACK STAR}'

mutex = threading.Lock()

with open('house.txt') as f:
    ascii_house = f.read().partition('#')[0]
    house = list(ascii_house.rstrip())


def colored_dot(color):
    if color == 'yellow':
        return f'\033[93m{BULB_CHAR}\033[0m'
    if color == 'red':
        return f'\033[91m{BULB_CHAR}\033[0m'
    if color == 'green':
        return f'\033[92m{BULB_CHAR}\033[0m'
    if color == 'blue':
        return f'\033[94m{BULB_CHAR}\033[0m'
    if color == 'dark':
        return f'\033[90m{BULB_CHAR}\033[0m'


def lights(color, indexes):
    off = True

    while True:
        for i in indexes:
            house[i] = colored_dot(color) if off else colored_dot('dark')

        mutex.acquire()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(''.join(house))
        mutex.release()

        off = not off

        time.sleep(random.uniform(0.3, 0.6))


yellow = []
red = []
green = []
blue = []

for i, char in enumerate(house):
    if char == 'Y':
        yellow.append(i)
        house[i] = BULB_CHAR
    elif char == 'R':
        red.append(i)
        house[i] = BULB_CHAR
    elif char == 'G':
        green.append(i)
        house[i] = BULB_CHAR
    elif char == 'B':
        blue.append(i)
        house[i] = BULB_CHAR

ty = threading.Thread(target=lights, args=('yellow', yellow))
tr = threading.Thread(target=lights, args=('red', red))
tg = threading.Thread(target=lights, args=('green', green))
tb = threading.Thread(target=lights, args=('blue', blue))

for t in [ty, tr, tg, tb]:
    t.start()
for t in [ty, tr, tg, tb]:
    t.join()
