#!/usr/bin/python
__author__ = "Stephane BARTHELEMY"
__copyright__ = "Copyright 2018, BARTHELEMY"
__credits__ = ["Stephane BARTHELEMY"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = __author__
__email__ = "stephane@sbarthelemy.com"


import os
import sys
from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
import threading
import lcddriver
import matrixdriver


class led :

    def __init__(self):
        self._led = port.PA10
        self._ledstate = 0
        self._loop = False
        gpio.init()
        gpio.setcfg(self._led, gpio.OUTPUT)
        self.matrix = matrixdriver.matrix()
        self.lcd = lcddriver.lcd()
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string("                    ", 1)
        self.lcd.lcd_display_string("  *** PI ALARM ***  ", 2)
        self.lcd.lcd_display_string("", 3)
        self.lcd.lcd_display_string("(c) BARTHELEMY      ", 4)
    
    def start(self):
        self._loop = True 
        self.tblink = threading.Thread(name='blink', target=self.process)
        self.tblink.start()
        self.tmaxtrix = threading.Thread(name='matrix', target=self.process_matrix)
        self.tmaxtrix.start()


    def process_matrix(self):
        while self._loop:
            check = self.matrix.checkkey()
            if check:
                self.key = self.matrix.readkey()
                print self.key

    def process(self):
        while self._loop:
            if  self._ledstate == 0:
                gpio.output(self._led,0)
                sleep(1)
            elif self._ledstate == 1:
                gpio.output(self._led,1)
                sleep(0.1)
            elif self._ledstate == 2:
                gpio.output(self._led, 1)
                sleep(0.1)
                gpio.output(self._led, 0)
                sleep(0.1)

                gpio.output(self._led, 1)
                sleep(0.1)
                gpio.output(self._led, 0)
                sleep(0.1)
                sleep(0.6)
            else:
                sleep(1)

    def stop (self):
        self._loop = False

    def setstate (self, state):
        self._ledstate = state    
