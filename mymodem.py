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
from time import sleep



class modem :

    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.xonxoff = 0
        self.ser.rtscts = True
        self.ser.timeout = 0
        self.ser.dsrdtr = True
        self.ser.port = '/dev/ttyUSB1' #try different ports here, if this doesn't work.
        self.ser.parity=serial.PARITY_NONE
        self.ser.open()
        self.ser.write('\r')
        #self.read_write('ATZ\r')
        self.read_write('AT+CMGF=1\r')
        ##following line of code sets the prefered message storage area to modem memory
        self.read_write('AT+CPMS="ME","ME","ME"\r')
        self.read_write('AT+CSCA="+33609001390",145\r')
        self.read_write('AT+CMGF=0\r')

    def read_write (self,data) :
        self.ser.write(data)
        self.msg = self.read_serial ()
        print self.msg
        return self.msg

    def read_serial(self,read_timeout=0.5):
        self.answer = ""
        #self.read_timeout = 0.5
        self.quantity = self.ser.in_waiting
        while True:
            if self.quantity > 0:
                self.answer += self.ser.read(self.quantity)
            else:
                # read_timeout is depends on port speed
                # with following formula it works:
                # 0.1 sec + 1.0 sec / baud rate (bits per second) * 10.0 bits (per character) * 10.0 times
                # example for 115200 baud rate:
                # 0.1 + 1.0 / 115200 * 10.0 * 10.0 ~ 0.1 sec
                sleep(read_timeout) 
            self.quantity = self.ser.in_waiting
            if self.quantity == 0:
                break      
        return self.answer

    def sendsms(self,number,text):
        self.read_write('AT+CMGF=1\r\n')
        self.read_write('AT+CMGS="%s"\r\n' % number)
        self.read_write('%s' % text)
        self.read_write(ascii.ctrl('z'))
        print "Text: %s  \nhas been sent to: %s" %(text,number)

    def read_all_sms(self):
        self.read_write('AT+CMGF=1\r')
        a = self.read_write('AT+CMGL="ALL"\r')
        lines = a.split( "\n" )
        z=[]
        y=[]
        for x in lines:
            if x.startswith('+CMGL:'):
                r=lines.index(x)
                t=r+1
                z.append(r)
                z.append(t)
        for x in z:
            y.append(lines[x])

        ## following line changes modem back to PDU mode
        self.read_write('AT+CMGF=0\r')
        return y

    def read_unread_sms(self):
        self.read_write('AT+CMGF=1\r')
        a = self.read_write('AT+CMGL="REC UNREAD"\r')
        lines = a.split( "\n" )
        z=[]
        y=[]
        for x in lines:
            if x.startswith('+CMGL:'):
                r=lines.index(x)
                t=r+1
                z.append(r)
                z.append(t)
        for x in z:
            y.append(lines[x])

        ## following line changes modem back to PDU mode
        self.read_write('AT+CMGF=0\r')
        return y
        


    def read_read_sms(self):
        self.read_write('AT+CMGF=1\r')
        a = self.read_write('AT+CMGL="REC READ"\r')
        lines = a.split( "\n" )
        z=[]
        y=[]
        for x in lines:
            if x.startswith('+CMGL:'):
                r=lines.index(x)
                t=r+1
                z.append(r)
                z.append(t)
        for x in z:
            y.append(lines[x])

        ## following line changes modem back to PDU mode
        self.read_write('AT+CMGF=0\r')
        return y

    def delete_all_sms(self):
        ##this changes modem back into PDU mode and deletes all texts then changes modem back into text mode
        self.read_write('AT+CMGF=0\r')
        self.read_write('AT+CMGD=0,4\r')
        self.read_write('AT+CMGF=1\r')

    def delete_read_sms(self):
        ##this changes modem back into PDU mode and deletes read texts then changes modem back into text mode
        self.read_write('AT+CMGF=0\r')
        self.read_write('AT+CMGD=0,1\r')
        self.read_write('AT+CMGF=1\r')

    def get_operator(self):
        a= self.read_write('AT+COPS?\r').replace('\"','')
        r=a.split(",")
        return r[2]

    def get_level(self):
        a=self.read_write ("AT+CSQ\r")
        r = a.split()
        s = r[2].split(",")
        return s[0]