import aocutils
import collections
from typing import List, Tuple
from enum import Enum

test_array = [
    ".|...\....",
    "|.-.\.....",
    ".....|-...",
    "........|.",
    "..........",
    ".........\\", # 1 backslash added to escape backslash
    "..../.\\\\..", # 2 backslash added to escape backslash
    ".-.-/..|..",
    ".|....-|.\\", # 1 backslash added to escape backslash
    "..//.|....",
]

class Direction(Enum):
    UP_DOWN = 1
    DOWN_UP = 2
    LEFT_RIGHT = 3
    RIGHT_LEFT = 4

def expand_light(map: List[str], starting_coords: Tuple[int, int], starting_direction: Direction):

    visited_coords_dir = set()
    next_coords_dir = collections.deque()
    next_coords_dir.append((starting_coords, starting_direction))

    while len(next_coords_dir) > 0:
        coords, direction = next_coords_dir.popleft()
        x, y = coords
        if x < 0 or x >= len(map[0]) or y < 0 or y >= len(map):
            # Node outside of boundaries
            continue
        if (coords, direction) in visited_coords_dir:
            # Already visited from this direction
            continue
        visited_coords_dir.add((coords, direction))
        next_node = map[y][x]
        if direction == Direction.LEFT_RIGHT:
            if next_node == ".":
                next_coords_dir.append(((x+1,y), Direction.LEFT_RIGHT))
            elif next_node == "/":
                next_coords_dir.append(((x,y-1), Direction.DOWN_UP))
            elif next_node == "\\":
                next_coords_dir.append(((x,y+1), Direction.UP_DOWN))
            elif next_node == "|":
                next_coords_dir.append(((x,y-1), Direction.DOWN_UP))
                next_coords_dir.append(((x,y+1), Direction.UP_DOWN))
            elif next_node == "-":
                next_coords_dir.append(((x+1,y), Direction.LEFT_RIGHT))
            else:
                raise RuntimeError(f"Node {next_node} not known")
        elif direction == Direction.RIGHT_LEFT:
            if next_node == ".":
                next_coords_dir.append(((x-1,y), Direction.RIGHT_LEFT))
            elif next_node == "/":
                next_coords_dir.append(((x,y+1), Direction.UP_DOWN))
            elif next_node == "\\":
                next_coords_dir.append(((x,y-1), Direction.DOWN_UP))
            elif next_node == "|":
                next_coords_dir.append(((x,y-1), Direction.DOWN_UP))
                next_coords_dir.append(((x,y+1), Direction.UP_DOWN))
            elif next_node == "-":
                next_coords_dir.append(((x-1,y), Direction.RIGHT_LEFT))
            else:
                raise RuntimeError(f"Node {next_node} not known")
        elif direction == Direction.UP_DOWN:
            if next_node == ".":
                next_coords_dir.append(((x,y+1), Direction.UP_DOWN))
            elif next_node == "/":
                next_coords_dir.append(((x-1,y), Direction.RIGHT_LEFT))
            elif next_node == "\\":
                next_coords_dir.append(((x+1,y), Direction.LEFT_RIGHT))
            elif next_node == "|":
                next_coords_dir.append(((x,y+1), Direction.UP_DOWN))
            elif next_node == "-":
                next_coords_dir.append(((x-1,y), Direction.RIGHT_LEFT))
                next_coords_dir.append(((x+1,y), Direction.LEFT_RIGHT))
            else:
                raise RuntimeError(f"Node {next_node} not known")
        elif direction == Direction.DOWN_UP:
            if next_node == ".":
                next_coords_dir.append(((x,y-1), Direction.DOWN_UP))
            elif next_node == "/":
                next_coords_dir.append(((x+1,y), Direction.LEFT_RIGHT))
            elif next_node == "\\":
                next_coords_dir.append(((x-1,y), Direction.RIGHT_LEFT))
            elif next_node == "|":
                next_coords_dir.append(((x,y-1), Direction.DOWN_UP))
            elif next_node == "-":
                next_coords_dir.append(((x-1,y), Direction.RIGHT_LEFT))
                next_coords_dir.append(((x+1,y), Direction.LEFT_RIGHT))
            else:
                raise RuntimeError(f"Node {next_node} not known")
        else:
            raise RuntimeError(f"Direction {direction} not known")

    visited_coords = {coords for coords, _direction in visited_coords_dir}
    return len(visited_coords)

if __name__ == "__main__":

    input_data = aocutils.getDataInput(16)
    #input_data = test_array

    #### Part 1 ####

    aocutils.printResult(1, expand_light(input_data, (0,0), Direction.LEFT_RIGHT))

    #### Part 2 ####

    max_energised = 0
    max_x = len(input_data[0])
    max_y = len(input_data)

    for x in range(max_x):
        max_energised = max(
            max_energised,
            expand_light(input_data, (x,0), Direction.UP_DOWN),
            expand_light(input_data, (x,max_y-1), Direction.DOWN_UP)
        )

    for y in range(max_y):
        max_energised = max(
            max_energised,
            expand_light(input_data, (0,y), Direction.LEFT_RIGHT),
            expand_light(input_data, (max_x-1,y), Direction.RIGHT_LEFT)
        )

    aocutils.printResult(2, max_energised)