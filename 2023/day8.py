import re
import math
import itertools
import aocutils


test_array_1 = [
    "RL",
    "",
    "AAA = (BBB, CCC)",
    "BBB = (DDD, EEE)",
    "CCC = (ZZZ, GGG)",
    "DDD = (DDD, DDD)",
    "EEE = (EEE, EEE)",
    "GGG = (GGG, GGG)",
    "ZZZ = (ZZZ, ZZZ)",
]

test_array_2 = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)",
]

test_array_3 = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)",
]

def parse_data(input: str):
    p  = re.compile('([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)')
    instructions = input[0]
    map_s = input[2:]
    map = {}
    for node in map_s:
        m = p.match(node)
        map[m.group(1)] = (m.group(2), m.group(3))
    return instructions, map

if __name__ == "__main__":
    
    input_data = aocutils.getDataInput(8)
    #input_data = test_array_1
    #input_data = test_array_2

    instructions, map = parse_data(input_data)
    
    # Part 1

    next_node = "AAA"
    next_step_iter_1 = itertools.cycle(instructions)
    count_1 = 0
    while next_node != "ZZZ":
        next_step = next(next_step_iter_1)
        next_node = map[next_node][0 if next_step == "L" else 1]
        count_1 += 1
    aocutils.printResult(1, count_1)

    #input_data = test_array_3
    #instructions, map = parse_data(input_data)

    # Part 2

    next_node_list = [n for n in map if n[2] == "A"]
    loop_size_list = [None for n in next_node_list]
    visited_node_dict_list = [dict() for n in next_node_list]
    next_step_iter_2 = itertools.cycle(instructions)
    count_2 = 0
    # Add initial visited nodes to set list
    for i,n in enumerate(next_node_list):
        visited_node_dict_list[i][n] = 0
    # Iterate
    while not all([l is not None for l in loop_size_list]):
        next_step = next(next_step_iter_2)
        next_node_list = [map[n][0 if next_step == "L" else 1] for n in next_node_list]
        count_2 += 1
        for i,n in enumerate(next_node_list):
            if loop_size_list[i] is not None:
                continue
            if n in visited_node_dict_list[i] and n[2] == 'Z':
                if (count_2 - visited_node_dict_list[i][n]) != visited_node_dict_list[i][n]:
                    print("Least common multiple not possible. Offset required.")
                    print(loop_size_list)
                    exit(1)
                loop_size_list[i] = count_2 - visited_node_dict_list[i][n]
            else:
                visited_node_dict_list[i][n] = count_2
    aocutils.printResult(2, math.lcm(*loop_size_list))