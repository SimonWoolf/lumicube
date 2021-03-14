import random

# treat the two vertical grids as a single 16x8 screen that wraps around. ignore the top one.
COL_COUNT = 16
ROW_COUNT = 8

# Have a fake row below the bottom row that's always at temperature 1, as the heat source
HEAT_SOURCE = [1 for col in range(COL_COUNT)]

# array of colours, coldest to hottest; length doesn't matter, temperatures will scale to fit
COLOURS = [0x0, 0x880000, 0xff0000, 0xff8800, 0xffff00, 0xffff88]

def colour_from_temperature(temperature):
    return COLOURS[min(int(temperature * len(COLOURS)), len(COLOURS) - 1)]

def set_leds(rows):
    for j, row in enumerate(rows):
        for i, temperature in enumerate(row):
            # print(i, j, temperature)
            cube.set_led(i, j, colour_from_temperature(temperature))

def bound(low, high, x):
    return max(low, min(high, x))

def new_temperature(cell, below_cell):
    cooling_decay = random.gauss(0.2, 0.1)
    conduction = random.gauss(0.6, 0.1)
    raw_temp = (cell * cooling_decay) + (below_cell * conduction)
    return bound(raw_temp, 0, 1)

def update_step(rows):
    for j in range(ROW_COUNT):
        current_row = rows[j]
        # If we're at the bottom row, our 'below row' is the 'heat source' fake-row
        below_row = rows[j-1] if j > 0 else HEAT_SOURCE
        for i in range(COL_COUNT):
            cell_below = below_row[i]
            current_row[i] = new_temperature(current_row[i], below_row[i])

def run():
    # initialize temperatures as a 2d grid of floats 0-1
    rows = [[0 for col in range(COL_COUNT)] for row in range(ROW_COUNT)]

    # initialize to black
    cube.set_all(0)

    while True:
        set_leds(rows)
        update_step(rows)


run()
