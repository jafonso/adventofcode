import aocutils
from typing import List, Tuple

test_array = [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#.....",
]

def calculate_real_galaxy_coords(data: List[str], rate: int):
    empty_col_list = [True] * len(data[0])
    empty_row_list = [True] * len(data)
    galaxy_coords_list = []

    # Get seen galaxies and empty rows/columns
    for y,row in enumerate(data):
        for x,val in enumerate(row):
            if val == "#":
                galaxy_coords_list.append((x, y))
                empty_col_list[x] = False
                empty_row_list[y] = False

    # Calculate the space expansion rates
    expansion_x = []
    expansion_y = []
    curr_expansion_x = 0
    curr_expansion_y = 0
    for is_empty in empty_col_list:
        if is_empty:
            curr_expansion_x += (rate - 1)
        expansion_x.append(curr_expansion_x)
    for is_empty in empty_row_list:
        if is_empty:
            curr_expansion_y += (rate - 1)
        expansion_y.append(curr_expansion_y)

    # Calculate the real positions of galaxies and return
    expanded_coords_list = []
    for x,y in galaxy_coords_list:
        expanded_coords_list.append((x + expansion_x[x], y + expansion_y[y]))
    return expanded_coords_list

def calculate_sum_of_distances(real_galaxy_coords: List[Tuple[int, int]]):
    distances = []
    for idx_1, galaxy_1_coords in enumerate(real_galaxy_coords):
        for idx_2, galaxy_2_coords in enumerate(real_galaxy_coords[idx_1+1:]):
            distances.append(abs(galaxy_2_coords[0]-galaxy_1_coords[0]) + abs(galaxy_2_coords[1]-galaxy_1_coords[1]))
    return sum(distances)

if __name__ == "__main__":
    
    input_data = aocutils.getDataInput(11)
    #input_data = test_array

    # Part 1

    real_galaxy_coords_1 = calculate_real_galaxy_coords(input_data, 2)
    aocutils.printResult(1, calculate_sum_of_distances(real_galaxy_coords_1))

    # Part 2

    real_galaxy_coords_2 = calculate_real_galaxy_coords(input_data, 1000000)
    aocutils.printResult(1, calculate_sum_of_distances(real_galaxy_coords_2))