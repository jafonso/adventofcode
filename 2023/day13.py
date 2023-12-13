import aocutils
from typing import List

test_array = [
    "#.##..##.",
    "..#.##.#.",
    "##......#",
    "##......#",
    "..#.##.#.",
    "..##..##.",
    "#.#.##.#.",
    "",
    "#...##..#",
    "#....#..#",
    "..##..###",
    "#####.##.",
    "#####.##.",
    "..##..###",
    "#....#..#",
]

class NotFoundError(Exception):
    pass

def parse_data(input: str):
    patterns = []
    last_p_start = 0
    for idx, row in enumerate(input):
        if row == "":
            patterns.append(input[last_p_start:idx])
            last_p_start = idx + 1
    else:
        if idx > last_p_start:
            patterns.append(input[last_p_start:])
    return patterns

def is_mirror_on(pattern: List[str], row_nr: int):
    half_1 = pattern[:row_nr]
    half_2 = pattern[row_nr:]
    half_1.reverse()
    common_len = min(len(half_1), len(half_2))
    return half_1[:common_len] == half_2[:common_len]

def differences_between_rows(row_1: str, row_2: str):
    return sum([0 if a == b else 1 for a,b in zip(row_1, row_2)])

def is_smudged_mirror_on(pattern: List[str], row_nr: int):
    half_1 = pattern[:row_nr]
    half_2 = pattern[row_nr:]
    half_1.reverse()
    common_len = min(len(half_1), len(half_2))
    return sum([differences_between_rows(row_1, row_2) for row_1, row_2 in zip(half_1[:common_len], half_2[:common_len])]) == 1

def find_mirror(pattern: List[str], is_smudged: bool):
    func = is_smudged_mirror_on if is_smudged else is_mirror_on
    for i in range(1, len(pattern)):
        if func(pattern, i):
            return i
    raise NotFoundError("No mirror found")

def find_mirror_horizontal(pattern: List[str], is_smudged: bool):
    return find_mirror(pattern, is_smudged)

def find_mirror_vertical(pattern: List[str], is_smudged: bool):
    return find_mirror(["".join(s) for s in zip(*pattern)], is_smudged)

if __name__ == "__main__":

    input_data = aocutils.getDataInput(13)
    #input_data = test_array

    patterns_list = parse_data(input_data)
    
    #### Part 1 ####

    result_1 = 0
    for pattern in patterns_list:
        try:
            result_1 += (100 * find_mirror_horizontal(pattern, False))
        except NotFoundError:
            result_1 += find_mirror_vertical(pattern, False)
    aocutils.printResult(1, result_1)

    #### Part 2 ####

    result_2 = 0
    for pattern in patterns_list:
        try:
            result_2 += (100 * find_mirror_horizontal(pattern, True))
        except NotFoundError:
            result_2 += find_mirror_vertical(pattern, True)
    aocutils.printResult(2, result_2)
