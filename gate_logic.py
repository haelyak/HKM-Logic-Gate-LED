import gate_conversions
import json
import board
import neopixel
import board
import adafruit_dotstar as dotstar

# Define the number of pixels in your DotStar LED strip
NUM_PIXELS = 30

# Initialize the DotStar LED strip
dots = dotstar.DotStar(board.SCK, board.MOSI, NUM_PIXELS, brightness=0.5)

f = open('example_puzzle.json') # Imports the puzzle as a json
data = json.load(f)

def setup():
    gateLEDs = [] # Array to hold the LEDs representing a logic gate

    for gate_number in data['gates'].items(): # Convert all the gates in the puzzle to LEDs
        gateLEDs += gate_conversions.gate_to_led(int(gate_number))

    for LED in gateLEDs:
        dots[LED] = (255, 0, 0) # Light up the perimeters of the gates

def compute(gate):

    inputs = []
    for input in data[gate]["input"]:
        inputs += gate_conversions.segment_to_led(input[0], input[1], input[2])
    
    outputs = []
    for output in data[gate]["output"]:
        outputs += gate_conversions.segment_to_led(output[0], output[1], output[2])

    gateType = ["NAND", "AND", "OR", "XOR" ]
    
    D1 = digitalRead(A0)
    D2 = digitalRead(A1)
    D3 = digitalRead(A2)
    D4 = digitalRead(A3)
    
    data = D1 << 3 | D2 << 2 | D3 << 1 | D4
    id = D2 << 1 | D3
    type = gateType[id]

    if type in data[gate]["accepts"]:
        if type == "NAND":
            if is_pixel_lit(inputs[0]) and is_pixel_lit(inputs[:-1]):
                return False
            else:
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments
                return True
        if type == "AND":
            if is_pixel_lit(inputs[0]) and is_pixel_lit(inputs[:-1]):
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments
                return True
            else:
                return False
        if type == "OR":
            if is_pixel_lit(inputs[0]) or is_pixel_lit(inputs[:-1]):
                return False
            else:
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments
                return True
        if type == "XOR":
            if is_pixel_lit(inputs[0]) != is_pixel_lit(inputs[:-1]):
                return False
            else:
                for LED in outputs:
                    dots[LED] = (255, 0, 0) # Light up the output segments
                return True



# Function to check if a pixel is lit up
def is_pixel_lit(pixel_index):
    if pixel_index < 0 or pixel_index >= NUM_PIXELS:
        return False  # Pixel index out of range
    
    # Check if the color of the specified pixel is not black (lit up)
    return dots[pixel_index] != (0, 0, 0)


