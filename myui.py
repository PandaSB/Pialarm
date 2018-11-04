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


class screen :

    indicator = False

    def __init__(self):
        self.lcd = lcddriver.lcd()
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string("                    ", 1)
        self.lcd.lcd_display_string("  *** PI ALARM ***  ", 2)
        self.lcd.lcd_display_string("", 3)
        self.lcd.lcd_display_string("(c) BARTHELEMY      ", 4)
        sleep(5)

    def page0(self):
        self.str = "                    "
        self.lcd.lcd_display_string(self.str, 1)
        self.lcd.lcd_display_string(self.str, 2)
        self.lcd.lcd_display_string(self.str, 3)
        self.lcd.lcd_display_string(self.str, 4)
    
    def page1(self,state=0,operator="None",menu=False,delay=0) : 
        self.str1 = operator.ljust(19)
        self.indicator ^= True
        if self.indicator : 
            self.str1 += "-"
        else :
            self.str1 += "|"
        self.str3 = "                    "
        if state == 0 :
            self.str2 = "** DISARMED **".center(20)
            self.str3 = "Press code + '#'".center(20)
        elif state == 1 :
            self.str2 = "** DELAYED ARMED **".center(20)
            self.str3 = str(delay).center(20)
        elif state == 2 :
            self.str2 = "** ARMED **".center(20)
            self.str3 = "Press code + '#'".center(20)
        elif state == 3 :
            self.str2 = "** DETECTION **".center(20)
            self.str3 = str(delay).center(20)
        elif state == 4 :
            self.str2 = "** ALARM ON **".center(20)
            self.str3 = "Press code + '#'".center(20)
        else :
            self.str2 = "** ERROR **".center(20)    
        if (menu == True) : 
            self.str4 = " 2 \24 8 \25"
        else :
            self.str4 = "* Menu ".ljust(16)

        self.lcd.lcd_display_string(self.str1, 1)
        self.lcd.lcd_display_string(self.str2, 2)
        self.lcd.lcd_display_string(self.str3, 3)
        self.lcd.lcd_display_string(self.str4, 4)

    def page2(self):
        self.str = "                    "
        self.lcd.lcd_display_string(self.str, 1)
        self.lcd.lcd_display_string(self.str, 2)
        self.lcd.lcd_display_string(self.str, 3)
        self.lcd.lcd_display_string(self.str, 4)

    def page3(self):
        self.str = "                    "
        self.lcd.lcd_display_string(self.str, 1)
        self.lcd.lcd_display_string(self.str, 2)
        self.lcd.lcd_display_string(self.str, 3)
        self.lcd.lcd_display_string(self.str, 4)

    def page4(self):
        self.str = "                    "
        self.lcd.lcd_display_string(self.str, 1)
        self.lcd.lcd_display_string(self.str, 2)
        self.lcd.lcd_display_string(self.str, 3)
        self.lcd.lcd_display_string(self.str, 4)


class keyboard :
    def __init__(self,callback=None):
        self.matrix = matrixdriver.matrix()
        self.oldkey = "-"
        self.callback = callback 
        self._loop = False


    def start(self) :
        self._loop = True 
        self.tmaxtrix = threading.Thread(name='matrix', target=self.process_matrix)
        self.tmaxtrix.start()

    def process_matrix(self):
        while self._loop:
            check = self.matrix.checkkey()
            if check:
                self.key = self.matrix.readkey()
                if self.key != self.oldkey : 
                    if self.callback != None :
                        self.callback(self.key,True)
                self.oldkey = self.key
            else : 
                if  self.oldkey != "-" :
                    if self.callback != None : 
                        self.callback(self.oldkey,False)
                self.oldkey = "-"

    def stop (self):
        self._loop = False
    


class led :

    def __init__(self):
        self._led = port.PA10
        self._ledstate = 0
        self._loop = False
        gpio.init()
        gpio.setcfg(self._led, gpio.OUTPUT)
    
    def start(self):
        self._loop = True 
        self.tblink = threading.Thread(name='blink', target=self.process)
        self.tblink.start()

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
