import aocutils
from typing import List, Tuple
from enum import Enum

test_array = [
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

class Direction(Enum):
    DOWN = 1
    UP = 2
    LEFT = 3
    RIGHT = 4

class HeapDict():
    heap = []
    key_dict = {}
    def pop(self):
        key = self.heap.pop()
        return (key, self.key_dict.pop(key))
    def pushOrModify(self, key, value):
        if key not in self.key_dict:
            self.heap.append(key)
        self.key_dict[key] = value
        self.heap.sort(key=lambda k: self.key_dict[k], reverse=True)
    def __len__(self):
        return len(self.key_dict)

map_offsets = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
]

def search_path(map: List[str], starting_coords: Tuple[int, int]):
    # Dijsktra algorithm
    x, y = starting_coords
    value = int(map[y][x])

    max_x = len(map[0])
    max_y = len(map)

    next_node_heap = HeapDict()
    prev_node_dict = {}
    node_dist_dict = {}

    # Original distance to all nodes is infinite, except for starting node
    large_value = 10**10 # Very large value
    for yy in range(max_y):
        for xx in range(max_x):
            node_dist_dict[xx,yy] = large_value
            next_node_heap.pushOrModify((xx, yy), large_value)

    # Insert starting node on the heap
    next_node_heap.pushOrModify((x,y), value)
    node_dist_dict[x,y] = 0
    prev_node_dict[x,y] = (None, None)

    while len(next_node_heap) > 0:
        #print([(key, next_node_heap.key_dict[key]) for key in next_node_heap.heap if next_node_heap.key_dict[key] < large_value ])
        (x,y), value = next_node_heap.pop()
        for x_off, y_off in map_offsets:
            x_next = x + x_off
            y_next = y + y_off
            if x_next < 0 or x_next >= max_x or y_next < 0 or y_next >= max_y:
                continue
            try:
                prev_x_1, prev_y_1 = prev_node_dict[x, y]
                prev_x_2, prev_y_2 = prev_node_dict[prev_x_1, prev_y_1]
                prev_x_3, prev_y_3 = prev_node_dict[prev_x_2, prev_y_2]
                if x_off != 0 and y == prev_y_1 and y == prev_y_2 and y == prev_y_3:
                    continue # 3 in a row horizontal
                if y_off != 0 and x == prev_x_1 and x == prev_x_2 and x == prev_x_3:
                    continue # 3 in a row vertical
            except KeyError:
                pass
            new_val = node_dist_dict[x,y] + int(map[y_next][x_next])
            if (x_next, y_next) not in node_dist_dict or new_val < node_dist_dict[x_next, y_next]:
                # NOTE: Problem is here... 'new_val' may be larger than 'node_dist_dict[x_next, y_next]' if we stopped due to 3 in a row
                node_dist_dict[x_next, y_next] = new_val
                prev_node_dict[x_next, y_next] = (x, y)
                next_node_heap.pushOrModify((x_next, y_next), new_val)
    return prev_node_dict, node_dist_dict

if __name__ == "__main__":

    #input_data = aocutils.getDataInput(17)
    input_data = test_array

    #### Part 1 ####
    
    prev_node_dict, node_dist_dict = search_path(input_data, (0,0))
    last_x, last_y = len(input_data[0])-1, len(input_data)-1
    x, y = last_x, last_y
    while x != None:
        #print((x,y), "->", node_dist_dict[x,y])
        x, y = prev_node_dict[x, y]

    aocutils.printResult(1, node_dist_dict[last_x, last_y])