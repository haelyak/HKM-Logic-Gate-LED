import json
import board
import adafruit_dotstar as dotstar
# import RPi.GPIO as GPIO
import time
import gate_conversions
import data_reader


# Define the number of pixels in your DotStar LED strip
NUM_PIXELS = 300

# Initialize the DotStar LED strip
dots = gate_conversions.dots


f = open('sample_board.json') # Imports the puzzle as a json
data = json.load(f)

def setup():
    gateLEDs = [] # Array to hold the LEDs representing a logic gate
    inputLEDs = [] # Array to hold the inputLEDs for all gates

    for gate_number in data['gates'].items(): # Convert all the gates in the puzzle to LEDs
        gateLEDs += gate_conversions.gate_to_led(int(gate_number[0]))

    for LED in gateLEDs:
        dots[LED] = (255, 255, 255) # Light up the perimeters of the gates in white
    dots.show()
        
    for gate_num, gate_info in data['gates'].items(): # gate_info is input, output, and accepts for each gate
        if gate_info['row'] == 0: # Row 0 is the bottom most row
            input_segs = gate_info['input']
            for input_seg in input_segs: # Convert all input_segs to LEDs
                inputLEDs += gate_conversions.segment_to_led(input_seg[0], input_seg[1], input_seg[2])
                for LED in inputLEDs: # Turn the inputLEDs white to indicate they are active
                    dots[LED] = (255, 255, 255)
                    dots.show()
                    time.sleep(0.05)
                print(inputLEDs)




# Function to check if a pixel is lit up
def is_pixel_lit(pixel_index):
    if pixel_index < 0 or pixel_index >= NUM_PIXELS:
        return False  # Pixel index out of range

    # Check if the color of the specified pixel is not black (lit up)
    return dots[pixel_index] != (0, 0, 0)

def compute_gate(gate, mux_index, is_four_pin):
    gateLEDs = [] # Array to hold the LEDs representing a logic gate

    inputs = [] # Convert input segments from json to led pixels
    for input in data[gate]["input"]:
        inputs += gate_conversions.segment_to_led(input[0], input[1], input[2])

    outputs = [] # Convert output segments from json to led pixels
    for output in data[gate]["output"]:
        outputs += gate_conversions.segment_to_led(output[0], output[1], output[2])

    gateType = ["NAND", "AND", "OR", "XOR" ]

    board_data = data_reader.read_data() # Read in all the data from the sensor boards

    gateType = data_reader.parse_gates(board_data, gate, mux_index, is_four_pin)
    
    if type in data[gate]["accepts"]:
        if type == "NAND":
            if all(is_pixel_lit(p) for p in inputs):
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0) # Turn off perimeters of gates for False
                return False
            else:
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (255, 0, 0) # Light up the perimeters of the gates in red for True
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments in red for True
                return True
        elif type == "AND":
            if all(is_pixel_lit(p) for p in inputs):
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (255, 0, 0) # Light up the perimeters of the gates in red for True
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments in red for True
                return True
            else:
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0) # Turn off perimeters of gates for False
                return False
        elif type == "OR":
            if any(is_pixel_lit(p) for p in inputs):
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (255, 0, 0) # Light up the perimeters of the gates in red for True
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments in red for True
                return True
            else:
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0) # Turn off perimeters of gates for False
                return False
        elif type == "XOR":
            if sum(is_pixel_lit(p) for p in inputs) % 2 != 0:
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (255, 0, 0) # Light up the perimeters of the gates in red
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments
                return True
            else:
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0) # Turn off perimeters of gates
                return False

def compute_switch(switch, mux_index, is_four_pin):
    board_data = data_reader.read_data() # Read in all the data from the sensor boards
    
    switchType = data_reader.parse_gates(board_data, switch, mux_index, is_four_pin)

    outputLEDs = [] # Convert input segments from json to led pixels
    for output in data[switch]["input"]:
        outputLEDs += gate_conversions.segment_to_led(output[0], output[1], output[2])

    if switchType == "ON":
        for LED in outputLEDs: # Turn output LEDs to red for ON
            dots[LED] = (255, 0, 0) 
    else:
        for LED in outputLEDs: # Turn output LEDs off for OFF
            dots[LED] = (0, 0, 0) 



setup()
while True:
    for switch in data['switches'].items(): # Loop through all the switches in the puzzle
        compute_gate(gate, gate["mux_index"], gate["is_four_pin"]) 
        
    for gate in data['gates'].items(): # Loop through all the gates in the puzzle
        compute_gate(gate, gate["mux_index"], gate["is_four_pin"]) 
    
