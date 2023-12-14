import aocutils
from typing import List

test_array = [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#....",
]

def calculate_row_load_left(col: str):
    total_load = 0
    for idx, s in enumerate(col):
        if s == "O":
            total_load += len(col) - idx
    return total_load

def tilt_left(input: List[str]):
    return ["#".join(["".join(sorted(seg, reverse=True)) for seg in row.split("#")]) for row in input]

def calculate_load_left(input: List[str]):
    return sum(calculate_row_load_left(row) for row in input)

def rotate_anticlockwise(input: List[str]):
    return list("".join(z) for z in zip(*input))[::-1]

def rotate_clockwise(input: List[str]):
    return list("".join(z)[::-1] for z in zip(*input))

def perform_single_cycle(input: List[str]):
    dish = tilt_left(input) # Tilt north
    dish = tilt_left(rotate_clockwise(dish)) # Tilt west
    dish = tilt_left(rotate_clockwise(dish)) # Tilt south
    dish = tilt_left(rotate_clockwise(dish)) # Tilt east
    return rotate_clockwise(dish) # Go back to north orientation

def perform_n_cycles(input: List[str], cycles: int):

    # At some point a loop will be found
    # We need to find it to avoid running all N cycles
    dish = input
    previous_dishes = {}
    for i in range(cycles):
        tuple_dish = tuple(dish)
        if tuple_dish in previous_dishes:
            loop_start = previous_dishes[tuple_dish]
            loop_size = i - previous_dishes[tuple_dish]
            break
        previous_dishes[tuple_dish] = i
        dish = perform_single_cycle(dish)
    else:
        raise RuntimeError("Did not find loop")
    
    remaining_cycles = (cycles - loop_start) % loop_size
    for i in range(remaining_cycles):
        dish = perform_single_cycle(dish)
    return dish

if __name__ == "__main__":

    input_data = aocutils.getDataInput(14)
    #input_data = test_array

    #### Part 1 ####

    # Start by rotating 90 degrees anticlockwise, north becomes left
    rotated_dish = rotate_anticlockwise(input_data)
    tilted_dish = tilt_left(rotated_dish)
    aocutils.printResult(1, calculate_load_left(tilted_dish))

    #### Part 2 ####

    # Start by rotating 90 degrees anticlockwise, north becomes left
    rotated_dish = rotate_anticlockwise(input_data)
    cycled_dish = perform_n_cycles(rotated_dish, 1000000000)    
    aocutils.printResult(2, calculate_load_left(cycled_dish))

