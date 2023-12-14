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

def calculate_line_load(col: str):
    total_load = 0
    last_anchor_load = len(col)
    for idx, s in enumerate(col):
        if s == "O":
            total_load += last_anchor_load
            last_anchor_load -= 1
        elif s == "#":
            last_anchor_load = len(col) - idx - 1
    return total_load

def calculate_north_load(data: List[str]):
    columns = zip(*data)
    return sum(calculate_line_load(col) for col in columns)

def rotate_anticlock(data: List[str]):
    return list("".join(z) for z in zip(*data))[::-1]

if __name__ == "__main__":

    #input_data = aocutils.getDataInput(14)
    input_data = test_array

    #### Part 1 ####
    aocutils.printResult(1, calculate_north_load(input_data))

    d1 = rotate_anticlock(input_data)
    d2 = rotate_anticlock(d1)
    d3 = rotate_anticlock(d2)

    print("\n".join(d1))
    print("\n")
    print("\n".join(d2))
    print("\n")
    print("\n".join(d3))

