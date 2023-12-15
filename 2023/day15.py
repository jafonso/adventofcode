import aocutils
from typing import List

test_array = [
    "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
]

def parse_data(input: str):
    return input[0].split(",")

def calculate_hash(word: str):
    aoc_hash = 0
    for c in word:
        aoc_hash += ord(c)
        aoc_hash *= 17
        aoc_hash %= 256
    return aoc_hash

def parse_command(word: str):
    if "=" in word:
        label = word.split("=")[0]
        signal = "="
        value = int(word.split("=")[1])
    elif "-" in word:
        assert "-" == word[-1] # Validate that this is the last character
        label = word.split("-")[0]
        signal = "-"
        value = None
    return label, calculate_hash(label), signal, value

def process_boxes(raw_commands_list: List[str]):
    boxes = [dict() for _ in range(256)]
    for word in raw_commands_list:
        label, label_hash, signal, value = parse_command(word)
        if signal == "=":
            # Python >= 3.6 dictionaries keep order of insertion
            # In Python 3.7 this was made part of the specification
            # Therefore, existing labels keep the order, while new labels are inserted by the end
            boxes[label_hash][label] = value      
        elif signal == "-":
            try:
                del boxes[label_hash][label]
            except KeyError:
                pass
        else:
            RuntimeError(f"Unknown signal {signal}")
    return boxes

def calculated_power(boxes_list: List[dict]):
    total_sum = 0
    for i, box in enumerate(boxes_list):
        for j, focal_value in enumerate(box.values()):
            total_sum += (i + 1) * (j + 1) * focal_value
    return total_sum

if __name__ == "__main__":

    input_data = aocutils.getDataInput(15)
    #input_data = test_array

    raw_commands_list = parse_data(input_data)

    #### Part 1 ####

    aocutils.printResult(1, sum(calculate_hash(word) for word in raw_commands_list))

    #### Part 2 ####

    boxes = process_boxes(raw_commands_list)
    aocutils.printResult(2, calculated_power(boxes))