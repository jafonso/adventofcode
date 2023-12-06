
import aocutils
from typing import List

test_array = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]

def find_number_with_digit_on(x, y, grid: List[str]):
    x_min = x
    x_max = x
    grid_max_x = len(grid[0])
    while x_min >= 0 and grid[y][x_min-1].isdigit():
        x_min -= 1
    while x_max < grid_max_x and grid[y][x_max].isdigit():
        x_max += 1
    return (x_min, y), int(grid[y][x_min:x_max])

def find_adjacent_numbers(x, y, grid):
    max_x = len(grid[0])
    max_y = len(grid)
    coords = {
        (-1,-1), (0,-1), (1,-1), 
        (-1, 0),         (1, 0),
        (-1, 1), (0, 1) ,(1, 1)
    }
    numbers_hit = set()
    numbers_found = []
    for x_dif, y_dif in coords:
        new_x = x + x_dif
        new_y = y + y_dif
        if new_x < 0 or new_x >= max_x:
            continue
        if new_y < 0 or new_y >= max_y:
            continue
        if grid[new_y][new_x].isdigit():
            coords, number = find_number_with_digit_on(new_x, new_y, grid)
            if coords not in numbers_hit:
                numbers_hit.add(coords)
                numbers_found.append(number)

    if len(numbers_found) == 0:
        RuntimeError(f"No number found in coords ({x},{y})")
    else:
        return numbers_found

if __name__ == "__main__":

    input_data = aocutils.getDataInput(3)
    #input_data = test_array

    # Part 1
    result_1 = 0
    for y,row in enumerate(input_data):
        for x,val in enumerate(row):
            if not val.isdigit() and val != '.':
                values = find_adjacent_numbers(x, y, input_data)
                result_1 += sum(values)
    aocutils.printResult(1, result_1)

    # Part 2
    result_2 = 0
    for y,row in enumerate(input_data):
        for x,val in enumerate(row):
            if val == '*':
                values = find_adjacent_numbers(x, y, input_data)
                if len(values) == 2:
                    result_2 += (values[0] * values[1])
    aocutils.printResult(2, result_2)