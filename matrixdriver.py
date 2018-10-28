import sys
sys.path.append("./lib")

import i2c_lib
from time import *

# LCD Address
ADDRESS_MATRIX = 0x3C

MATRIX_FULLINPUT = 0b11111111
MATRIX_CHECKKEY  = 0b01111000
MATRIX_COL3      = 0b01111110
MATRIX_COL2      = 0b01111101
MATRIX_COL1      = 0b01111011
MATRIX_LINE4     = 0b00001000
MATRIX_LINE3     = 0b00010000
MATRIX_LINE2     = 0b00100000
MATRIX_LINE1     = 0b01000000



class matrix:
    def __init__(self):
        self.matrix_device = i2c_lib.i2c_device(ADDRESS_MATRIX)
        self.matrix_device.write_cmd(MATRIX_FULLINPUT)
        sleep(0.0005)
        self.data = 0

    def checkkey(self):
        self.matrix_device.write_cmd(MATRIX_CHECKKEY)
        sleep(0.0005)
        self.data = self.matrix_device.read ()
        if (self.data & MATRIX_CHECKKEY ) != MATRIX_CHECKKEY :
            result = True
        else:
            result = False
        return result

    def readkey (self):
        self.key = ' '
        self.matrix_device.write_cmd(MATRIX_COL1)
        sleep(0.0005)
        self.data = self.matrix_device.read ()
        if (self.data & MATRIX_COL1 ) != MATRIX_COL1 :
            if (self.data & MATRIX_LINE1 ) == 0 :
                self.key = '1'
            if (self.data & MATRIX_LINE2 ) == 0 :
                self.key = '4'
            if (self.data & MATRIX_LINE3 ) == 0 :
                self.key = '7'
            if (self.data & MATRIX_LINE4 ) == 0 :
                self.key = '*'
        self.matrix_device.write_cmd(MATRIX_COL2)
        sleep(0.0005)
        self.data = self.matrix_device.read ()
        if (self.data & MATRIX_COL2 ) != MATRIX_COL2 :
            if (self.data & MATRIX_LINE1 ) == 0 :
                self.key = '2'
            if (self.data & MATRIX_LINE2 ) == 0 :
                self.key = '5'
            if (self.data & MATRIX_LINE3 ) == 0 :
                self.key = '8'
            if (self.data & MATRIX_LINE4 ) == 0 :
                self.key = '0'
        self.matrix_device.write_cmd(MATRIX_COL3)
        sleep(0.0005)
        self.data = self.matrix_device.read ()
        if (self.data & MATRIX_COL3 ) != MATRIX_COL3 :
            if (self.data & MATRIX_LINE1 ) == 0 :
                self.key = '3'
            if (self.data & MATRIX_LINE2 ) == 0 :
                self.key = '6'
            if (self.data & MATRIX_LINE3 ) == 0 :
                self.key = '9'
            if (self.data & MATRIX_LINE4 ) == 0 :
                self.key = '#'

        return self.key


 
