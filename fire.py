import random
import time

# treat the two vertical grids as a single 16x8 screen that wraps around. ignore the top one.
COL_COUNT = 16
ROW_COUNT = 8

def colour_from_temperature(temperature):
    red = 0 if temperature < 0.1 else min((temperature - 0.1) * 2, 1)
    green = 0 if temperature < 0.3 else min((temperature - 0.3) * 2, 1)
    blue = 0 if temperature < 0.9 else min((temperature - 0.9) * 2, 1)
    return (int(red * 0xff) << 16) + (int(green * 0xff) << 8) + int(blue * 0xff)

def set_leds(temps):
    colours = {}
    for j in range(ROW_COUNT):
        for i in range(COL_COUNT):
            temperature = temps[(i,j)]
            colours[(i,j)] = colour_from_temperature(temperature)
            # print(colour_from_temperature(temperature))

    # print(temps)
    # print(colours)
    cube.set_leds(colours)

def bound(low, high, x):
    return max(low, min(high, x))

def new_temperature(cell, below_cell):
    cooling_decay = random.gauss(0.8, 0.1)
    conduction = random.gauss(0.15, 0.1)
    raw_temp = (cell * cooling_decay) + (below_cell * conduction)
    return bound(raw_temp, 0, 1)

def update_step(temps):
    for j in range(ROW_COUNT):
        # If we're at the bottom row, our 'below row' is the 'heat source' fake-row
        for i in range(COL_COUNT):
            current_cell = temps[(i,j)]
            below_cell = temps[(i,j-1)] if j > 0 else 1
            temps[(i,j)] = new_temperature(current_cell, below_cell)

def run():
    # initialize temperatures as a 2d grid of floats 0-1
    temps = {}
    for j in range(ROW_COUNT):
        for i in range(COL_COUNT):
            temps[(i,j)] = 0

    # initialize to black
    cube.set_all(0)

    while True:
        set_leds(temps)
        update_step(temps)
        # time.sleep(0.05)


run()
