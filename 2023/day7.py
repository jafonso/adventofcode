import aocutils
import functools

from typing import Callable

test_array = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]

def parse_data(input: str):
    return [(a[0], int(a[1])) for a in [s.split() for s in input]]

card_to_value1 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

card_to_value2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}

def translate1(cards: str):
    output = {}
    for card in cards:
        value = card_to_value1[card]
        if value not in output:
            output[value] = 1
        else:
            output[value] += 1
    return output

def translate2(cards: str):
    output = {}
    for card in cards:
        value = card_to_value2[card]
        if value not in output:
            output[value] = 1
        else:
            output[value] += 1
    if card_to_value2["J"] in output and output[card_to_value2["J"]] != 5:
        j_count = output[card_to_value2["J"]]
        del output[card_to_value2["J"]]
        best_pairs = sorted([(v, k) for k,v in output.items()], reverse=True)
        for v,k in best_pairs:
            if k != card_to_value2["J"]:
                output[k] += j_count
                break
    return output

def compare_labels1(card1: str, card2: str):
    for idx,_ in enumerate(card1):
        if card_to_value1[card1[idx]] < card_to_value1[card2[idx]]:
            return -1
        elif card_to_value1[card1[idx]] > card_to_value1[card2[idx]]:
            return 1
    return 0

def compare_labels2(card1: str, card2: str):
    for idx,_ in enumerate(card1):
        if card_to_value2[card1[idx]] < card_to_value2[card2[idx]]:
            return -1
        elif card_to_value2[card1[idx]] > card_to_value2[card2[idx]]:
            return 1
    return 0

def compare(tfunct: Callable[[str], None], lfunct: Callable[[str], None], card1: str, card2: str):
    card1_counted = tfunct(card1)
    card2_counted = tfunct(card2)
    counts1 = sorted([v for v in card1_counted.values()], reverse=True)
    counts2 = sorted([v for v in card2_counted.values()], reverse=True)
    for idx,_ in enumerate(counts1):
        if counts1[idx] < counts2[idx]:
            return -1
        elif counts1[idx] > counts2[idx]:
            return 1
    return lfunct(card1, card2)

if __name__ == "__main__":
    
    input_data = aocutils.getDataInput(7)
    #input_data = test_array

    # Part 1
    cards_bid_pairs1 = parse_data(input_data)
    cards_bid_pairs1.sort(key=functools.cmp_to_key(lambda x, y: compare(translate1, compare_labels1, x[0], y[0])))
    result_1 = sum(idx * bid for idx, (_, bid) in enumerate(cards_bid_pairs1, start=1))
    aocutils.printResult(1, result_1)

    # Part 1
    cards_bid_pairs2 = parse_data(input_data)
    cards_bid_pairs2.sort(key=functools.cmp_to_key(lambda x, y: compare(translate2, compare_labels2, x[0], y[0])))
    result_2 = sum(idx * bid for idx, (_, bid) in enumerate(cards_bid_pairs2, start=1))
    aocutils.printResult(2, result_2)