import aocutils
import collections
import operator
from functools import reduce
from enum import Enum
from typing import Optional, Callable, List, Dict, Tuple

test_array_1 = [
    "broadcaster -> a, b, c",
    "%a -> b",
    "%b -> c",
    "%c -> inv",
    "&inv -> a",
]

test_array_2 = [
    "broadcaster -> a",
    "%a -> inv, con",
    "&inv -> b",
    "%b -> con",
    "&con -> output",
]

class Pulse(Enum):
    LOW = 1,
    HIGH = 2

class Module:
    
    def __init__(self, name: str):
        self.input_gates: List[Pulse] = []
        self.output_cables: List[Cable] = []
        self.name = name
    
    def get_input_func(self) -> Callable[[Optional[Pulse]], None]:
        raise NotImplemented() 

    def config_output_cable(self, output_cable): 
        self.output_cables.append(output_cable)

    def tick(self):
        raise NotImplemented()

class Cable:
    
    def __init__(self, from_module: Module, to_module: Module):
        self.value = None
        self.from_module = from_module
        self.to_module = to_module
        self.count_low = 0
        self.count_high = 0
        self.to_module_gate_func = to_module.get_input_func()
        self.from_module.config_output_cable(self)

    def __str__(self) -> str:
        if self.value == Pulse.LOW:
            value_str = "-low->"
        elif self.value == Pulse.HIGH:
            value_str = "-high->"
        else:
            value_str = "- / ->"
        return f"{self.from_module.name} {value_str} {self.to_module.name}"

    def set_input_value(self, value):
        self.value = value
    
    def tick(self):
        if self.value == Pulse.LOW:
            self.count_low += 1
        elif self.value == Pulse.HIGH:
            self.count_high += 1
        self.to_module_gate_func(self.value)
        return self.to_module

    def is_inactive(self):
        return self.value is None
    
    def get_count(self):
        return self.count_low, self.count_high

class RX(Module):
    
    def __init__(self, name: str):
        super().__init__(name)
        self.low_pulse = False

    def get_input_func(self) -> Callable[[Optional[Pulse]], None]:
        def set_input_func(input: Pulse):
            if input == Pulse.LOW:
                self.low_pulse = True
            else:
                self.low_pulse = False
        return set_input_func
    
    def config_output_cable(self, output_cable): 
        raise RuntimeError("RX module can't have an output cable")
    
    def low_pulse_received(self):
        return self.low_pulse
    
    def tick(self):
        return []

class Button(Module):

    def __init__(self, name: str):
        super().__init__(name)
        self.button_pushed = False

    def push_button(self):
        self.button_pushed = True

    def get_input_func(self) -> Callable[[Optional[Pulse]], None]:
        raise RuntimeError("Button should not have an input cable") 

    def tick(self):
        if len(self.output_cables) != 1:
            raise RuntimeError("Button should have exactly 1 output")
        if self.button_pushed:
            self.output_cables[0].set_input_value(Pulse.LOW)
            self.button_pushed = False
            return self.output_cables
        else:
            self.output_cables[0].set_input_value(None)
            return []

class Broadcaster(Module):

    def __init__(self, name: str):
        super().__init__(name)
        self.input_gate = None

    def get_input_func(self) -> Callable[[Optional[Pulse]], None]:
        if self.input_gate:
            raise RuntimeError("Input of broadcaster already set")
        def set_input_func(input: Pulse):
            self.input_gate = input
        return set_input_func

    def tick(self):
        for cable in self.output_cables:
            cable.set_input_value(self.input_gate)
        return self.output_cables

class Conjunction(Module):

    def __init__(self, name: str):
        super().__init__(name)
        self.last_input_val: List[Pulse] = []

    def get_input_func(self) -> Callable[[Optional[Pulse]], None]:
        self.last_input_val.append(Pulse.LOW)
        idx = len(self.last_input_val) - 1
        def set_input_func(input: Pulse):
            self.last_input_val[idx] = input
        return set_input_func

    def tick(self):
        if all(last_input == Pulse.HIGH for last_input in self.last_input_val):
            out_pulse = Pulse.LOW
        else:
            out_pulse = Pulse.HIGH
        for cable in self.output_cables:
            cable.set_input_value(out_pulse)
        return self.output_cables

class FlipFlop(Module):

    class FlipFlopState(Enum):
        ON = 1,
        OFF = 2

    def __init__(self, name: str):
        super().__init__(name)
        self.last_input: Pulse = None
        self.position = self.FlipFlopState.OFF

    def get_input_func(self) -> Callable[[Optional[Pulse]], None]:
        def set_input_func(input: Pulse):
            self.last_input = input
        return set_input_func

    def tick(self):
        if self.input_gates is None:
            raise RuntimeError("FlopFlop should has no input")
        if self.last_input == Pulse.LOW:
            if self.position == self.FlipFlopState.ON:
                self.position = self.FlipFlopState.OFF
                for cable in self.output_cables:
                    cable.set_input_value(Pulse.LOW)
            else:
                self.position = self.FlipFlopState.ON
                for cable in self.output_cables:
                    cable.set_input_value(Pulse.HIGH)
            return self.output_cables
        else:
            return []

def parse_data(input: List[str]) -> Tuple[Dict[str, Module], List[Cable]]:
    parsed_entries = []
    for entry in input:
        from_module_str, to_module_list_str = entry.split(" -> ")
        if from_module_str[0] == "%":
            from_module_type = FlipFlop
            from_module = from_module_str[1:]
        elif from_module_str[0] == "&":
            from_module_type = Conjunction
            from_module = from_module_str[1:]
        elif from_module_str == "broadcaster":
            from_module_type = Broadcaster
            from_module = from_module_str
        else:
            raise RuntimeError(f"Unable to parse module '{from_module_str}'")
            
        to_module_list = to_module_list_str.split(", ")
        parsed_entries.append((from_module_type, from_module, to_module_list))

    # Create dictionary of modules by name
    # Add button at start
    module_dict = {}
    module_dict["button"] = Button("button")
    for parsed_entry in parsed_entries:
        module_type, module_name, _ = parsed_entry
        module_dict[module_name] = module_type(module_name)
    module_dict["rx"] = RX("rx")

    # Connect modules
    cables = []
    cables.append(Cable(module_dict["button"], module_dict["broadcaster"]))
    for parsed_entry in parsed_entries:
        _, module_name, to_module_name_list = parsed_entry
        for to_module_name in to_module_name_list:
            # If to_module does not exist, add a dummy one
            cables.append(Cable(module_dict[module_name], module_dict[to_module_name]))

    return module_dict, cables

def press_button_and_run(module_dict: Dict[str, Module], *, debug: bool=False):
    
    next_cables_to_process = collections.deque()

    module_dict["button"].push_button()
    next_cables_to_process.extend(module_dict["button"].tick())

    while next_cables_to_process:
        next_cable = next_cables_to_process.popleft()
        if next_cable.is_inactive():
            raise RuntimeError("Cable is inactive")
        next_module = next_cable.tick()
        if debug:
            print(next_cable)
        next_cables_to_process.extend(next_module.tick())

def press_button_n_times(module_dict: Dict[str, Module], press_count: int, *, debug: bool=False):
    for _ in range(press_count):
        press_button_and_run(module_dict, debug=debug)
        if debug:
            print("################################")

def count_pulses(cables: List[Cable]):
    # Return tuple: low_pulse, high_pulse
    return tuple(sum(x) for x in zip(*(cable.get_count() for cable in cables)))

def order_by_low_pulses(cables: List[Cable]):
    output = []
    for cable in cables:
        output.append((cable.count_low, cable.count_high, cable))
    output.sort(key=lambda x: (x[0], x[1]))
    for out in output:
        low_pulses, high_pulses, cable = out
        print(f"{cable.from_module.name} --> {cable.to_module.name}: L: {low_pulses} H: {high_pulses}")

def probe_high_count(module: Module):
    return module.output_cables[0].count_high

if __name__ == "__main__":

    input_data = aocutils.getDataInput(20)
    #input_data = test_array_1
    #input_data = test_array_2
    
    #### Part 1 ####

    module_dict, cables = parse_data(input_data) # Parse data for part 1

    press_button_n_times(module_dict, 1000, debug=False)
    low_pulses, high_pulses = count_pulses(cables)
    aocutils.printResult(1, low_pulses * high_pulses)

    #### Part 2 ####

    module_dict, cables = parse_data(input_data) # Parse data again for part 2

    # These are all the modules that appear before the end module 'rx'.
    # For 'rx' to be LOW, all of these need to be HIGH at the same time.
    # They are cyclic, therefore we only need to find the minimum common multiple of the first occurrence
    # of a HIGH on each one of them.
    first_high_occurence_on = {
        module_dict["qn"]: None,
        module_dict["xf"]: None,
        module_dict["zl"]: None,
        module_dict["xn"]: None,
    }

    count = 0
    while True:
        count += 1
        press_button_n_times(module_dict, 1, debug=False)
        for module, value in first_high_occurence_on.items():
            if not value and probe_high_count(module) > 0:
                first_high_occurence_on[module] = count
        if all(val != None for val in first_high_occurence_on.values()):
            break

    aocutils.printResult(2, reduce(operator.mul, first_high_occurence_on.values(), 1))