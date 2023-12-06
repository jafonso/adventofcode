import aocutils

test_array = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]

cubes_in_bag = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def parse_data(input: str):
    
    game, data = input.split(":")
    game_number = int(game.split()[1])

    # Separate by ;
    game_sets_str_list = data.split(";")
    # Further separate by ,
    game_sets_substr_list = [set(s.split(",")) for s in game_sets_str_list]
    # Transform substrings into maps
    game_sets_list = [{kv[1]: int(kv[0]) for kv in [kv.split() for kv in substr_set]} for substr_set in game_sets_substr_list]
    
    return game_number, game_sets_list

if __name__ == "__main__":

    input_data = aocutils.getDataInput(2)

    # Part 1
    result_1 = 0
    for data in input_data:
        game_possible = True
        game_number, game_sets_list = parse_data(data)
        for game_set in game_sets_list:
            for k, v in game_set.items():
                if v > cubes_in_bag[k]:
                    game_possible = False
                    break
            if game_possible is False:
                break
        if game_possible:
            result_1 += game_number
    aocutils.printResult(1, result_1)

    # Part 2
    result_2 = 0
    for data in input_data:
        _, game_sets_list = parse_data(data)
        max_values_set = {}
        for game_set in game_sets_list:
            for k, v in game_set.items():
                if k not in max_values_set:
                    max_values_set[k] = v
                else:
                    max_values_set[k] = max(max_values_set[k], v)
        power = 1
        for _, v in max_values_set.items():
            power *= v
        result_2 += power
    aocutils.printResult(2, result_2)
