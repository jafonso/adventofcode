import aocutils
import heapq
from typing import List, Tuple
from enum import Enum

test_array_1 = [
    "2413432311323",
    "3215453535623",
    "3255245654254",
    "3446585845452",
    "4546657867536",
    "1438598798454",
    "4457876987766",
    "3637877979653",
    "4654967986887",
    "4564679986453",
    "1224686865563",
    "2546548887735",
    "4322674655533",
]

test_array_2 = [
    "111111111111",
    "999999999991",
    "999999999991",
    "999999999991",
    "999999999991",
]

class Direction(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

class WeirdDict:
    def __init__(self):
        self.min_val = None
        self.items_by_val = {}
        self.key_dict = {}
    def pop(self):
        if self.min_val is None:
            raise RuntimeError("No items in WeirdDict")
        val = self.min_val
        # Remove oldest item, considering python dict keeps order
        val_dict = self.items_by_val[self.min_val]
        key = next(iter(val_dict))
        val_dict.pop(key)
        if len(val_dict) == 0:
            del self.items_by_val[self.min_val]
            self.min_val = min(self.items_by_val.keys()) if self.items_by_val else None
        return key, val
    def pushOrModify(self, key, value):
        # Remove old first
        if key in self.key_dict:
            old_val = self.key_dict
            val_dict = self.items_by_val[old_val]
            val_dict.pop(key)
            if len(val_dict) == 0:
                del self.items_by_val[self.min_val]
        # Add again
        self.key_dict[key] = value
        if value not in self.items_by_val:
            self.items_by_val[value] = {}
            self.items_by_val[value][key] = None # Value is irrelevant here
            self.min_val = min(self.items_by_val.keys()) # Update min value
        else:
            self.items_by_val[value][key] = None
    def __len__(self):
        return len(self.key_dict)

map_offsets = [
    (0,1, Direction.DOWN),
    (0,-1, Direction.UP),
    (-1,0, Direction.LEFT),
    (1,0, Direction.RIGHT),
]

MAX_STEPS = 10**10

def search_path(map: List[str], starting_coords: Tuple[int, int], min_steps: int=1, max_steps: int=MAX_STEPS):
    # Dijsktra algorithm

    max_x = len(map[0])
    max_y = len(map)

    next_node_heap = WeirdDict()
    node_dist_dict = {}
    prev_node_dict = {}

    x_prev, y_prev = starting_coords
    node_dist_dict[x_prev, y_prev, None, None] = 0
    prev_node_dict[x_prev, y_prev, None, None] = ((None, None, None, None), None)
    
    # Insert initial values
    for x_off, y_off, dir_next in map_offsets:
        x_next = x_prev + x_off
        y_next = y_prev + y_off
        if x_next < 0 or x_next >= max_x or y_next < 0 or y_next >= max_y:
            continue
        new_val = int(map[y_next][x_next])
        next_node_heap.pushOrModify((x_next, y_next, dir_next, 1), new_val)
        node_dist_dict[x_next, y_next, dir_next, 1] = new_val
        prev_node_dict[x_next, y_next, dir_next, 1] = ((x_prev, y_prev, None, None), 0)

    while len(next_node_heap) > 0:
        (x_prev, y_prev, dir_prev, dist_prev), value_prev = next_node_heap.pop()

        # Check all neighbours
        for x_off, y_off, dir_next in map_offsets:

            # Do not revert direction
            if (dir_next, dir_prev) in (
                    (Direction.UP, Direction.DOWN),
                    (Direction.DOWN, Direction.UP),
                    (Direction.LEFT, Direction.RIGHT), (Direction.RIGHT, Direction.LEFT)
                ):
                continue

            # Check minimum steps in one direction
            if dir_next != dir_prev and dist_prev < min_steps:
                continue

            # Calculate next positions
            x_next = x_prev + x_off
            y_next = y_prev + y_off
            if x_next < 0 or x_next >= max_x or y_next < 0 or y_next >= max_y:
                continue

            # Calculate how many steps in one direction
            dist_next = dist_prev + 1 if dir_next == dir_prev else 1

            # Check maximum steps in one directione
            if dist_next > max_steps:
                continue

            # If this is the last, try to return
            if x_next == max_x-1 and y_next == max_y-1:
                if dist_next < min_steps:
                    continue
                value_next = value_prev + int(map[y_next][x_next])
                node_dist_dict[x_next, y_next, dir_next, dist_next] = value_next
                prev_node_dict[x_next, y_next, dir_next, dist_next] = ((x_prev, y_prev, dir_prev, dist_prev), value_prev)
                return prev_node_dict, node_dist_dict
        
            value_next = value_prev + int(map[y_next][x_next])
            if (x_next, y_next, dir_next, dist_next) not in node_dist_dict or value_next < node_dist_dict[x_next, y_next, dir_next, dist_next]:
                node_dist_dict[x_next, y_next, dir_next, dist_next] = value_next
                prev_node_dict[x_next, y_next, dir_next, dist_next] = ((x_prev, y_prev, dir_prev, dist_prev), value_prev)
                next_node_heap.pushOrModify((x_next, y_next, dir_next, dist_next), value_next)
    #return prev_node_dict, node_dist_dict

def get_lowest_node_on(node_dist_dict, x: int, y: int, MAX_STEPS: int=1000):
    for distance in range(MAX_STEPS):
        for direction in (Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT):
            if (x , y, direction, distance) in node_dist_dict:
                return (x , y, direction, distance)
    raise RuntimeError(f"Could not find lowest node on ({x},{y})")

if __name__ == "__main__":

    input_data = aocutils.getDataInput(17)
    #input_data = test_array_1
    #input_data = test_array_2

    #### Part 1 ####
    
    _, node_dist_dict_1 = search_path(input_data, (0,0), min_steps=1, max_steps=3)
    last_x1, last_y1 = len(input_data[0])-1, len(input_data)-1
    node_tuple_1 = get_lowest_node_on(node_dist_dict_1, last_x1, last_y1)
    aocutils.printResult(1, node_dist_dict_1[node_tuple_1])

    #### Part 2 ####

    _, node_dist_dict_2 = search_path(input_data, (0,0), min_steps=4, max_steps=10)
    last_x2, last_y2 = len(input_data[0])-1, len(input_data)-1
    node_tuple_2 = get_lowest_node_on(node_dist_dict_2, last_x2, last_y2)
    aocutils.printResult(2, node_dist_dict_2[node_tuple_2])