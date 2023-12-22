import aocutils
import collections
from typing import List, Tuple, Optional

test_array = [
    "...........",
    ".....###.#.",
    ".###.##..#.",
    "..#.#...#..",
    "....#.#....",
    ".##..S####.",
    ".##..#...#.",
    ".......##..",
    ".##.#.####.",
    ".##..##.##.",
    "...........",
]

coord_offsets = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1),
]

def find_starting_coords(input: List[str]):
    for y, row in enumerate(input):
        for x, val in enumerate(row):
            if val == "S":
                return (x, y)
            
def find_dimensions(input: List[str]):
    size_x = len(input[0])
    size_y = len(input)
    return size_x, size_y

def calculate_reachable_plots(input: List[str], starting_coords: Tuple[int, int], starting_step: int=0, max_steps: Optional[int]=None):
    reach_count_odd = 0
    reach_count_even = 0

    if starting_step < 0:
        RuntimeError(f"Starting step is {starting_step}. It should be at least zero.")

    size_x, size_y = find_dimensions(input)

    visited_steps = [[-1 for _ in range(size_x)] for _ in range(size_y)]
    next_steps = collections.deque()

    next_steps.append((starting_step, starting_coords))

    while len(next_steps) > 0:
        step_count, (x, y) = next_steps.popleft()
        if max_steps and step_count > max_steps:
            continue
        elif x < 0 or x >= size_x or y < 0 or y >= size_y:
            continue
        elif input[y][x] == "#":
            continue
        elif visited_steps[y][x] >= 0:
            continue
        else:
            visited_steps[y][x] = step_count
            if step_count % 2 == 0:
                reach_count_even += 1
            else:
                reach_count_odd += 1
            for off_x, off_y in coord_offsets:
                next_x = x + off_x
                next_y = y + off_y
                next_steps.append((step_count + 1, (next_x, next_y)))
        
    return visited_steps

def count_reached_plots(visited_steps: List[List[int]], steps: int):
    remaining = steps % 2
    count = 0
    for row in visited_steps:
        for val in row:
            if val >= 0 and val % 2 == remaining and val <= steps:
                count += 1
    return count

def merge_reached_plots(visited_steps_1: List[List[int]], visited_steps_2: List[List[int]]):
    size_x, size_y = find_dimensions(visited_steps_1)
    visited_steps = [[-1 for _ in range(size_x)] for _ in range(size_y)]
    for y in range(size_y):
        for x in range(size_x):
            if visited_steps_1[y][x] < 0:
                visited_steps[y][x] = visited_steps_2[y][x]
            elif visited_steps_2[y][x] < 0:
                visited_steps[y][x] = visited_steps_1[y][x]
            else:
                visited_steps[y][x] = min(visited_steps_1[y][x], visited_steps_2[y][x])
    return visited_steps

def print_step_matrix(input: List[str], visited_steps: List[List[int]]):
    output = []
    for y, row in enumerate(input):
        output_row = []
        output.append(output_row)
        for x, val in enumerate(row):
            if val == "#":
                output_row.append("#")
            elif visited_steps[y][x] < 0:
                output_row.append(".")
            else:
                output_row.append(str(visited_steps[y][x] % 10))
    print("\n".join("".join(o_row) for o_row in output))

def assert_open_lanes(input: List[str], has_starting_lane: bool=False):
    _size_x, _size_y = find_dimensions(input)
    start_x, start_y = find_starting_coords(input_data)

    # Check that matrix is a square
    assert _size_x == _size_y
    size = _size_x

    # Assert that all edges are open lanes

    for s in range(size):
        assert input[s][0] == "."
        assert input[s][size-1] == "."
        assert input[0][s] == "."
        assert input[size-1][s] == "."

    # Assert that dimensions are odd and 'S' is in the middle
        
    assert size % 2 == 1
    assert start_x == (size // 2)
    assert start_y == (size // 2)

    # Asser that the time to go from corner to corner is enough to reach all plots

    for xx_start, yy_start in ((0,0), (0, size-1), (size-1, 0), (size-1, size-1)):
        xx_end = (size-1 - xx_start)
        yy_end = (size-1 - yy_start)
        visited_step_matrix = calculate_reachable_plots(input_data, (xx_start, yy_start))
        assert visited_step_matrix[yy_end][xx_end] == 2 * (size-1)
        for y in range(1, size-1):
            for x in range(1, size-1):
                assert visited_step_matrix[y][x] <= visited_step_matrix[yy_end][xx_end]

    # The following assetions only work for the large input
    
    if has_starting_lane:

        # Assert that all middle lanes are open lanes (centered on 'S')

        for s in range(size):
            assert input[s][start_x] in (".", "S")
            assert input[start_y][s] in (".", "S")

        # Check if the time to go from center to edges is enough to reach all of it's values 

        visited_step_matrix = calculate_reachable_plots(input_data, (start_x, start_y))

        assert visited_step_matrix[start_x][0] == visited_step_matrix[start_x][size-1]
        assert visited_step_matrix[0][start_y] == visited_step_matrix[size-1][start_y]

        assert visited_step_matrix[0][0] == visited_step_matrix[0][size-1]
        assert visited_step_matrix[0][0] == visited_step_matrix[size-1][0]
        assert visited_step_matrix[0][0] == visited_step_matrix[size-1][size-1]

        assert visited_step_matrix[0][0] == 2 * visited_step_matrix[start_x][0]
    
        for y in range(1, size-1):
            for x in range(1, size-1):
                assert visited_step_matrix[y][x] < visited_step_matrix[0][0]

def count_reached_plots_infinity(input: List[str], max_steps: int, has_starting_lane: bool=False):
    
    count = 0

    start_coords = find_starting_coords(input_data)
    
    size = len(input_data)
    visited_step_matrix = calculate_reachable_plots(input_data, start_coords)

    reached_plots_on_center_panel = count_reached_plots(visited_step_matrix, 100000 + max_steps % 2)
    reached_plots_on_odd_panel = count_reached_plots(visited_step_matrix, 100000 + max_steps % 2 + 1)

    count += reached_plots_on_center_panel

    up_left_steps = visited_step_matrix[0][0]
    up_right_steps = visited_step_matrix[0][size-1]
    down_left_steps = visited_step_matrix[size-1][0]
    down_right_steps = visited_step_matrix[size-1][size-1]

    start_x, start_y = start_coords
    up_steps = visited_step_matrix[0][start_x]
    down_steps = visited_step_matrix[size-1][start_x]
    left_steps = visited_step_matrix[start_y][0]
    right_steps = visited_step_matrix[start_y][size-1]

    # How many panels are guaranteed to be completed on all directions

    completed_panels_up_left = (max_steps - up_left_steps) // size
    completed_panels_up_right = (max_steps - up_right_steps) // size
    completed_panels_down_left = (max_steps - down_left_steps) // size
    completed_panels_down_right = (max_steps - down_right_steps) // size

    for starting_steps, completed_sides, coords in (
        (up_left_steps, completed_panels_up_left, (size-1, size-1)), 
        (up_right_steps, completed_panels_up_right, (0, size-1)),
        (down_left_steps, completed_panels_down_left, (size-1, 0)),
        (down_right_steps, completed_panels_down_right, (0, 0))):

        panels_like_center_panel = (completed_sides // 2) ** 2
        panels_like_odd_panel = ((completed_sides - 1) // 2) * (1 + ((completed_sides - 1) // 2))

        count += panels_like_center_panel * reached_plots_on_center_panel
        count += panels_like_odd_panel * reached_plots_on_odd_panel

        check_corner_closer_steps = starting_steps + (completed_sides - 1) * size + 2 # TODO: Check these +2
        check_corner_outer_steps = starting_steps + completed_sides * size + 2

        visited_step_matrix_closer = calculate_reachable_plots(input_data, coords, starting_step=check_corner_closer_steps, max_steps=max_steps)
        count += completed_sides * count_reached_plots(visited_step_matrix_closer, max_steps)

        visited_step_matrix_outer = calculate_reachable_plots(input_data, coords, starting_step=check_corner_outer_steps, max_steps=max_steps)
        count += (completed_sides + 1) * count_reached_plots(visited_step_matrix_outer, max_steps)

    if not has_starting_lane:

        count_panels_up = (completed_panels_up_left - 1, completed_panels_up_right - 1)
        count_panels_down = (completed_panels_down_left - 1, completed_panels_down_right - 1)
        count_panels_left = (completed_panels_up_left - 1, completed_panels_down_left - 1)
        count_panels_right = (completed_panels_up_right - 1, completed_panels_down_right - 1)

        count_panels_up_min = min(*count_panels_up)
        count_panels_down_min = min(*count_panels_down)
        count_panels_left_min = min(*count_panels_left)
        count_panels_right_min = min(*count_panels_right)

        count += reached_plots_on_center_panel * (count_panels_up_min // 2)
        count += reached_plots_on_odd_panel * ((count_panels_up_min + 1) // 2)
        count += reached_plots_on_center_panel * (count_panels_down_min // 2)
        count += reached_plots_on_odd_panel * ((count_panels_down_min + 1) // 2)
        count += reached_plots_on_center_panel * (count_panels_left_min // 2)
        count += reached_plots_on_odd_panel * ((count_panels_left_min + 1) // 2)
        count += reached_plots_on_center_panel * (count_panels_right_min // 2)
        count += reached_plots_on_odd_panel * ((count_panels_right_min + 1) // 2)

        # Up blocks

        steps_up_closer_a = up_left_steps + count_panels_up_min * size + 1
        steps_up_closer_b = up_right_steps + count_panels_up_min * size + 1
        steps_up_outer_a = up_left_steps + (count_panels_up_min + 1) * size + 1
        steps_up_outer_b = up_right_steps + (count_panels_up_min + 1) * size + 1

        up_a_coord = (0,size-1)
        up_b_coord = (size-1,size-1)

        visited_step_matrix_up_closer = merge_reached_plots(
            calculate_reachable_plots(input_data, up_a_coord, starting_step=steps_up_closer_a, max_steps=max_steps),
            calculate_reachable_plots(input_data, up_b_coord, starting_step=steps_up_closer_b, max_steps=max_steps)
        )
        visited_step_matrix_up_outer = merge_reached_plots(
            calculate_reachable_plots(input_data, up_a_coord, starting_step=steps_up_outer_a, max_steps=max_steps),
            calculate_reachable_plots(input_data, up_b_coord, starting_step=steps_up_outer_b, max_steps=max_steps)
        )
        count += count_reached_plots(visited_step_matrix_up_closer, max_steps)
        count += count_reached_plots(visited_step_matrix_up_outer, max_steps)


        steps_down_closer_a = down_left_steps + count_panels_down_min * size + 1
        steps_down_closer_b = down_right_steps + count_panels_down_min * size + 1
        steps_down_outer_a  = down_left_steps + (count_panels_down_min + 1) * size + 1
        steps_down_outer_b  = down_right_steps + (count_panels_down_min + 1) * size + 1

        down_a_coord = (0,0)
        down_b_coord = (size-1,0)

        visited_step_matrix_down_closer = merge_reached_plots(
            calculate_reachable_plots(input_data, down_a_coord, starting_step=steps_down_closer_a, max_steps=max_steps),
            calculate_reachable_plots(input_data, down_b_coord, starting_step=steps_down_closer_b, max_steps=max_steps)
        )
        visited_step_matrix_down_outer = merge_reached_plots(
            calculate_reachable_plots(input_data, down_a_coord, starting_step=steps_down_outer_a, max_steps=max_steps),
            calculate_reachable_plots(input_data, down_b_coord, starting_step=steps_down_outer_b, max_steps=max_steps)
        )
        count += count_reached_plots(visited_step_matrix_down_closer, max_steps)
        count += count_reached_plots(visited_step_matrix_down_outer, max_steps)

        steps_left_closer_a = up_left_steps + count_panels_left_min * size + 1
        steps_left_closer_b = down_left_steps + count_panels_left_min * size + 1
        steps_left_outer_a = up_left_steps + (count_panels_left_min + 1) * size + 1
        steps_left_outer_b = down_left_steps + (count_panels_left_min + 1) * size + 1

        left_a_coord = (size-1,0)
        left_b_coord = (size-1,size-1)

        visited_step_matrix_left_closer = merge_reached_plots(
            calculate_reachable_plots(input_data, left_a_coord, starting_step=steps_left_closer_a, max_steps=max_steps),
            calculate_reachable_plots(input_data, left_b_coord, starting_step=steps_left_closer_b, max_steps=max_steps)
        )
        visited_step_matrix_left_outer = merge_reached_plots(
            calculate_reachable_plots(input_data, left_a_coord, starting_step=steps_left_outer_a, max_steps=max_steps),
            calculate_reachable_plots(input_data, left_b_coord, starting_step=steps_left_outer_b, max_steps=max_steps)
        )
        count += count_reached_plots(visited_step_matrix_left_closer, max_steps)
        count += count_reached_plots(visited_step_matrix_left_outer, max_steps)

        steps_right_closer_a = up_right_steps + count_panels_right_min * size + 1
        steps_right_closer_b = down_right_steps + count_panels_right_min * size + 1
        steps_right_outer_a = up_right_steps + (count_panels_right_min + 1) * size + 1
        steps_right_outer_b = down_right_steps + (count_panels_right_min + 1) * size + 1

        right_a_coord = (0,0)
        right_b_coord = (0,size-1)

        visited_step_matrix_right_closer = merge_reached_plots(
            calculate_reachable_plots(input_data, right_a_coord, starting_step=steps_right_closer_a, max_steps=max_steps),
            calculate_reachable_plots(input_data, right_b_coord, starting_step=steps_right_closer_b, max_steps=max_steps)
        )
        visited_step_matrix_right_outer = merge_reached_plots(
            calculate_reachable_plots(input_data, right_a_coord, starting_step=steps_right_outer_a, max_steps=max_steps),
            calculate_reachable_plots(input_data, right_b_coord, starting_step=steps_right_outer_b, max_steps=max_steps)
        )
        count += count_reached_plots(visited_step_matrix_right_closer, max_steps)
        count += count_reached_plots(visited_step_matrix_right_outer, max_steps)

    else:

        assert completed_panels_up_left == completed_panels_up_right
        assert completed_panels_up_left == completed_panels_down_left
        assert completed_panels_up_left == completed_panels_down_right
        
        assert up_steps == down_steps
        assert up_steps == left_steps
        assert up_steps == right_steps

        count_panels = completed_panels_up_left
        steps = up_steps

        # Calculate central columns

        count += reached_plots_on_center_panel * (count_panels // 2)
        count += reached_plots_on_odd_panel * ((count_panels + 1) // 2)
        count += reached_plots_on_center_panel * (count_panels // 2)
        count += reached_plots_on_odd_panel * ((count_panels + 1) // 2)
        count += reached_plots_on_center_panel * (count_panels // 2)
        count += reached_plots_on_odd_panel * ((count_panels + 1) // 2)
        count += reached_plots_on_center_panel * (count_panels // 2)
        count += reached_plots_on_odd_panel * ((count_panels + 1) // 2)
    
        steps_closer = steps + count_panels * size + 1
        steps_outer = steps + (count_panels + 1) * size + 1

        # End of column Up
        coord = (start_x,size-1)
        visited_step_matrix_up_closer = calculate_reachable_plots(input_data, coord, starting_step=steps_closer, max_steps=max_steps)
        visited_step_matrix_up_outer = calculate_reachable_plots(input_data, coord, starting_step=steps_outer, max_steps=max_steps)
        count += count_reached_plots(visited_step_matrix_up_closer, max_steps)
        count += count_reached_plots(visited_step_matrix_up_outer, max_steps)

        # End of column Down
        coord = (start_x,0)
        visited_step_matrix_up_closer = calculate_reachable_plots(input_data, coord, starting_step=steps_closer, max_steps=max_steps)
        visited_step_matrix_up_outer = calculate_reachable_plots(input_data, coord, starting_step=steps_outer, max_steps=max_steps)
        count += count_reached_plots(visited_step_matrix_up_closer, max_steps)
        count += count_reached_plots(visited_step_matrix_up_outer, max_steps)

        # End of column Left
        coord = (size-1,start_y)
        visited_step_matrix_up_closer = calculate_reachable_plots(input_data, coord, starting_step=steps_closer, max_steps=max_steps)
        visited_step_matrix_up_outer = calculate_reachable_plots(input_data, coord, starting_step=steps_outer, max_steps=max_steps)
        count += count_reached_plots(visited_step_matrix_up_closer, max_steps)
        count += count_reached_plots(visited_step_matrix_up_outer, max_steps)

        # End of column Right
        coord = (0,start_y)
        visited_step_matrix_up_closer = calculate_reachable_plots(input_data, coord, starting_step=steps_closer, max_steps=max_steps)
        visited_step_matrix_up_outer = calculate_reachable_plots(input_data, coord, starting_step=steps_outer, max_steps=max_steps)
        count += count_reached_plots(visited_step_matrix_up_closer, max_steps)
        count += count_reached_plots(visited_step_matrix_up_outer, max_steps)
        
    return count

if __name__ == "__main__":

    input_data = aocutils.getDataInput(21)
    #input_data = test_array

    start_coords = find_starting_coords(input_data)

    #### Part 1 ####

    visited_step_matrix_1 = calculate_reachable_plots(input_data, start_coords, max_steps=64)
    aocutils.printResult(1, count_reached_plots(visited_step_matrix_1, 64))

    #### Part 2 ####

    assert_open_lanes(input_data, has_starting_lane=(not (input_data is test_array)))
    aocutils.printResult(2, count_reached_plots_infinity(input_data, 26501365, has_starting_lane=(not (input_data is test_array))))




