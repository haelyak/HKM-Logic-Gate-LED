import gate_conversions
import json
import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)
f = open('example_puzzle.json') # Imports the puzzle as a json
data = json.load(f)

def setup():
    gateLEDs = [] # Array to hold the LEDs representing a logic gate

    for gate_number in data['gates'].items(): # Convert all the gates in the puzzle to LEDs
        gateLEDs += gate_conversions.gate_to_led(int(gate_number))

    for LED in gateLEDs:
        pixels[LED] = (255, 0, 0) # Light up the perimeters of the gates

def compute(gate):
    # Detect if a gate is placed and what type of gate
    # puzzle_piece = type of gate placed




