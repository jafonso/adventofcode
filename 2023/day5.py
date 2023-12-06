import aocutils
import bisect
from typing import NamedTuple

test_array = [
    "seeds: 79 14 55 13"
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4",
]

class MappingType(NamedTuple):
    val_from_min: int
    val_from_max: int
    offset: int

class SmartMap:

    HUGE_INT = 10**100

    def __init__(self) -> None:
        self.mappings = []
        self.starting_values = []
        self.starting_values_dirty = False
        

    def insert_range(self, value_to, value_from, lenght):
        self.mappings.append(MappingType(value_from, value_from + lenght - 1, value_to - value_from))
        self.mappings.sort(key=lambda x: x.val_from_min)
        self.starting_values_dirty = True

    def map(self, value):
        idx = bisect.bisect_right([x.val_from_min for x in self.mappings], value) - 1
        if idx < 0:
            return value
        mapping = self.mappings[idx]
        if value > mapping.val_from_max:
            return value
        else:
            return value + mapping.offset
        
    def get_mapping_values(self):
        if not self.starting_values_dirty:
            return self.starting_values
        
        # Otherwise, clear and restart
        self.starting_values = []
        current_value = 0
        for x in self.mappings:
            if current_value < x.val_from_min:
                self.starting_values.append(MappingType(current_value, x.val_from_min-1, 0))
                current_value = x.val_from_min
            self.starting_values.append(x)
            current_value = x.val_from_max + 1
        # Add range after all maps
        self.starting_values.append(MappingType(current_value, SmartMap.HUGE_INT, 0))
        self.starting_values_dirty = False
        return self.starting_values
    
    def map_range(self, value_min, value_max):
        return_tuples = [] # Each tupple contains a min and max value

        starting_values = self.get_mapping_values()
        for mapping in starting_values:
            if value_min > mapping.val_from_max:
                continue # Nothing to get here
            iter_min = value_min + mapping.offset
            iter_max = mapping.val_from_max + mapping.offset if value_max > mapping.val_from_max else value_max + mapping.offset
            return_tuples.append((iter_min, iter_max))
            if value_max <= mapping.val_from_max:
                break # No more tuples to get
            else:
                value_min = mapping.val_from_max + 1

        return return_tuples
    
    def __str__(self):
        return str(self.mappings)
    
    def __repr__(self):
        return self.__str__()
    
def parse_data(input: str):

    # Define seed as seeds
    seeds = list()
    op_map = dict()
    map_map = dict()
    last_map = None
    for row in input:
        if "seeds" in row:
            _, seeds_str =  row.split(":")
            seeds = [int(v) for v in seeds_str.split()]
        elif "map" in row:
            str_from, _, str_to = row.split()[0].split("-")
            op_map[str_from] = str_to
            last_map = SmartMap()
            map_map[str_from] = last_map
        elif len(row.split()) == 3:
            val_to, val_from, lenght = [int(v) for v in row.split()]
            last_map.insert_range(val_to, val_from, lenght)
        elif len(row) == 0:
            last_map = None
        else:
            RuntimeError("Unable to parse row: " + row)
    return seeds, op_map, map_map

def parse_data_range(input: str):
    seeds, op_map, map_map = parse_data(input)
    seed_ranges = [(seeds[i], seeds[i] + seeds[i+1] - 1) for i in range(0, len(seeds), 2)]
    return seed_ranges, op_map, map_map

if __name__ == "__main__":

    input_data = aocutils.getDataInput(5)
    #input_data = test_array

    # Part 1
    result_1 = 0
    seeds, op_map, map_map = parse_data(input_data)
    min_locations_1 = set()
    for seed in seeds:
        str_iter = "seed"
        value_iter = seed
        while (str_iter in op_map):
            smart_map_obj = map_map[str_iter]
            value_iter = smart_map_obj.map(value_iter)
            str_iter = op_map[str_iter]
        min_locations_1.add(value_iter)
    result_1 = min(min_locations_1)
    aocutils.printResult(1, result_1)

    # Part 2
    result_2 = 0
    seed_ranges, op_map, map_map = parse_data_range(input_data)
    min_locations_2 = set()
    for seed_range in seed_ranges:
        str_iter = "seed"
        value_iter = [seed_range,]
        while (str_iter in op_map):
            smart_map_obj = map_map[str_iter]
            next_iter = []
            for v in value_iter:
                next_iter.extend(smart_map_obj.map_range(v[0], v[1]))
            value_iter = next_iter
            str_iter = op_map[str_iter]
        min_locations_2.add(min([min for min,max in value_iter]))
    result_2 = min(min_locations_2)
    aocutils.printResult(2, result_2)
        
                
