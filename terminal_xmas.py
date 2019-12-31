import os
import random
import threading
import time

BULB_CHAR = '\N{BLACK STAR}'

mutex = threading.Lock()

with open('house.txt') as f:
    ascii_house = f.read().partition('#')[0]
    house = list(ascii_house.rstrip())


def colored_bulb(color):
    color_code = {'yellow': 3, 'red': 1, 'green': 2, 'blue': 4,
                  'dark': 0}[color]
    return f'\033[9{color_code}m{BULB_CHAR}\033[0m'


def lights(color, indexes):
    off = True

    while True:
        for i in indexes:
            house[i] = colored_bulb(color) if off else colored_bulb('dark')

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

thread_yellow = threading.Thread(target=lights, args=('yellow', yellow))
thread_red = threading.Thread(target=lights, args=('red', red))
thread_green = threading.Thread(target=lights, args=('green', green))
thread_blue = threading.Thread(target=lights, args=('blue', blue))

for thread in [thread_yellow, thread_red, thread_green, thread_blue]:
    thread.start()
for thread in [thread_yellow, thread_red, thread_green, thread_blue]:
    thread.join()
