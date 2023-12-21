import aocutils
import collections
from typing import List, Tuple, Optional

test_array = [
    "...........",
    ".....###.#.",
    ".###.##..#.",
    "..#.#...#..",
    "....#.#....",
    ".##..S####.",
    ".##..#...#.",
    ".......##..",
    ".##.#.####.",
    ".##..##.##.",
    "...........",
]

coord_offsets = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
]

def find_starting_coords(input: List[str]):
    for y, row in enumerate(input):
        for x, val in enumerate(row):
            if val == "S":
                return (x, y)
            
def find_dimensions(input: List[str]):
    size_x = len(input[0])
    size_y = len(input)
    return size_x, size_y

def calculate_reachable_plots(input: List[str], starting_coords_list: List[Tuple[int, int]], starting_step: int=0, max_steps: Optional[int]=None):
    reach_count_odd = 0
    reach_count_even = 0

    if starting_step < 0:
        RuntimeError(f"Starting step is {starting_step}. It should be at least zero.")

    size_x, size_y = find_dimensions(input)

    visited_steps = [[-1 for _ in range(size_x)] for _ in range(size_y)]
    next_steps = collections.deque()

    for starting_coord in starting_coords_list:
        next_steps.append((starting_step, starting_coord))

    while len(next_steps) > 0:
        step_count, (x, y) = next_steps.popleft()
        if max_steps and step_count > max_steps:
            continue
        elif x < 0 or x >= size_x or y < 0 or y >= size_y:
            continue
        elif input[y][x] == "#":
            continue
        elif visited_steps[y][x] >= 0:
            continue
        else:
            visited_steps[y][x] = step_count
            if step_count % 2 == 0:
                reach_count_even += 1
            else:
                reach_count_odd += 1
            for off_x, off_y in coord_offsets:
                next_x = x + off_x
                next_y = y + off_y
                next_steps.append((step_count + 1, (next_x, next_y)))
        
    return visited_steps

def count_reached_plots(visited_steps: List[List[int]], steps: int):
    remaining = steps % 2
    count = 0
    for row in visited_steps:
        for val in row:
            if val % 2 == remaining and val <= steps:
                count += 1
    return count

if __name__ == "__main__":

    input_data = aocutils.getDataInput(21)
    #input_data = test_array

    #### Part 1 ####

    start_coords = find_starting_coords(input_data)
    visited_step_matrix = calculate_reachable_plots(input_data, [start_coords], max_steps=64)
    aocutils.printResult(1, count_reached_plots(visited_step_matrix, 64))

    #### Part 2 ####
