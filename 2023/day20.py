import aocutils
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
        self.input_gates.append(None)
        idx = len(self.input_gates) - 1
        def set_input_func(input: Optional[Pulse]):
            self.input_gates[idx] = input
        return set_input_func

    def config_output_cable(self, output_module): 
        self.output_cables.append(output_module)

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

    def is_inactive(self):
        return self.value is None
    
    def get_count(self):
        return self.count_low, self.count_high

class Button(Module):

    def __init__(self, name: str):
        super().__init__(name)
        self.button_pushed = False

    def push_button(self):
        self.button_pushed = True

    def tick(self):
        if len(self.output_cables) != 1:
            raise RuntimeError("Button should have exactly 1 output")
        if self.button_pushed:
            self.output_cables[0].set_input_value(Pulse.LOW)
            self.button_pushed = False
        else:
            self.output_cables[0].set_input_value(None)

class Broadcaster(Module):

    def tick(self):
        if len(self.input_gates) != 1:
            raise RuntimeError("Broadcaster should have exactly 1 input")
        for cable in self.output_cables:
            cable.set_input_value(self.input_gates[0])

class Conjunction(Module):

    def __init__(self, name: str):
        super().__init__(name)
        self.pulse_received = False
        self.last_input_val: List[Pulse] = []

    def get_input_func(self) -> Callable[[Optional[Pulse]], None]:
        func = super().get_input_func()
        self.last_input_val.append(Pulse.LOW)
        idx = len(self.last_input_val) - 1
        def set_input_func(input: Optional[Pulse]):
            func(input)
            if input is not None:
                self.pulse_received = True
                self.last_input_val[idx] = input
        return set_input_func

    def tick(self):
        if not self.pulse_received:
            out_pulse = None
        elif all(last_input == Pulse.HIGH for last_input in self.last_input_val):
            out_pulse = Pulse.LOW 
        else:
            out_pulse = Pulse.HIGH
        for cable in self.output_cables:
            cable.set_input_value(out_pulse)
        self.pulse_received = False

class FlipFlop(Module):

    class FlipFlopState(Enum):
        ON = 1,
        OFF = 2

    def __init__(self, name: str):
        super().__init__(name)
        self.position = self.FlipFlopState.OFF

    def tick(self):
        if len(self.input_gates) == 0:
            raise RuntimeError("FlopFlop should has no inputs")
        if any(input == Pulse.LOW for input in self.input_gates):
            if self.position == self.FlipFlopState.ON:
                self.position = self.FlipFlopState.OFF
                for cable in self.output_cables:
                    cable.set_input_value(Pulse.LOW)
            else:
                self.position = self.FlipFlopState.ON
                for cable in self.output_cables:
                    cable.set_input_value(Pulse.HIGH)
        else:
            for cable in self.output_cables:
                cable.set_input_value(None) # Do not output anything

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
        else:
            if from_module_str != "broadcaster":
                raise RuntimeError(f"Unable to find type of module '{from_module_str}'")
            from_module_type = Broadcaster
            from_module = from_module_str
        to_module_list = to_module_list_str.split(", ")
        parsed_entries.append((from_module_type, from_module, to_module_list))

    # Create dictionary of modules by name
    # Add button at start
    module_dict = {}
    module_dict["button"] = Button("button")
    for parsed_entry in parsed_entries:
        module_type, module_name, _ = parsed_entry
        module_dict[module_name] = module_type(module_name)

    # Connect modules
    cables = []
    cables.append(Cable(module_dict["button"], module_dict["broadcaster"]))
    for parsed_entry in parsed_entries:
        _, module_name, to_module_name_list = parsed_entry
        for to_module_name in to_module_name_list:
            # If to_module does not exist, add a dummy one
            cables.append(Cable(module_dict[module_name], module_dict.get(to_module_name, Module(to_module_name))))

    return module_dict, cables

def tick_once(module_dict: Dict[str, Module], cables: List[Cable]):
    # Return True if there are still cables with active values
    for module in module_dict.values():
        module.tick()
    for cable in cables:
        cable.tick()
    return not all(cable.is_inactive() for cable in cables)

def print_cables(cables: List[Cable]):
    for cable in cables:
        if not cable.is_inactive():
            print(cable)

def press_button_and_run(module_dict: Dict[str, Module], cables: List[Cable], *, debug: bool=False):
    module_dict["button"].push_button()
    tick_once(module_dict, cables)
    if debug:
        print_cables(cables)
    while not all(cable.is_inactive() for cable in cables):
        tick_once(module_dict, cables)
        if debug: 
            print_cables(cables)

def press_button_n_times(module_dict: Dict[str, Module], cables: List[Cable], press_count: int):
    for _ in range(press_count):
        press_button_and_run(module_dict, cables)

def count_pulses(cables: List[Cable]):
    # Return tuple: low_pulse, high_pulse
    return tuple(sum(x) for x in zip(*(cable.get_count() for cable in cables)))

if __name__ == "__main__":

    input_data = aocutils.getDataInput(20)
    #input_data = test_array_1
    #input_data = test_array_2
    
    #### Part 1 ####

    module_dict, cables = parse_data(input_data) # Parse data for part 1

    print()
    press_button_and_run(module_dict, cables, debug=True)

    #press_button_n_times(module_dict, cables, 1000)
    #low_pulses, high_pulses = count_pulses(cables)
    #aocutils.printResult(1, low_pulses * high_pulses)

    #### Part 1 ####