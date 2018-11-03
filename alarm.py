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
import threading
from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
from curses import ascii
from myui import led 
from myui import screen
from mymodem import modem
from mydetect import line


check_phone_number  = False
phone_allow = "+33600000000"
check_sms_password = True 
password_allow = "testpasswd"

gsmmodem = modem()
operator = gsmmodem.get_operator()

#print gsmmodem.read_all_sms()
#print gsmmodem.read_read_sms()
#print gsmmodem.read_unread_sms()
#print gsmmodem.get_level()

state = 2
page = 1 
blink = led()
blink.setstate(state)
blink.start()

display = screen()
sleep (3)
detectline = line()
detectline.start()

try:
    print ("Press CTRL+C to exit")
    while True:
        if detectline.Isdetected() == True:
            print ("Zone 1 detected ")
            detectline.clear()
        if page == 0 : 
            display.page0()
        elif page == 1 :
            display.page1(state,operator,False,0)
        elif page == 2 :
            display.page2() 
        elif page == 3 :
            display.page3()
        elif  page == 4 :
            display.page4()
        else :
            display.page0()
        smslist  = gsmmodem.read_read_sms()
        if smslist :
            for x in smslist : 
                if x.startswith("+CMGL:"): 
                    info = x.split(",")
                    if check_phone_number :
                        tel = info[2].replace('"', '')
                        if phone_allow.find(tel) != -1 : 
                            smsok = True
                        else :
                            smsok = False
                    else :
                        smsok = True 
                    if smsok : 
                        print "SMS ok"     
        else :
            print "no SMS receved"
        sleep(1)
except KeyboardInterrupt:
    print ("Goodbye.")
    blink.stop()
    detectline.stop()