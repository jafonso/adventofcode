import aocutils


test_array = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]

digits_map_1 = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}  

digits_map_2 = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}  

def get_first_last_digit(kv: dict, input: str):

    first = next(kv[k] for idx, _ in enumerate(input) for k in kv if input[idx:].startswith(k))
    last = next(kv[k] for idx, _ in enumerate(input) for k in kv if input[-1-idx:].startswith(k))

    return int(str(first) + str(last))

if __name__ == "__main__":
    
    input_data = aocutils.getDataInput(1)

    # Part 1
    values = [get_first_last_digit(digits_map_1, s) for s in input_data]
    result_1 = sum(values)
    aocutils.printResult(1, result_1)

    # Part 2
    values = [get_first_last_digit(digits_map_2, s) for s in input_data]
    result_2 = sum(values)
    aocutils.printResult(2, result_2)

