import LEDconsts
import Gateconsts
import board
import adafruit_dotstar
import time
import busio
import digitalio


num_pixels = 300
dots = adafruit_dotstar.DotStar(board.A4, board.A5, num_pixels, brightness=0.05, auto_write=False)


def is_hardware_spi(clock_pin, data_pin):
    try:
        p = busio.SPI(clock_pin, data_pin)
        p.deinit()
        return True
    except ValueError:
        return False


# Provide the two pins you intend to use.
# if is_hardware_spi(board.A4, board.A5):
    # print("This pin combination is hardware SPI!")
# else:
    # print("This pin combination isn't hardware SPI.")


def segment_to_led(name, dir, segmentnum):
    ''' Converts a given segment to specific LED dots
        name: an int representing the number of the row or column
        dir: a string either "row" or "col"
        segmentnum: an int representing which segment
    '''
    leds = [] # Array to store leds representing a segment

    if "col" == dir: # cols have 3 LEDs per segment
        previous = sum(LEDconsts.rowlengths) + sum(LEDconsts.collengths[:name]) # add up the previous cols to figure out starting LED
        ledstart = previous + segmentnum*2 # each segment has 3LEDs but overlaps with 1 LED from previous segment
        leds += [ledstart, ledstart+1, ledstart+2]
    if "row" == dir: # rows have 4 LEDs per segment
        previous =  sum(LEDconsts.rowlengths[:name])
        ledstart = previous + segmentnum*3
        leds += [ledstart, ledstart+1, ledstart+2, ledstart+3]
    return leds


# for i in range(0,len(LEDconsts.collengths)):
    #for j in range(0, LEDconsts.segpercol[i]):
        #print("(", i, "col", j, ")", segment_to_led(i,"col", j))
        #for led in segment_to_led(i,"col", j):
            #dots[led] = (255, 0, 0)
            #dots.show()
        #time.sleep(1)


#for i in range(0,len(LEDconsts.rowlengths)):
    #for j in range(0, LEDconsts.segperrow[i]):
        #print("(", i, "row", j, ")", segment_to_led(i,"row", j))
        #for leds in segment_to_led(i,"row", j):
            #dots[leds] = (255, 0, 0)
            #dots.show()
        #time.sleep(1)


def gate_to_led(gate):
    """ Converts a given gate to specific LED dots
        gate: an int representing a specific gate
        gates are numbered left to right, bottom to top
    """
    leds = [] # Array to store the leds representing a gate
    segs = Gateconsts.gateSegs[gate] # The segments that represent a gate (hardcoded)
    for seg in segs:
        leds+= segment_to_led(seg[0], seg[1], seg[2]) # Segments are arrays with name, dir, segmentnum
    return leds

# for i in range(0, 3):
    # print("gate", i, ":", gate_to_led(i))
    # for leds in gate_to_led(i):
        # dots[leds] = (255, 0, 0)
    # dots.show()
    # time.sleep(1)
