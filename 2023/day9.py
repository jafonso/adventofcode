import aocutils
from typing import List

test_array = [
    "0 3 6 9 12 15",
    "1 3 6 10 15 21",
    "10 13 16 21 30 45",
]

def parse_data(input: str):
    return [[int(v) for v in s.split()] for s in input]

def prev_next_value(sequence: List[int]):
    if all(v == 0 for v in sequence):
        return (0, 0)
    else:
        prev_value_below, next_value_below = prev_next_value([j-i for i, j in zip(sequence[:-1], sequence[1:])])
        return (sequence[0] - prev_value_below, sequence[-1] + next_value_below)

if __name__ == "__main__":
    
    input_data = aocutils.getDataInput(9)
    #input_data = test_array

    sequences = parse_data(input_data)

    results_list = [prev_next_value(seq) for seq in sequences]
    result_2_list, result_1_list = zip(*results_list)
    aocutils.printResult(1, sum(result_1_list))
    aocutils.printResult(1, sum(result_2_list))