import aocutils
import functools
from typing import Tuple

test_array_1 = [
    "#.#.### 1,1,3",
    ".#...#....###. 1,1,3",
    ".#.###.#.###### 1,3,1,6",
    "####.#...#... 4,1,1",
    "#....######..#####. 1,6,5",
    ".###.##....# 3,2,1",
]

test_array_2 = [
    "???.### 1,1,3",
    ".??..??...?##. 1,1,3",
    "?#?#?#?#?#?#?#? 1,3,1,6",
    "????.#...#... 4,1,1",
    "????.######..#####. 1,6,5",
    "?###???????? 3,2,1",
]

def parse_data(input: str):
    return [(spring_str, tuple(int(g) for g in spring_groups.split(","))) for spring_str, spring_groups in [row.split() for row in input]]

def unfold_data(springs_list, factor: int):
    return [("?".join([spring_str] * factor), spring_groups * factor) for spring_str, spring_groups in springs_list]

@functools.lru_cache
def count_arrangements(spring_str: str, spring_groups: Tuple[int]):
    if len(spring_str) == 0 and len(spring_groups) > 0:
        # No more springs in the string
        return 0
    elif len(spring_groups) == 0:
        # There should not be any more groups of damaged springs (#) in the string
        # If this is true then we found a valid arrangement
        return 1 if "#" not in spring_str else 0
    elif spring_str[0] == ".":
        # There is at least one leading operational spring in the string
        # Trim it and call againg recursivelly
        return count_arrangements(spring_str.lstrip("."), spring_groups)
    elif spring_str[0] == "#":
        # There is at least one leading broken string
        # Check if a valid group is possible
        group_size = spring_groups[0]
        if len(spring_str) < group_size:
            # String not long enough
            return 0
        elif "." in spring_str[:group_size]:
            # Sub string contains an operational string
            return 0
        elif len(spring_str) == group_size:
            return count_arrangements("", spring_groups[1:])
        elif len(spring_str) > group_size:
            if spring_str[group_size] == "#":
                # Substring longer than group size
                return 0
            elif spring_str[group_size] == "?":
                return count_arrangements(("." + spring_str[group_size+1:]), spring_groups[1:])
            else:
                return count_arrangements(spring_str[group_size:], spring_groups[1:])
        else:
            raise RuntimeError("Unknown arrangement: ", spring_str, spring_groups)
    elif spring_str[0] == "?":
        # Test the two scenarios and add the possible combinations
        return count_arrangements(("#" + spring_str[1:]), spring_groups) + \
            count_arrangements(("." + spring_str[1:]), spring_groups)
    else:
        raise RuntimeError("Unknown arrangement: ", spring_str, spring_groups)

if __name__ == "__main__":

    input_data = aocutils.getDataInput(12)
    #input_data = test_array_1
    #input_data = test_array_2

    springs_list = parse_data(input_data)
    total_rows = len(springs_list)

    #### Part 1 ####

    counts_list = []
    for spring_str, spring_groups in springs_list:
        counts_list.append(count_arrangements(spring_str, spring_groups))
    aocutils.printResult(1, sum(counts_list))


    #### Part 2 ####

    springs_list_unfolded = unfold_data(springs_list, 5)
    counts_list = []
    for spring_str, spring_groups in springs_list_unfolded:
        counts_list.append(count_arrangements(spring_str, spring_groups))
    aocutils.printResult(2, sum(counts_list))
    



