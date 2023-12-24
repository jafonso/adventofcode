import aocutils
from typing import List, Dict, Tuple, Set

test_array = [
    "#.#####################",
    "#.......#########...###",
    "#######.#########.#.###",
    "###.....#.>.>.###.#.###",
    "###v#####.#v#.###.#.###",
    "###.>...#.#.#.....#...#",
    "###v###.#.#.#########.#",
    "###...#.#.#.......#...#",
    "#####.#.#.#######.#.###",
    "#.....#.#.#.......#...#",
    "#.#####.#.#.#########v#",
    "#.#...#...#...###...>.#",
    "#.#.#v#######v###.###v#",
    "#...#.>.#...>.>.#.###.#",
    "#####v#.#.###v#.#.###.#",
    "#.....#...#...#.#.#...#",
    "#.#########.###.#.#.###",
    "#...###...#...#...#.###",
    "###.###.#.###v#####v###",
    "#...#...#.#.>.>.#.>.###",
    "#.###.###.#.###.#.#v###",
    "#.....###...###...#...#",
    "#####################.#",
]

offsets = [
    ( 1, 0),
    (-1, 0),
    ( 0, 1),
    ( 0,-1),
]

def find_edges(nodes_dict: Dict[Tuple[int, int], int], input: List[str]):
    
    max_x = len(input[0])
    max_y = len(input)
    edges = {}

    for node_coords, node_id in nodes_dict.items():

        x, y = node_coords
        edges[node_id] = set()
        visited = set()
        next_steps = []
        next_steps.append((node_coords, 0))

        if input[y][x] != ".":
            raise RuntimeError(f"Unexpected character '{input[y][x]}' in node ({x},{y})")
        
        while next_steps:
            curr_coords, curr_dist = next_steps.pop()
            visited.add(curr_coords)
            if curr_coords in nodes_dict and curr_dist > 0:
                # If node corresponds to another node, create edge
                edges[node_id].add((nodes_dict[curr_coords], curr_dist))
                continue
            # Otherwise, check all connected nodes
            x_curr, y_curr = curr_coords
            for x_off, y_off in offsets:
                x_next = x_curr+x_off
                y_next = y_curr+y_off
                if x_next < 0 or x_next >= max_x or y_next < 0 or y_next >= max_y:
                    continue
                next_coords = (x_next, y_next)
                next_symbol = input[y_curr+y_off][x_curr+x_off]
                if next_coords in visited:
                    # Ignore if visited
                    continue
                elif next_symbol == "#":
                    # Ignore if trees
                    continue
                elif next_symbol == ".":
                    next_steps.append((next_coords, curr_dist+1))
                elif x_off == 1 and next_symbol == ">":
                     next_steps.append((next_coords, curr_dist+1))
                elif x_off == -1 and next_symbol == "<":
                    next_steps.append((next_coords, curr_dist+1))
                elif y_off == 1 and next_symbol == "v":
                     next_steps.append((next_coords, curr_dist+1))
                elif y_off == -1 and next_symbol == "^":
                    next_steps.append((next_coords, curr_dist+1))
                elif x_off == 1 and next_symbol == "<":
                    # Not connected in this direction
                    continue
                elif x_off == -1 and next_symbol == ">":
                    # Not connected in this direction
                    continue
                elif y_off == 1 and next_symbol == "^":
                    # Not connected in this direction
                    continue
                elif y_off == -1 and next_symbol == "v":
                    # Not connected in this direction
                    continue
                else:
                    raise RuntimeError(f"Unexpected character '{next_symbol}' in node ({next_coords[0]}, {next_coords[1]})")

    return edges

def parse_data(input: List[str]):

    size_x = len(input[0])
    size_y = len(input)
    nodes = []

    for i, c in enumerate(input[0]):
        if c == ".":
            node_start = (i,0)
            break
    for i, c in enumerate(input[size_y-1]):
        if c == ".":
            node_end = (i, size_y-1)
            break
    
    # Starting node
    nodes.append(node_start)

    # Find intersections (nodes)
    for y in range(1, size_y-1):
        for x in range(1, size_x-1):
            if input[y][x] == "#":
                # Ignore forest
                continue
            connected_paths = 0
            connected_dots = 0
            for x_off, y_off in offsets:
                if input[y+y_off][x+x_off] != "#":
                    connected_paths += 1
                    if input[y+y_off][x+x_off] == ".":
                        connected_dots += 1
            if connected_paths > 2:
                # More than 2 paths means an intersection
                if connected_dots > 0:
                    # Assert this...
                    # It means that all edges are in one direction only
                    raise RuntimeError(f"Node ({x}, {y}) is connected to a dot")
                nodes.append((x, y))

    # Ending node
    nodes.append(node_end)

    # Node to idx
    nodes_dict_by_coord = {(x,y): idx for idx, (x,y) in enumerate(nodes)}
    nodes_dict_by_id = {idx: (x, y) for idx, (x,y) in enumerate(nodes)}

    # Find edges
    edges = find_edges(nodes_dict_by_coord, input)

    #for coords, id in nodes_dict_by_id.items():
    #    print(f"Node {coords}: {id}")
    #print("Edges:")
    #for node_from, node_to_set in edges.items():
    #     for node_to, dist in node_to_set:
    #        print(f"{node_from} --> {node_to} ({dist})")

    return nodes, edges

def longest_dist_from_to(nodes: List[Tuple[int, int]], edges: Dict[int, Set[int]], start_id: int, end_id: int, visited_set: Set[int]):

    # End of recursive function
    if start_id == end_id:
        return 0

    max_dist = 0
    for to_id, dist in edges[start_id]:
        if to_id in visited_set:
            continue
        remain_dist = dist + longest_dist_from_to(nodes, edges, to_id, end_id, visited_set | {to_id})
        if max_dist < remain_dist:
            max_dist = remain_dist
    return max_dist

def edges_without_slopes(edges: Dict[int, Set[int]]):
    output = {}
    for from_id, to_id_dist_set in edges.items():
        if from_id not in output:
            output[from_id] = set()
        for to_id, dist in to_id_dist_set:
            if to_id not in output:
                output[to_id] = set()
            output[from_id].add((to_id, dist))
            output[to_id].add((from_id, dist))
    return output

def find_longest_hike(nodes: List[Tuple[int, int]], edges: Dict[int, Set[int]], is_slippery: bool):

    node_start_id = 0
    node_end_id = len(nodes)-1
    if is_slippery:
        return longest_dist_from_to(nodes, edges, node_start_id, node_end_id, {node_start_id})
    else:
        edges_no_slopes = edges_without_slopes(edges)
        return longest_dist_from_to(nodes, edges_no_slopes, node_start_id, node_end_id, {node_start_id})

if __name__ == "__main__":


    input_data = aocutils.getDataInput(23)
    #input_data = test_array

    nodes, edges = parse_data(input_data)

    #### Part 1 ####

    aocutils.printResult(1, find_longest_hike(nodes, edges, True))

    #### Part 1 ####

    aocutils.printResult(2, find_longest_hike(nodes, edges, False))

