import aocutils
import re
from typing import List, Tuple, Dict
from enum import Enum

test_array = [
    "R 6 (#70c710)",
    "D 5 (#0dc571)",
    "L 2 (#5713f0)",
    "D 2 (#d2c081)",
    "R 2 (#59c680)",
    "D 2 (#411b91)",
    "L 5 (#8ceee2)",
    "U 2 (#caa173)",
    "L 1 (#1b58a2)",
    "U 2 (#caa171)",
    "R 2 (#7807d2)",
    "U 3 (#a77fa3)",
    "L 2 (#015232)",
    "U 2 (#7a21e3)",
]

class Direction(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

direction_map_1 = {
    "D": Direction.DOWN,
    "U": Direction.UP,
    "L": Direction.LEFT,
    "R": Direction.RIGHT,
}

direction_map_2 = {
    "0": Direction.RIGHT,
    "1": Direction.DOWN,
    "2": Direction.LEFT,
    "3": Direction.UP,
}

def parse_data_1(input: str):
    rgex = re.compile('([UDLR]) ([0-9]*) \(#[0-9a-f]{6}\)')
    return [(direction_map_1[m.group(1)], int(m.group(2))) for m in  [rgex.match(line) for line in input]]

def parse_data_2(input: str):
    rgex = re.compile('[UDLR] [0-9]* \(#([0-9a-f]{5})([0-3])\)')
    return [(direction_map_2[m.group(2)], int(m.group(1), 16)) for m in  [rgex.match(line) for line in input]]

def count_area(instructions: List[Tuple[Direction, int, str]]):
    # Adaptation of the formula to calculate area of a N-size irregular polygon
    area = 0
    x, y = 0, 0

    prev_horizontal = None
    prev_vertical = None
    prev_y = 0

    # In order to complete the cycle, we first need to go back and look at the last two iterations of the loop
    prev_direction_1, prev_length_1 = instructions[-1]
    prev_direction_2, prev_length_2 = instructions[-2]
    if prev_direction_1 == Direction.RIGHT or prev_direction_1 == Direction.LEFT:
        prev_horizontal = prev_direction_1
    else:
        prev_vertical = prev_direction_1
        prev_y = y - prev_length_1
    if prev_direction_2 == Direction.RIGHT or prev_direction_2 == Direction.LEFT:
        prev_horizontal = prev_direction_2
    else:
        prev_vertical = prev_direction_2
        prev_y = y - prev_length_2

    # Confirm that we found both vertical and horizonal previous directions
    assert prev_horizontal is not None
    assert prev_vertical is not None

    for direction, lenght in instructions:
        if direction == Direction.RIGHT:
            area += y * (lenght - 1)
            if prev_horizontal == Direction.RIGHT:
                area += max(prev_y, y)
            elif prev_y < y:
                area += y
                area -= (prev_y - 1)
            prev_horizontal = direction
            x += lenght
        elif direction == Direction.LEFT:
            area -= (y - 1) * (lenght - 1)
            if prev_horizontal == Direction.LEFT: 
                area -= min(prev_y - 1, y - 1)
            elif prev_y > y:
                area += prev_y
                area -= (y - 1)
            prev_horizontal = direction
            x -= lenght
        elif direction == Direction.UP:
            prev_y = y
            y += lenght
        elif direction == Direction.DOWN:
            prev_y = y
            y -= lenght
        else:
            raise RuntimeError()
    return area

if __name__ == "__main__":

    input_data = aocutils.getDataInput(18)
    #input_data = test_array

    #### Part 1 ####

    aocutils.printResult(1, count_area(parse_data_1(input_data)))

    #### Part 2 ####

    aocutils.printResult(1, count_area(parse_data_2(input_data)))
