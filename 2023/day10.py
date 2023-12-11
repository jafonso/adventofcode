import aocutils
from typing import List

test_array_1 = [
    "-L|F7",
    "7S-7|",
    "L|7||",
    "-L-J|",
    "L|-JF",
]

test_array_2 = [
    "7-F7-",
    ".FJ|7",
    "SJLL7",
    "|F--J",
    "LJ.LJ",
]

test_array_3 = [
    "...........",
    ".S-------7.",
    ".|F-----7|.",
    ".||.....||.",
    ".||.....||.",
    ".|L-7.F-J|.",
    ".|..|.|..|.",
    ".L--J.L--J.",
    "...........",
]

# Mapping symbols to adjacent node offsets (x,y)
symbol_adj_map = {
    "|": {( 0,-1), ( 0,1)},
    "-": {(-1, 0), ( 1,0)},
    "L": {( 0,-1), ( 1,0)},
    "J": {( 0,-1), (-1,0)},
    "7": {( 0, 1), (-1,0)},
    "F": {( 0, 1), ( 1,0)},
    ".": {},
    "S": {(-1, 0), ( 1,0), ( 0,-1), ( 0, 1)},
}

valid_s_adj = {
    (-1, 0): {"-", "L", "F"},
    ( 1, 0): {"-", "J", "7"},
    ( 0,-1): {"|", "7", "F"},
    ( 0, 1): {"-", "J", "7"},
}

def find_s_coords(data: List[str]):
    for y, row in enumerate(data):
        sx_pos = row.find("S")
        if sx_pos >= 0:
            return (sx_pos, y)

def find_s_value(data: List[str], x, y):
    # Ignoring corner case where S is on a edge
    if data[y-1][x] in {"|", "F", "7"}:
        if data[y][x+1] in {"-", "J", "7"}:
            return "L"
        elif data[y+1][x] in {"|", "J", "L"}:
            return "|"
        elif data[y][x-1] in {"-", "L", "F"}:
            return "J"
    elif data[y][x+1] in {"-", "J", "7"}:
        if data[y+1][x] in {"|", "J", "L"}:
            return "F"
        elif data[y][x-1] in {"-", "L", "F"}:
            return "-"
    elif data[y+1][x] in {"|", "J", "L"}:
        if data[y][x-1] in {"-", "L", "F"}:
            return "7"
    raise RuntimeError("Did not find value for S")

if __name__ == "__main__":

    #input_data = aocutils.getDataInput(10)
    #input_data = test_array_1
    #input_data = test_array_2
    input_data = test_array_3

    # Part 1

    visited_nodes = [[False for _ in range(len(input_data[0]))] for _ in range(len(input_data))]

    (x, y) = find_s_coords(input_data)
    count = 0
    while visited_nodes[y][x] == False:
        visited_nodes[y][x] = True
        count += 1
        if input_data[y][x] == "S":
            value_for_s = find_s_value(input_data, x, y)
            input_data[y].replace("S", value_for_s)
        for off_x, off_y in symbol_adj_map[input_data[y][x]]:
            if input_data[y + off_y][x + off_x] != '.' and visited_nodes[y + off_y][x + off_x] == False:
                x += off_x
                y += off_y
                break
        else:
            pass
    aocutils.printResult(1, count // 2)
    
    # Part 2

    # 1. Create matrix of corners between tile positions
    # 2. Starting by a matrix corner (which is always outside) expand to all outside corners, and mark them
    # 3. Visit the full matrix, checking corners 4-by-4 (a square/tile).
    # 4. If none of the 4 corners is marked, it corresponds to a tile that is enclosed by the loop
    # 5. Count this
    
    corner_matrix = [[False for _ in range(len(input_data[0]) + 1)] for _ in range(len(input_data) + 1)]

    can_move = {
        (-1, 0): {".", "-", "J", "L"}, # Check value on -1,-1
        ( 0,-1): {".", "|", "J", "F"},
        ( 1, 0): {".", "-", "7", "F"}, # Check value on 1,1
        ( 0, 1): {".", "|", "F", "L"},
    }

    next_list = []
    next_list.append((0,0))
    while len(next_list) > 0:
        x, y = next_list.pop()
        print(x, y)
        corner_matrix[y][x] = True
        for (off_x, off_y), accepted_tiles in can_move.items():
            try:
                next_x = x + off_x
                next_y = y + off_y
                print(next_x, next_y)
                if corner_matrix[next_y][next_x]:
                    continue
                if off_x > 0 or off_y > 0:
                    if not visited_nodes[next_y][next_x] or corner_matrix[next_y][next_x] in accepted_tiles:
                        next_list.append((next_x, next_y))
                elif off_x < 0 or off_y < 0:
                    if not visited_nodes[next_y - 1][next_x - 1] or corner_matrix[next_y][next_x] in accepted_tiles:
                        next_list.append((next_x, next_y))
            except IndexError:
                continue
    print(corner_matrix)




