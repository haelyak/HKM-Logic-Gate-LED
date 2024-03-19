import LEDconsts
import Gateconsts

def segment_to_led(name, dir, segmentnum):
    ''' Converts a given segment to specific LED pixels
        name: an int representing the number of the row or column
        dir: a string either "row" or "col"
        segmentnum: an int representing which segment
    '''
    leds = [] # Array to store leds representing a segment
    
    if "col" == dir: # cols have 3 LEDs per segment
        previous = sum(LEDconsts.collengths[:name + 1]) # add up the previous cols to figure out starting LED
        ledstart = previous + segmentnum*3 # each segment has 3LEDs
        leds += [ledstart, ledstart+1, ledstart+2]
    if "row" == dir: # rows have 4 LEDs per segment
        previous = sum(LEDconsts.rowlengths[:name + 1])
        ledstart = previous + segmentnum*4
        leds += [ledstart, ledstart+1, ledstart+2, ledstart+3]
    return leds

# print(segment_to_led(1, "row", 1))

# print(segment_to_led(5, "col", 20))

def gate_to_led(gate):
    """ Converts a given gate to specific LED pixels
        gate: an int representing a specific gate
        gates are numbered left to right, bottom to top
    """
    leds = [] # Array to store the leds representing a gate
    segs = Gateconsts.gateSegs[gate] # The segments that represent a gate (hardcoded)
    for seg in segs: 
        leds+= segment_to_led(seg[0], seg[1], seg[2]) # Segments are arrays with name, dir, segmentnum
    return leds

print(gate_to_led(1))
