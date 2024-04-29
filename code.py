import json
import adafruit_dotstar as dotstar
import time
import gate_conversions
import data_reader


# Define the number of pixels in your DotStar LED strip
NUM_PIXELS = 300

# Initialize the DotStar LED strip
dots = gate_conversions.dots


f = open("sample_board.json")  # Imports the puzzle as a json
data = json.load(f)


def setup():
    gateLEDs = []  # Array to hold the LEDs representing a logic gate
    inputLEDs = []  # Array to hold the inputLEDs for all gates

    for gate_number in data[
        "gates"
    ].items():  # Convert all the gates in the puzzle to LEDs
        gateLEDs += gate_conversions.gate_to_led(int(gate_number[0]))

    for LED in gateLEDs:
        dots[LED] = (255, 255, 255)  # Light up the perimeters of the gates in white
    dots.show()

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
                    dots[LED] = (255, 255, 255)
                    dots.show()
                    time.sleep(0.05)


# Function to check if a pixel is lit up
def is_pixel_lit(pixel_index):
    if pixel_index < 0 or pixel_index >= NUM_PIXELS:
        return False  # Pixel index out of range

    # Check if the color of the specified pixel is not black (lit up)
    return dots[pixel_index] != (0, 0, 0)

# Function to check if a pixel is lit up
def is_pixel_red(pixel_index):
    if pixel_index < 0 or pixel_index >= NUM_PIXELS:
        return False  # Pixel index out of range

    # Check if the color of the specified pixel is not black (lit up)
    return dots[pixel_index] == (255, 0, 0)


def compute_gate(gate, mux_index, is_four_pin):
    gateLEDs = []  # Array to hold the LEDs representing a logic gate

    inputs = []  # Convert input segments from json to led pixels
    for input in gate[1]["input"]:
        inputs += gate_conversions.segment_to_led(input[0], input[1], input[2])

    outputs = []  # Convert output segments from json to led pixels
    for output in gate[1]["output"]:
        outputs += gate_conversions.segment_to_led(output[0], output[1], output[2])


    board_data = data_reader.read_data()  # Read in all the data from the sensor boards

    gateType = data_reader.parse_gates(board_data, int(gate[0]), mux_index, is_four_pin)

    # print(board_data)
    print(gateType)
    if gateType == "None":
        for LED in gateLEDs:
                    dots[LED] = (
                        255,
                        255,
                        255,
                    )  # Light up the perimeters of the gates in red for True
        for LED in outputs:
            dots[LED] = (
                        255,
                        255,
                        255,
                    )
        dots.show()

    if gateType in gate[1]["accepts"]: # If the gate excepts the puzzle piece placed on it
        if gateType == "NAND":
            if all(is_pixel_lit(p) for p in inputs):
                gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0)  # Turn off perimeters of gates for False
                return False
            else:
                gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
                for LED in gateLEDs:
                    dots[LED] = (
                        255,
                        0,
                        0,
                    )  # Light up the perimeters of the gates in red for True
                for LED in outputs:
                    dots[LED] = (
                        255,
                        0,
                        0,
                    )  # Light up the output segments in red for True
                return True
        elif gateType == "AND":
            if all(is_pixel_lit(p) for p in inputs):
                gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
                for LED in gateLEDs:
                    dots[LED] = (
                        255,
                        0,
                        0,
                    )  # Light up the perimeters of the gates in red for True
                for LED in outputs:
                    dots[LED] = (
                        255,
                        0,
                        0,
                    )  # Light up the output segments in red for True
                return True
            else:
                gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0)  # Turn off perimeters of gates for False
                return False
        elif gateType == "OR":
            if any(is_pixel_lit(p) for p in inputs):
                gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
                for LED in gateLEDs:
                    dots[LED] = (
                        255,
                        0,
                        0,
                    )  # Light up the perimeters of the gates in red for True
                for LED in outputs:
                    dots[LED] = (
                        255,
                        0,
                        0,
                    )  # Light up the output segments in red for True
                return True
            else:
                gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0)  # Turn off perimeters of gates for False
                return False
        elif gateType == "XOR":
            if sum(is_pixel_lit(p) for p in inputs) % 2 != 0:
                gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
                for LED in gateLEDs:
                    dots[LED] = (
                        255,
                        0,
                        0,
                    )  # Light up the perimeters of the gates in red for True
                for LED in outputs:
                    dots[LED] = (255, 0, 0)  # Light up the output segments in red for True
                dots.show()
                return True
            else:
                gateLEDs += gate_conversions.gate_to_led(int(gate[0]))
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0)  # Turn off perimeters of gates for False
                return False
    dots.show()


def compute_switch(switch, mux_index, is_four_pin):
    board_data = data_reader.read_data()  # Read in all the data from the sensor boards

    switchType = data_reader.parse_gates(
        board_data, int(switch[0]), mux_index, is_four_pin
    )

    outputLEDs = []  # Convert output segments from json to led pixels
    for output in switch[1]["output"]:
        outputLEDs += gate_conversions.segment_to_led(output[0], output[1], output[2])

    if switchType == "ON":
        for LED in outputLEDs:  # Turn output LEDs to red for ON
            dots[LED] = (255, 0, 0)
    else:
        for LED in outputLEDs:  # Turn output LEDs off for OFF
            dots[LED] = (0, 0, 0)


setup()
print("Done setup")
while True:
    for switch in data[
        "switches"
    ].items():  # Loop through all the switches in the puzzle
        compute_switch(switch, switch[1]["mux_index"], switch[1]["is_four_pin"])
    print("Done switches")

    for gate in data["gates"].items():  # Loop through all the gates in the puzzle
        compute_gate(gate, gate[1]["mux_index"], gate[1]["is_four_pin"])
    print("Done gates")

# type: ignore
