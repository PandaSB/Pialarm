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

class line:

    def __init__(self):
        self._loop = False
        self.detected = False 
        self._line1 = port.PA2
        gpio.init()
        gpio.setcfg(self._line1, gpio.INPUT)
        gpio.pullup(self._line1, gpio.PULLUP)
    
    def start(self):
        self.tline = threading.Thread(name='line', target=self.process)
        self._loop = True 
        self.tline.start()

    def process(self):
        while self._loop:
            self.line_state = gpio.input(self._line1) # Read line1 state
            if self.line_state != 0:
                self.detected = True 
            sleep (0.1)

    def stop (self):
        self._loop = False

    def Isdetected(self):
        return self.detected

    def clear(self):
        self.detected =  False 