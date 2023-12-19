import aocutils
import re
from typing import NamedTuple, List, Tuple, Dict, Callable, Union
from enum import Enum

test_array = [
    "px{a<2006:qkq,m>2090:A,rfg}",
    "pv{a>1716:R,A}",
    "lnx{m>1548:A,A}",
    "rfg{s<537:gd,x>2440:R,A}",
    "qs{s>3448:A,lnx}",
    "qkq{x<1416:A,crn}",
    "crn{x>2662:A,R}",
    "in{s<1351:px,qqz}",
    "qqz{s>2770:qs,m<1801:hdj,R}",
    "gd{a>3333:R,R}",
    "hdj{m>838:A,pv}",
    "",
    "{x=787,m=2655,a=1222,s=2876}",
    "{x=1679,m=44,a=2067,s=496}",
    "{x=2036,m=264,a=79,s=2244}",
    "{x=2461,m=1339,a=466,s=291}",
    "{x=2127,m=1623,a=2188,s=1013}",
]

class PartRating(NamedTuple):
    # Can hold both individual values and ranges (min, max)
    x: Union[int, Tuple[int, int]]
    m: Union[int, Tuple[int, int]]
    a: Union[int, Tuple[int, int]]
    s: Union[int, Tuple[int, int]]

ratings_re = re.compile('\{x=([0-9]*),m=([0-9]*),a=([0-9]*),s=([0-9]*)\}')

def parse_part(entry: str):
    m = ratings_re.match(entry)
    if m is None:
        raise RuntimeError(f"Failed to parse entry: {entry}")
    return PartRating(x=int(m.group(1)), m=int(m.group(2)), a=int(m.group(3)), s=int(m.group(4)))

def create_rule_func(key: str, symbol: str, value: int, dest: str):
    if symbol is None:
        return lambda part: dest
    elif symbol == "<":
        return lambda part: dest if getattr(part, key) < value else None
    elif symbol == ">":
        return lambda part: dest if getattr(part, key) > value else None
    else:
        raise RuntimeError(f"Unknown symbol: {symbol}")

def parse_workflow(entry: str):
    key, remaining_raw = entry.split("{")
    remaining_raw = remaining_raw.rstrip("}")
    raw_rules_list = remaining_raw.split(",")
    rule_list = []

    for raw_rule in raw_rules_list:
        if "<" in raw_rule:
            rule_key_val, rule_dest = raw_rule.split(":")
            rule_key, rule_value = rule_key_val.split("<")
            rule_list.append(create_rule_func(rule_key, "<", int(rule_value), rule_dest))
        elif ">" in raw_rule:
            rule_key_val, rule_dest = raw_rule.split(":")
            rule_key, rule_value = rule_key_val.split(">")
            rule_list.append(create_rule_func(rule_key, ">", int(rule_value), rule_dest))
        else:
            rule_dest = raw_rule
            rule_list.append(create_rule_func(None, None, None, rule_dest))

    def func(part: PartRating):
        for f in rule_list:
            ret = f(part)
            if ret is not None:
                return ret
        raise RuntimeError(f"Reached end of rules without return")
    return key, func

def parse_data_1(input: List[str]) -> Tuple[List[PartRating], Dict[str, Callable[[PartRating], str]]]:
    ratings_list = []
    workflows = {}
    for entry in input:
        if entry == "":
            pass
        elif entry[0] == "{":
            ratings_list.append(parse_part(entry))
        else:
            w_key, w_func = parse_workflow(entry)
            workflows[w_key] = w_func

    return ratings_list, workflows

def calculate_part_score(part: PartRating):
    return part.x + part.m + part.a + part.s

def calculate_all_parts_score(part_list: List[PartRating], workflows: Dict[str, Callable[[PartRating], str]]):
    result = 0
    for part in part_list:
        wf = "in"
        while wf not in ("A", "R"):
            wf = workflows[wf](part)
        if wf == "A":
            result += calculate_part_score(part)
    return result

def split_part_range(key: str, symbol: str, value: int, part_range: PartRating):
    # Return tuple (accepted_ranges, rejected_ranges)
    # If any of those is empty, return None
    if symbol is None:
        # All ranges fit condition
        return part_range, None
    elif symbol == "<":
        curr_range_min, curr_range_max = getattr(part_range, key)
        if curr_range_max < value:
            # The full range fits the condition
            return part_range, None
        elif curr_range_min >= value:
            # The full range fails the condition
            return None, part_range
        else:
            # Only part of the range fits the condition
            new_range_1 = (curr_range_min, value - 1)
            new_range_2 = (value, curr_range_max)
            new_part_range_1 = part_range._replace(**{key: new_range_1})
            new_part_range_2 = part_range._replace(**{key: new_range_2})
            return new_part_range_1, new_part_range_2
    elif symbol == ">":
        curr_range_min, curr_range_max = getattr(part_range, key)
        if curr_range_min > value:
            # The full range fits the condition
            return part_range, None
        elif curr_range_max <= value:
            # The full range fails the condition
            return None, part_range
        else:
            # Only part of the range fits the condition
            new_range_1 = (value+1, curr_range_max)
            new_range_2 = (curr_range_min, value)
            new_part_range_1 = part_range._replace(**{key: new_range_1})
            new_part_range_2 = part_range._replace(**{key: new_range_2})
            return new_part_range_1, new_part_range_2
    else:
        raise RuntimeError(f"Unknown symbol: {symbol}")

def parse_workflow_2(entry: str):

    key, remaining_raw = entry.split("{")
    remaining_raw = remaining_raw.rstrip("}")
    raw_rules_list = remaining_raw.split(",")
    split_rule_list = []

    for raw_rule in raw_rules_list:
        if "<" in raw_rule:
            rule_key_val, rule_dest = raw_rule.split(":")
            rule_key, rule_value = rule_key_val.split("<")
            split_rule_list.append((rule_dest, lambda part_range, rule_key=rule_key, rule_value=rule_value: split_part_range(rule_key, "<", int(rule_value), part_range)))
        elif ">" in raw_rule:
            rule_key_val, rule_dest = raw_rule.split(":")
            rule_key, rule_value = rule_key_val.split(">")
            split_rule_list.append((rule_dest, lambda part_range, rule_key=rule_key, rule_value=rule_value: split_part_range(rule_key, ">", int(rule_value), part_range)))
        else:
            rule_dest = raw_rule
            split_rule_list.append((rule_dest, lambda part_range: split_part_range(None, None, None, part_range)))

    def func(part: PartRating):
        part_range_list = [part]
        processed_part_ranges = []
        for next_wf, func in split_rule_list:
            part_list_next = []
            for curr_part_range in part_range_list:
                part_range_complete, part_range_incomplete = func(curr_part_range)
                if part_range_complete:
                    processed_part_ranges.append((next_wf, part_range_complete))
                if part_range_incomplete:
                    part_list_next.append(part_range_incomplete)
            part_range_list = part_list_next
        return processed_part_ranges
    
    return key, func

def parse_data_2(input: List[str]) -> Dict[str, Callable[[PartRating], str]]:
    workflows = {}
    for entry in input:
        if entry == "":
            pass
        elif entry[0] == "{":
            pass
        else:
            w_key, w_func = parse_workflow_2(entry)
            workflows[w_key] = w_func
    return workflows

def calculate_part_combinations(part_range: PartRating):
    return \
        (part_range.x[1] - part_range.x[0] + 1) \
        * (part_range.m[1] - part_range.m[0] + 1) \
        * (part_range.a[1] - part_range.a[0] + 1) \
        * (part_range.s[1] - part_range.s[0] + 1)

def calculate_all_workflow_combinations(workflows: Dict[str, Callable[[PartRating], List[Tuple[str, PartRating]]]]):
    part_ranges = []
    accepted_part_ranges = []
    part_ranges.append(("in", PartRating(x=(1,4000), m=(1,4000), a=(1,4000), s=(1,4000))))
    while len(part_ranges) > 0:
        wf_name, part_range = part_ranges.pop()
        new_wf_part_range_list = workflows[wf_name](part_range)
        for new_wf_name, new_part_rating in new_wf_part_range_list:
            if new_wf_name == "R":
                pass
            elif new_wf_name == "A":
                accepted_part_ranges.append(new_part_rating)
            else:
                part_ranges.append((new_wf_name, new_part_rating))
    return sum(calculate_part_combinations(rating) for rating in accepted_part_ranges)

if __name__ == "__main__":

    input_data = aocutils.getDataInput(19)
    #input_data = test_array

    #### Part 1 ####

    part_list, workflows = parse_data_1(input_data)
    aocutils.printResult(1, calculate_all_parts_score(part_list, workflows))

    #### Part 2 ####

    workflows_2 = parse_data_2(input_data)
    aocutils.printResult(2, calculate_all_workflow_combinations(workflows_2))