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
    
    def page1(self,state=0,operator="None",menu=False,delay=0,code="",level = 0) : 
        self.str1 = operator
        if level == 0 : # 0
            self.lcd.lcd_setcgram ( 1 , [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00] )
        elif level < 10 : # Marginal
            self.lcd.lcd_setcgram ( 1 , [0x00,0x00,0x00,0x00,0x00,0x00,0x08,0x08] )
        elif level < 15 : # OK
            self.lcd.lcd_setcgram ( 1 , [0x00,0x00,0x00,0x00,0x04,0x04,0x0C,0x0C] )
        elif level < 20 : # Good
            self.lcd.lcd_setcgram ( 1 , [0x00,0x00,0x02,0x02,0x06,0x06,0x0E,0x0E] )
        else :  # Excelent
            self.lcd.lcd_setcgram ( 1 , [0x01,0x01,0x03,0x03,0x07,0x07,0x0F,0x1F] )
        self.str1 += " ["+chr(1) + "]"
        self.str1 = self.str1.rjust(19)

        self.indicator ^= True
        if self.indicator : 
            self.str1 = "-" + self.str1
        else :
            self.str1 = "|" + self.str1
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
            self.str4 = "2/8 UP/DO 5/6 LF/RG"
        else :
            self.str4 = "* Menu".ljust(16)+code.ljust(4)

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
    

class buzzer : 
    def __init__ (self) : 
        self._pin = port.PA6
        gpio.init()
        gpio.setcfg(self._pin, gpio.OUTPUT)
        gpio.output(self._pin, 0)

    def beep (self,time) : 
        gpio.output(self._pin,1)
        sleep (time)    
        gpio.output(self._pin,0)

class led :

    def __init__(self):
        self._led = port.PA10
        self._ledstate = 0
        self._loop = False
        gpio.init()
        gpio.setcfg(self._led, gpio.OUTPUT)
        gpio.output(self._led, 0)
    
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
                gpio.output(self._led,1)
                sleep(0.5)
                gpio.output(self._led,0)
                sleep(0.5)
            elif self._ledstate == 3:
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

    def setstate (self, state=0):
        self._ledstate = state    
