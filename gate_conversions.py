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
        previous = sum(LEDconsts.collengths[:name]) # add up the previous cols to figure out starting LED
        ledstart = previous + segmentnum*2 # each segment has 3LEDs but overlaps with 1 LED from previous segment
        leds += [ledstart, ledstart+1, ledstart+2]
    if "row" == dir: # rows have 4 LEDs per segment
        previous = sum(LEDconsts.collengths) + sum(LEDconsts.rowlengths[:name])
        ledstart = previous + segmentnum*4
        leds += [ledstart, ledstart+1, ledstart+2, ledstart+3]
    return leds

segpercol = [2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2]
for i in range(0,len(LEDconsts.collengths)):
    for j in range(0, segpercol[i]):
        print("(", i, "col", j, ")", segment_to_led(i,"col", j))


segperrow = [2, 4, 6, 8, 10, 10, 10]
for i in range(0,len(LEDconsts.rowlengths)):
    for j in range(0, segperrow[i]):
        print("(", i, "row", j, ")", segment_to_led(i,"row", j))



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

for i in range(0, 6):
    print("gate", i, ":", gate_to_led(i))
