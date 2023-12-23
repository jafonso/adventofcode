import aocutils
import functools
import collections
from typing import List, Dict, Tuple, Set

test_array = [
    "1,0,1~1,2,1",
    "0,0,2~2,0,2",
    "0,2,3~2,2,3",
    "0,0,4~0,2,4",
    "2,0,5~2,2,5",
    "0,1,6~2,1,6",
    "1,1,8~1,1,9",
]

def parse_data(input: List[str]):
    bricks = {}
    brick_count = 0
    for entry in input:
        bricks[brick_count] = set()
        coords_1, coords_2 = entry.split("~")
        x1, y1, z1 = (int(s) for s in coords_1.split(","))
        x2, y2, z2 = (int(s) for s in coords_2.split(","))
        x1, x2 = (x2, x1) if x1 > x2 else (x1, x2)
        y1, y2 = (y2, y1) if y1 > y2 else (y1, y2)
        z1, z2 = (z2, z1) if z1 > z2 else (z1, z2)
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                for z in range(z1, z2+1):
                    bricks[brick_count].add((x,y,z))
        brick_count += 1
    return bricks

def fill_3d_grid(bricks: Dict[int, Tuple[int, int, int]]):
    grid = collections.defaultdict(dict) # This way we can check any Z position, even if it was not added
    for brick_key, coords in bricks.items():
        for x,y,z in coords:
            grid[z][x, y] = brick_key # With z, (x,y) for easily checking layer by layer
    return grid 

def move_brick_down(brick_key: int, new_z_min: int, bricks: Dict[int, Set[Tuple[int, int, int]]], grid: Dict[int, Dict[Tuple[int, int], int]]):
    # First, clear from grid
    for x,y,z in bricks[brick_key]:
        del grid[z][x, y]
    # Then, change the brick coords
    curr_z_min = min(z for _,_,z in bricks[brick_key])
    z_offset = curr_z_min - new_z_min
    new_bricks_set = set()
    for x,y,z in bricks[brick_key]:
        new_bricks_set.add((x,y,z - z_offset))
    bricks[brick_key] = new_bricks_set
    # Finally, add it back to the grid
    for x,y,z in bricks[brick_key]:
        grid[z][x, y] = brick_key

def let_bricks_fall(bricks: Dict[int, Set[Tuple[int, int, int]]], grid: Dict[int, Dict[Tuple[int, int], int]]):
    max_z = max(grid.keys())
    # Where is the last block in a column. By default 0 (ground).
    bottom_view = collections.defaultdict(int)
    for z in range(1, max_z+1):
        level_grid = grid[z]
        bricks_on_level = set(level_grid.values())
        for brick_key in bricks_on_level:
            brick_z_min = min(z for _,_,z in bricks[brick_key])
            if brick_z_min < z:
                # We have already pushed this brick as low as possible, nothing to do
                continue
            brick_xy_set = set((x,y) for x,y,_ in bricks[brick_key])
            min_z_possible = max(bottom_view[x,y]+1 for x,y in brick_xy_set)
            #print(min_z_possible)
            move_brick_down(brick_key, min_z_possible, bricks, grid)
            # Update bottom view
            new_max_z = max(z for _,_,z in bricks[brick_key])
            for xx, yy in brick_xy_set:
                bottom_view[xx, yy] = new_max_z

def get_directly_desintegrated_bricks(brick_key: int, bricks: Dict[int, Set[Tuple[int, int, int]]], grid: Dict[int, Dict[Tuple[int, int], int]]):
    
    max_z = max(z for _,_,z in bricks[brick_key])
    level_grid = grid[max_z]
    above_grid = grid[max_z+1]
    above_grid_bricks = set(above_grid.values())

    supported_bricks = set()
    for x,y in above_grid:
        if (x,y) in level_grid and level_grid[x,y] != brick_key:
            supported_bricks.add(above_grid[x,y])

    # the brick is safe to remove if all other bricks are still supported
    return above_grid_bricks - supported_bricks

def get_dependency_graph(bricks: Dict[int, Set[Tuple[int, int, int]]], grid: Dict[int, Dict[Tuple[int, int], int]]):
    dependency_graph = [set() for _ in bricks]

    # Know which bricks supports each other
    max_z = max(z for blocks in bricks.values() for _,_,z in blocks)
    for z in range(1, max_z):
        level_grid = grid[z]
        above_grid = grid[z+1]
        for x,y in above_grid:
            if (x,y) in level_grid and level_grid[x,y] != above_grid[x,y]:
                dependency_graph[above_grid[x,y]].add(level_grid[x,y])

    return tuple(frozenset(s) for s in dependency_graph)

@functools.lru_cache
def is_broken_by_removing(brick: int, removed_brick: int):
    if brick == removed_brick:
        return True
    elif len(get_all_desintegrated_bricks.dependency_graph[brick]) == 0:
        return False
    else:
        return all(is_broken_by_removing(next_brick, removed_brick) for next_brick in get_all_desintegrated_bricks.dependency_graph[brick])

def get_all_desintegrated_bricks(brick_key: int, bricks: Dict[int, Set[Tuple[int, int, int]]], grid: Dict[int, Dict[Tuple[int, int], int]]):
    
    get_all_desintegrated_bricks.dependency_graph = get_dependency_graph(bricks, grid)

    desintegrated_bricks = set()
    for i in bricks:
        if is_broken_by_removing(i, brick_key) and i != brick_key:
            desintegrated_bricks.add(i)

    return desintegrated_bricks

get_all_desintegrated_bricks.dependency_graph = None


if __name__ == "__main__":

    input_data = aocutils.getDataInput(22)
    #input_data = test_array

    bricks = parse_data(input_data)
    grid = fill_3d_grid(bricks)
    let_bricks_fall(bricks, grid)

    #### Part 1 ####

    count_1 = 0
    for brick_key in bricks:
        desintegrated_bricks = get_directly_desintegrated_bricks(brick_key, bricks, grid)
        if len(desintegrated_bricks) == 0:
            count_1 += 1
    
    aocutils.printResult(1, count_1)

    #### Part 2 ####

    count_2 = 0
    for brick_key in bricks:
        desintegrated_bricks = get_all_desintegrated_bricks(brick_key, bricks, grid)
        count_2 += len(desintegrated_bricks)
    
    aocutils.printResult(2, count_2)
