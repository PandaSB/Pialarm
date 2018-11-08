#!/usr/bin/python

import os
import sys
import threading
import ConfigParser
import io
from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
from curses import ascii
from myui import led 
from myui import buzzer
from myui import screen
from myui import keyboard
from mymodem import modem
from mydetect import line


__author__     = "Stephane BARTHELEMY"
__copyright__  = "Copyright 2018, BARTHELEMY"
__credits__    = ["Stephane BARTHELEMY"]
__license__    = "MIT"
__version__    = "1.0"
__maintainer__ = __author__
__email__      = "stephane@sbarthelemy.com"

def set_state (value) : 
    global state
    global timeout
    if   value == "0" :
        state = 0
        gsmmodem.sendsms(phone_allow,"ALARM DISARMED")                
    elif value == "1" :
        state = 1
        timeout = default_timeout
        gsmmodem.sendsms(phone_allow,"ALARM PRE ARMED")        
    elif value == "2" :
        state = 2
        gsmmodem.sendsms(phone_allow,"ALARM ARMED")        
    elif value == "3" :
        state = 3
        timeout = default_timeout
        gsmmodem.sendsms(phone_allow,"ALARM PRE DETECTION")        
    elif value == "4"  :
        state = 4
        gsmmodem.sendsms(phone_allow,"ALARM DETECTION")        
    elif value == "arm" :    
        state = 2
        gsmmodem.sendsms(phone_allow,"ALARM ARMED")        
    elif value == "disarm" :
        state = 0
        gsmmodem.sendsms(phone_allow,"ALARM DISARMED")        


def manage_sms (list) : 
    for x in list : 
        if x.startswith("+CMGL:"): 
            info = x.split(",")
            tel = info[2].replace('"', '')
            if check_phone_number :
                if phone_allow == tel : 
                    smsok = True
                else :
                    smsok = False
            else :
                smsok = True 
            if smsok : 
                r=list.index(x)
                smsline = list[r+1]
                index_cmd  = 0
                index_arg  = 1
                index_arg2 = 2
                smsdata = smsline.split()
                print smsdata
                if check_sms_password :
                    index_cmd  +=1
                    index_arg  +=1
                    index_arg2 +=1
                    if password_allow != smsdata[0] : 
                            smsok = False
            if smsok : 
                cmd = smsdata[index_cmd]
                if cmd == "state" : 
                    arg = smsdata[index_arg]
                    set_state(arg)


def display_page (lpage) : 
    if lpage == 0 : 
        display.page0()
    elif lpage == 1 :
        display.page1(state,operator,menu,timeout,code)
    elif lpage == 2 :
        display.page2() 
    elif lpage == 3 :
        display.page3()
    elif lpage == 4 :
        display.page4()
    else :
        display.page0()


def action () : 
    global state 
    global timeout
    if   (state == 0) :
        # disarm
        state += 0 # nothing to do
        blink.setstate(1) 
    elif (state == 1) :
        # delay arm
        if timeout > 0 :
            timeout -= 1; 
        if timeout == 0 :
            set_state("2")
        blink.setstate(1)
    elif (state == 2) :
        # arm 
        if detectline.Isdetected() == True:
            print ("Zone 1 detected ")
            detectline.clear()
            set_state ("3")
        blink.setstate(2)
    elif (state == 3) :
        # delay detection
        if timeout > 0 :
            timeout -= 1; 
        if timeout == 0 :
            set_state ("4")
        blink.setstate(3) 
    elif (state == 4) :
        # detection
        state +=0 # nothing to do
        blink.setstate(3)  

def KeyReceived (value , press) : 
    global menu
    global code
    if press : 
        bip.beep(0.2)
        if value == '*' :
            menu = not menu
        elif value == '#' :
            print "code : " + code
            print "code_allow : " + code_allow
            print "state :" + str(state) 
            if code == code_allow : 
                if state == 0 :
                    set_state ("1")
                else :
                    set_state ("0")
            code = "" 
        else :
            code += value
            if len(code) > 4 :
                code = code[1:] 
            print code 

#Init 

configfile_name = "/etc/alarm.conf"
if not os.path.isfile(configfile_name):
    cfgfile = open(configfile_name, 'w')
    # Add content to the file
    Config = ConfigParser.ConfigParser()
    Config.add_section('alarm')
    Config.set('alarm', 'check_phone', False)
    Config.set('alarm', 'check_password', True)
    Config.set('alarm', 'passwd', 'Test')
    Config.set('alarm', 'code', '1234')
    Config.set('alarm', 'phone', '+33600000000')
    Config.set('alarm', 'timeout','10')
    Config.set('alarm', 'state', '0')
    Config.add_section('modem')
    Config.set('modem','port','/dev/ttyUSB1')
    Config.set('modem','sms_server','+33609001390')
    Config.write(cfgfile)
    cfgfile.close()


# Load the configuration file
with open(configfile_name) as f:
    iniconfig = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(iniconfig))
    check_phone_number = config.getboolean ('alarm','check_phone')
    check_sms_password = config.getboolean ('alarm','check_password')
    phone_allow        = config.get        ('alarm','phone')
    password_allow     = config.get        ('alarm','passwd')
    state              = int (config.get   ('alarm','state'))
    default_timeout    = int (config.get   ('alarm','timeout'))
    code_allow         = config.get        ('alarm','code')
    port               = config.get        ('modem', 'port')
    smsserver          = config.get        ('modem','sms_server')
 
    f.close()

print "Configuration data"
print "  check phone number : " + str (check_phone_number )
print "  check password     : " + str (check_sms_password )
print "  phone              : " + phone_allow
print "  password           : " + password_allow
print "  state              : " + str (state)
print "  timeout            : " + str (default_timeout)
print "  port               : " + port
print "  sms server         : " + smsserver

timeout            = default_timeout
page               = 1 
code               = ""
menu                = False

gsmmodem = modem(port,smsserver)
operator = gsmmodem.get_operator()

blink = led()
blink.setstate(state)
blink.start()

bip = buzzer()


key = keyboard(KeyReceived)
key.start()

display = screen()
sleep (1)
detectline = line()
detectline.start()

try:
    print ("Press CTRL+C to exit")
    while True:
        display_page (page) 
        action ()   
        smslist  = gsmmodem.read_unread_sms()
        if smslist :
            manage_sms (smslist)
            gsmmodem.delete_all_sms()
        sleep(1)
except KeyboardInterrupt:
    print ("Goodbye.")
    blink.stop()
    detectline.stop()
    key.stop()
