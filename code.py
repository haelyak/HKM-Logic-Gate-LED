import gate_conversions
import json
import board
import board
import adafruit_dotstar as dotstar
# import RPi.GPIO as GPIO
import time


# Define the number of pixels in your DotStar LED strip
NUM_PIXELS = 300

# Initialize the DotStar LED strip
dots = gate_conversions.dots

# Set up GPIO mode
# GPIO.setmode(GPIO.BCM)

# Define GPIO pins
# D_PINS = [17, 18, 22, 23]  # Example GPIO pins for D1, D2, D3, D4

# Set up GPIO pins as inputs
# for pin in D_PINS:
    # GPIO.setup(pin, GPIO.IN)

f = open('sample_board.json') # Imports the puzzle as a json
data = json.load(f)

def setup():
    gateLEDs = [] # Array to hold the LEDs representing a logic gate
    inputLEDs = []

    for gate_number in data['gates'].items(): # Convert all the gates in the puzzle to LEDs
        gateLEDs += gate_conversions.gate_to_led(int(gate_number[0]))

    for LED in gateLEDs:
        dots[LED] = (255, 255, 255) # Light up the perimeters of the gates
    dots.show()

    for gate_num in range(0, 1):
        for json_gate in data['gates'].items():
            input_segs = json_gate[1]['input']
            for input_seg in input_segs:
                print(input_seg)
                inputLEDs += gate_conversions.segment_to_led(input_seg[0], input_seg[1], input_seg[2])
                for LED in inputLEDs:

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

def compute(gate):

    inputs = [] # Convert input segments from json to led pixels
    for input in data[gate]["input"]:
        inputs += gate_conversions.segment_to_led(input[0], input[1], input[2])

    outputs = [] # Convert output segments from json to led pixels
    for output in data[gate]["output"]:
        outputs += gate_conversions.segment_to_led(output[0], output[1], output[2])

    gateType = ["NAND", "AND", "OR", "XOR" ]

    # Read in the signal from each sensor pin
    D_states = [GPIO.input(pin) for pin in D_PINS]


    id = D_states[1] << 1 | D_states[2] # These two pins represent the type of board
                                        # Convert to a 2-digit binary number
    type = gateType[id] # Find the type of gate from the array

    if type in data[gate]["accepts"]:
        if type == "NAND":
            if all(is_pixel_lit(p) for p in inputs):
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (0, 0, 0) # Turn off perimeters of gates
                return False
            else:
                gateLEDs += gate_conversions.gate_to_led(gate)
                for LED in gateLEDs:
                    dots[LED] = (255, 0, 0) # Light up the perimeters of the gates in red
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments in red
                return True
        elif type == "AND":
            if all(is_pixel_lit(p) for p in inputs):
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
        elif type == "OR":
            if any(is_pixel_lit(p) for p in inputs):
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





setup()
# while True:
    # for gate in data: # somehow loop through all the sensor boards?
        # compute(gate)
