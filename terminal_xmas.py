import os
import random
import threading
import time

BULB_CHAR = '\N{BLACK STAR}'

mutex = threading.Lock()

with open('house.txt') as f:
    ascii_house = f.read().partition('#')[0]
    house = list(ascii_house.rstrip())


def get_bulb(color):
    color_code = {'yellow': 3, 'red': 1, 'green': 2, 'blue': 4,
                  'dark': 0}[color]
    return f'\033[9{color_code}m{BULB_CHAR}\033[0m'


def switch_lights(color, index_list):
    lights_off = True

    while True:
        for index in index_list:
            house[index] = get_bulb(color) if lights_off else get_bulb('dark')

        mutex.acquire()
        os.system('cls' if os.name == 'nt' else 'clear')
        print(''.join(house))
        mutex.release()

        lights_off = not lights_off

        time.sleep(random.uniform(0.3, 0.6))


yellow = []
red = []
green = []
blue = []

index_lists = {'Y': yellow, 'R': red, 'G': green, 'B': blue}

for i, char in enumerate(house):
    if char in ('Y', 'R', 'G', 'B'):
        index_lists[char].append(i)
        house[i] = BULB_CHAR

threads = [threading.Thread(target=switch_lights, args=('yellow', yellow)),
           threading.Thread(target=switch_lights, args=('red', red)),
           threading.Thread(target=switch_lights, args=('green', green)),
           threading.Thread(target=switch_lights, args=('blue', blue))]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
