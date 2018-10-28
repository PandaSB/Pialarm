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
import serial
import threading
from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
from curses import ascii
from myui import led 
from mymodem import modem
from mydetect import line

##read_read_sms()

state = 2
blink = led()
blink.setstate(state)
blink.start()

detectline = line()
detectline.start()

try:
    print ("Press CTRL+C to exit")
    while True:
        if detectline.Isdetected() == True:
            print ("Zone 1 detected ")
            detectline.clear()
        sleep(1)
except KeyboardInterrupt:
    print ("Goodbye.")
    blink.stop()
    detectline.stop()