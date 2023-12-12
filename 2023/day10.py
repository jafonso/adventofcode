import aocutils
from typing import List, Tuple, Set

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

def edge_between_tiles(tile_1_coords: Tuple[int, int], tile_2_coords: Tuple[int, int]):
    tile_1_x, tile_1_y = tile_1_coords
    tile_2_x, tile_2_y = tile_2_coords
    if tile_1_x == tile_2_x:
        x = tile_1_x
        y = max(tile_1_y, tile_2_y)
        return frozenset({(x, y), (x+1,y)})
    elif tile_1_y == tile_2_y:
        x = max(tile_1_x, tile_2_x)
        y = tile_1_y
        return frozenset({(x, y), (x,y+1)})
    raise RuntimeError(f"Tiles {tile_1_coords}, {tile_2_coords} are not adjacent")

def cut_edge_between_tiles(tile_edges: Set[Set[Tuple[int, int]]], tile_1_coords: Tuple[int, int], tile_2_coords: Tuple[int, int]):
    tile_edges.remove(edge_between_tiles(tile_1_coords, tile_2_coords))

if __name__ == "__main__":

    input_data = aocutils.getDataInput(10)
    #input_data = test_array_1
    #input_data = test_array_2
    #input_data = test_array_3

    #### Part 1 ####

    visited_tiles = [[False for _ in range(len(input_data[0]))] for _ in range(len(input_data))]

    # Get set of all edges between tiles

    #   +---(edge 1)---+
    #   |              |
    #   |   Tile x,y   |
    #(edge 4)       (edge 2)
    #   |              |
    #   |              |
    #   +---(edge 3)---+
    #
    # edge 1: (x,y)     <> (x+1,y)
    # edge 2: (x+1,y)   <> (x+1,y+1)
    # edge 3: (x+1,y+1) <> (x,y+1)
    # edge 4: (x,y+1)   <> (x,y)

    tile_edges = set()
    for y in range(len(input_data)):
        for x in range(len(input_data[0])):
            tile_edges.add(frozenset({(x,y), (x+1,y)}))
            tile_edges.add(frozenset({(x+1,y),(x+1,y+1)}))
            tile_edges.add(frozenset({(x+1,y+1), (x,y+1)}))
            tile_edges.add(frozenset({(x,y+1), (x,y)}))

    # Check that the number of edges is correct (edges of all tiles, two tiles sharing an edge just count as one)
    assert len(tile_edges) == ((len(input_data[0]) * len(input_data) * 2) + len(input_data[0]) + len(input_data))

    (start_x, start_y) = find_s_coords(input_data)
    value_for_s = find_s_value(input_data, start_x, start_y)
    input_data[start_y] = input_data[start_y].replace("S", value_for_s)

    count = 0
    x, y = start_x, start_y
    while visited_tiles[y][x] == False:
        visited_tiles[y][x] = True
        count += 1
        for off_x, off_y in symbol_adj_map[input_data[y][x]]:
            if input_data[y + off_y][x + off_x] != '.' and visited_tiles[y + off_y][x + off_x] == False:
                # Cut edge between tiles
                cut_edge_between_tiles(tile_edges, (x, y), (x + off_x, y + off_y))
                # Update current tile
                x += off_x
                y += off_y
                break
        else:
            pass
    # Cut last edge between end and start
    cut_edge_between_tiles(tile_edges, (x, y), (start_x, start_y))

    aocutils.printResult(1, count // 2)

    #### Part 2 ####
    
    visited_tile_corners = [[False for _ in range(len(input_data[0]) + 1)] for _ in range(len(input_data) + 1)]

    # Go along all tile corners, starting from (0,0) which is guaranteed to be outside, and mark the ones that are connected
    next_corner_list = []
    next_corner_list.append((0,0))

    while next_corner_list:
        x, y = next_corner_list.pop()
        if visited_tile_corners[y][x] == True:
            continue
        visited_tile_corners[y][x] = True
        for off_x, off_y in valid_s_adj.keys():
            if frozenset({(x,y), (x + off_x, y + off_y)}) in tile_edges:   
                next_corner_list.append((x + off_x, y + off_y))

    # Finally, count all tiles whose 4 corners were not visited
    # These are the ones inside the loop
    tiles_inside_loop_count = 0
    for y in range(len(input_data)):
        for x in range(len(input_data[0])):
            if not any(visited_tile_corners[y+off_y][x+off_x] for off_x,off_y in [(0,0), (0,1), (1,0), (1,1)]):
                tiles_inside_loop_count += 1
    aocutils.printResult(2, tiles_inside_loop_count)