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

    cube.set_leds(colours)

def bound(low, high, x):
    return max(low, min(high, x))

def new_temperature(cell, lower_cells):
    [below_left_cell, below_cell, below_right_cell] = lower_cells
    self_contribution = cell * random.gauss(0.85, 0.05)
    upward_contribution = below_cell * random.gauss(0.08, 0.02)
    wind_velocity = random.gauss(0, 0.02) + 0.03 # bias a bit rightwards
    wind_source = below_right_cell if wind_velocity < 0 else below_left_cell
    wind_contribution = wind_source * abs(wind_velocity)
    raw_temp = self_contribution + upward_contribution + wind_contribution
    return bound(raw_temp, 0, 1)

def update_step(temps):
    for j in range(ROW_COUNT):
        for i in range(COL_COUNT):
            current_cell = temps[(i,j)]
            # If we're at the bottom row, our 'below row' is the 'heat source' fake-row
            lower_cells = [
                temps[(i-1,j-1)],
                temps[(i,j-1)],
                temps[(i+1,j-1)]
            ] if j > 0 else [1,1,1]
            temps[(i,j)] = new_temperature(current_cell, lower_cells)

def run():
    # initialize temperatures as a 2d grid of floats 0-1
    # include boundary columns either side of the visible ones
    temps = {}
    for j in range(ROW_COUNT):
        for i in range(-1, COL_COUNT + 1):
            temps[(i,j)] = 0

    # initialize to black
    cube.set_all(0)

    while True:
        set_leds(temps)
        update_step(temps)


run()
