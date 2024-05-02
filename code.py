import json
import adafruit_dotstar as dotstar
import time
import gate_conversions
import data_reader


def reduce(f, arr):
    if len(arr) == 0: 
        return None 
    if len(arr) == 1: 
        return arr[0]

    if len(arr) == 2:
        return f(arr[0], arr[1])
    return reduce(f, f(arr[0], arr[1]))

logic_funcs = {
    "NAND": lambda x, y: not (x and y) ,
    "AND": lambda x, y: x and y,
    "OR": lambda x, y: x or y ,
    "XOR": lambda x,y: x ^ y 
}


# Define the number of pixels in your DotStar LED strip
NUM_PIXELS = 300

# Define the colors of the LEDs
LED_TRUE = (77, 14, 0)
LED_FALSE = (0, 0, 0)
LED_WHITE = (50, 50, 50)
LED_OFF = (0, 0, 0)

# Initialize the DotStar LED strip
dots = gate_conversions.dots


f = open("sample_board.json")  # Imports the puzzle as a json
data = json.load(f)


def light_up(leds, color):
    for led in leds:
        dots[led] = color

def setup():
    gateLEDs = []  # Array to hold the LEDs representing a logic gate
    inputLEDs = []  # Array to hold the inputLEDs for all gates

    for gate_number in data[
        "gates"
    ].items():  # Convert all the gates in the puzzle to LEDs
        gateLEDs += gate_conversions.gate_to_led(int(gate_number[0]))

    for LED in gateLEDs:
        dots[LED] = LED_WHITE  # Light up the perimeters of the gates in white

    for gate_num, gate_info in data[
        "gates"
    ].items():  # gate_info is input, output, and accepts for each gate
        if gate_info["row"] == 0:  # Row 0 is the bottom row of gates
            input_segs = gate_info["input"]
            for input_seg in input_segs:  # Convert all input_segs to LEDs
                inputLEDs += gate_conversions.segment_to_led(
                    input_seg[0], input_seg[1], input_seg[2]
                )
                for (
                    LED
                ) in inputLEDs:  # Turn the inputLEDs white to indicate they are active
                    dots[LED] = LED_WHITE
                    time.sleep(0.05)


def compute_gate(gate, mux_index, is_four_pin):

    board_data = data_reader.read_data()  # Read in all the data from the sensor boards
    print(board_data)
    gateType = data_reader.parse_gates(board_data, gate[1]["gate_index"], mux_index, is_four_pin)
    print(gateType)

    gateLEDs = []  # Convert gates to led pixels
    gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
    
    inputs = []  # Convert input segments from json to led pixels
    for input in gate[1]["input"]:
        inputs += gate_conversions.segment_to_led(input[0], input[1], input[2])

    outputs = []  # Convert output segments from json to led pixels
    for output in gate[1]["output"]:
        outputs += gate_conversions.segment_to_led(output[0], output[1], output[2])
        outputs = outputs

    if is_four_pin == 0:
        if gateType == "ON":
            light_up(outputs[1:], LED_TRUE)
            return True
        elif gateType == "OFF":
            light_up(outputs[1:], LED_FALSE)
            return False
        elif gateType is None:
            light_up(outputs[1:], LED_WHITE)
            return None
    else: # Logic gate not a switch
       
        input_gates = gate[1]["input_gate"]
        input_bools = []

        for input_gate in input_gates:
            val = bool_tree[input_gate]
            if val is None: 
                light_up(gateLEDs, LED_WHITE)
            else:
                input_bools.append(val)

        if len(input_bools) == 0:
            light_up(gateLEDs, LED_OFF)
            light_up(outputs, LED_OFF)
            return None

        if gateType is None or gateType not in gate[1]["accepts"] or len(input_bools)< len(input_gates):
            # no computation
            light_up(outputs, LED_OFF)
            light_up(gateLEDs, LED_WHITE)
            return None


        f = logic_funcs[gateType]

        if reduce(f, input_bools):
            light_up(gateLEDs, LED_TRUE)
            light_up(outputs, LED_TRUE)
            return True
        else:
            light_up(gateLEDs, LED_FALSE)
            return False
        




setup()
dots.show()
print("Done setup")

bool_tree = [None for i in data["gates"].items()]
try:
    while True:
        for gate in data["gates"].items():  # Loop through all the gates in the puzzle
            bool_tree[int(gate[0])] = compute_gate(gate, gate[1]["mux_index"], gate[1]["is_four_pin"])
        dots.show()

finally:
    dots.deinit()

# type: ignore
