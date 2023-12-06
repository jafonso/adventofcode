import aocutils

test_array = [
    "Time:      7  15   30",
    "Distance:  9  40  200",
]

def parse_data_1(input: str):
    time_values_str = input[0].split(":")[1].split()
    dist_values_str = input[1].split(":")[1].split()
    time_values = [int(s) for s in time_values_str]
    dist_values = [int(s) for s in dist_values_str]
    return list(zip(time_values, dist_values))

def parse_data_2(input: str):
    time_value_str = input[0].split(":")[1].replace(" ", "")
    dist_value_str = input[1].split(":")[1].replace(" ", "")
    time_values = int(time_value_str)
    dist_values = int(dist_value_str)
    return (time_values, dist_values)

def travel_dist_calculator(charge_time, total_time):
    remaining_time = total_time - charge_time
    speed = charge_time
    return remaining_time * speed

if __name__ == "__main__":

    input_data = aocutils.getDataInput(6)
    #input_data = test_array

    # Part 1
    data_pairs_1 = parse_data_1(input_data)

    total_mult = 1
    for i, (time, dist) in enumerate(data_pairs_1):
        count_wins = 0
        for t in range(time+1):
            travel_dist = travel_dist_calculator(t, time)
            if travel_dist > dist:
                count_wins += 1
        total_mult *= count_wins
    aocutils.printResult(1, total_mult)

    # Part 2
    # TODO: This can be achieved much faster with bissection

    data_pairs_2 = parse_data_2(input_data)
    time, dist = data_pairs_2

    count_wins = 0
    for t in range(time+1):
        travel_dist = travel_dist_calculator(t, time)
        if travel_dist > dist:
            count_wins += 1
    aocutils.printResult(2, count_wins)