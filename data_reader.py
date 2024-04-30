import board
import time
import digitalio

INPUT = digitalio.Direction.INPUT
OUTPUT = digitalio.Direction.OUTPUT

# data selection pins
DS_0 = digitalio.DigitalInOut(board.D9)
DS_0.direction = OUTPUT
DS_1 = digitalio.DigitalInOut(board.D10)
DS_1.direction = OUTPUT
DS_2 = digitalio.DigitalInOut(board.D11)
DS_2.direction = OUTPUT
DS_3 = digitalio.DigitalInOut(board.D12)
DS_3.direction = OUTPUT

#data input pins

DATA_0 = digitalio.DigitalInOut(board.A0)
DATA_0.direction = INPUT
DATA_1 = digitalio.DigitalInOut(board.A1)
DATA_1.direction = INPUT

def read_data():
    data = [False for i in range(32)]
    for i in range(16):
        n = i
        DS_0.value = bool(n % 2)

        n >>= 1
        DS_1.value = bool(n % 2)

        n >>= 1
        DS_2.value = bool(n % 2)

        n >>= 1
        DS_3.value = bool(n % 2)

        time.sleep(0.001) # wait 1ms

        data[i] = DATA_0.value
        data[16+i] = DATA_1.value

    return data


GATES = {
    (1,0,0,1): "NAND",
    (1,0,1,1): "OR",
    (1,1,0,1): "AND",
    (1,1,1,1): "XOR",
    (0,1): "OFF",
    (1,1): "ON",

    # invalid data because no contact
    (0,0,0,0): None,
    (0,0,1,0): None,
    (0,1,0,0): None,
    (0,1,1,0): None,
    (1,0,0,0): None,
    (1,0,1,0): None,
    (1,1,0,0): None,
    (1,1,1,0): None,
    (0,0,0,1): None,
    (0,0,1,1): None,
    (0,1,0,1): None,
    (0,1,1,1): None,
    (0,0): None,
    (1,0): None
}

def parse_gates(data, gate_index, mux_index, is_four_pin):
    inc = 4 if is_four_pin else 2

    # print(gate_index)
    # print(mux_index)
    # print(inc)
    # print(mux_index*16+gate_index*inc)
    # print(mux_index*16+gate_index*inc+inc)
      
    # print(tuple(data[mux_index*16+gate_index*inc:mux_index*16+gate_index*inc+inc] ))

    return GATES[tuple(data[mux_index*16+gate_index*inc:mux_index*16+gate_index*inc+inc] )]
