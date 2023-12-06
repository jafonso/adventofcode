import aocutils

test_array = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]

def parse_data(input: str):
    
    game, data = input.split(":")
    game_number = int(game.split()[1])

    winning_set_str, betting_set_str = data.split("|")
    winning_set = {int(val) for val in winning_set_str.split()}
    betting_set = {int(val) for val in betting_set_str.split()}

    return game_number, winning_set, betting_set

if __name__ == "__main__":

    input_data = aocutils.getDataInput(4)
    #input_data = test_array

    # Part 1
    result_1 = 0
    for data in input_data:
        _, winning_set, betting_set = parse_data(data)
        winning_numbers_count = len(winning_set & betting_set)
        if winning_numbers_count > 0:
            result_1 += (2 ** (winning_numbers_count-1))
    aocutils.printResult(1, result_1)

    # Part 2
    wins_per_card = []
    for data in input_data:
        _, winning_set, betting_set = parse_data(data)
        wins_per_card.append(len(winning_set & betting_set))
    total_cards = [0] * len(wins_per_card)
    for idx, wins in enumerate(wins_per_card):
        total_cards[idx] += 1
        for j in range(wins):
            try:
                total_cards[idx + 1 + j] += total_cards[idx]
            except IndexError:
                continue
    result_2 = sum(total_cards)
    aocutils.printResult(2, result_2)