#!/usr/bin/python
__author__ = "Stephane BARTHELEMY"
__copyright__ = "Copyright 2018, BARTHELEMY"
__credits__ = ["Stephane BARTHELEMY"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = __author__
__email__ = "stephane@sbarthelemy.com"


class modem :

    def __init__(self):
        ser = serial.Serial()
        ser.port = '/dev/ttyUSB0'
        ser.baudrate = 115200
        ser.timeout = 1
        ser.open()
        ser.write('AT+CMGF=1\r\n')
        ##following line of code sets the prefered message storage area to modem memory
        ser.write('AT+CPMS="ME","SM","ME"\r\n')
        ser.write('AT+CSCA="+33609001390",145')

    def sendsms(self,number,text):
        ser.write('AT+CMGF=1\r\n')
        sleep(2)
        ser.write('AT+CMGS="%s"\r\n' % number)
        sleep(2)
        ser.write('%s' % text)
        sleep(2)
        ser.write(ascii.ctrl('z'))
        print "Text: %s  \nhas been sent to: %s" %(text,number)

    def read_all_sms(self):
        ser.write('AT+CMGF=1\r\n')
        sleep(5)
        ser.write('AT+CMGL=4\r\n')
        sleep(15)
        a = ser.readlines()
        z=[]
        y=[]
        for x in a:
            if x.startswith('+CMGL:'):
                r=a.index(x)
                t=r+1
                z.append(r)
                z.append(t)
        for x in z:
            y.append(a[x])

        ## following line changes modem back to PDU mode
        ser.write('AT+CMGF=0\r\n')
        return y

    def read_unread_sms(self):
        ser.write('AT+CMGF=1\r\n')
        sleep(5)
        ser.write('AT+CMGL=1\r\n')
        sleep(15)
        a = ser.readlines()
        z=[]
        y=[]
        for x in a:
            if x.startswith('+CMGL:'):
                r=a.index(x)
                t=r+1
                z.append(r)
                z.append(t)
        for x in z:
            y.append(a[x])

        ##Following line changed modem back to PDU mode
        ser.write('AT+CMGF=0\r\n')
        return y    

        


    def read_read_sms(self):
        ##returns all unread sms's on your sim card
        ser.write('AT+CMGS=1\r\n')
        ser.read(100)
        ser.write('AT+CMGL="REC READ"\r\n')
        ser.read(1)
        a = ser.readlines()
        for x in a:
            print x

    def delete_all_sms(self):
        ##this changes modem back into PDU mode and deletes all texts then changes modem back into text mode
        ser.write('AT+CMGF=0\r\n')
        sleep(5)
        ser.write('AT+CMGD=0,4\r\n')
        sleep(5)
        ser.write('AT+CMGF=1\r\n')

    def delete_read_sms(self):
        ##this changes modem back into PDU mode and deletes read texts then changes modem back into text mode
        ser.write('AT+CMGF=0\r\n')
        sleep(5)
        ser.write('AT+CMGD=0,1\r\n')
        sleep(5)
        ser.write('AT+CMGF=1\r\n')

        ##this is an attempt to run ussd commands from the gsm modem

    def check_ussd_support(self):
        ##if return from this is "OK" this phone line supports USSD, find out the network operators codes
        ser.write('AT+CMGF=0\r\n')
        ser.write('AT+CUSD=?\r\n')
        ser.write('AT+CMGF=1\r\n')

    ##This function is an attempt to get your sim airtime balance using USSD mode
    def get_balance():
        ##first set the modem to PDU mode, then pass the USSD command(CUSD)=1, USSD code eg:*141# (check your mobile operators USSD numbers)
        ## Error may read +CUSD: 0,"The service you requested is currently not available.",15
        ## default value for <dcs> is 15 NOT 1
        ser.write('AT+CMGF=0\r\n')
        ser.write('AT+CUSD=1,*141#,15\r\n')
        ser.read(1)
        a = ser.readlines()
        print a
        ser.write('AT+CMGF=1\r\n')

    def ussd_sms_check(self):
        ##first set the modem to PDU mode, then pass the USSD command(CUSD)=1, USSD code eg:*141# (check your mobile operators USSD numbers)
        ser.write('AT+CMGF=0\r\n')
        ser.write('AT+CUSD=1,*141*1#,15\r\n')
        ser.read(100)
        a = ser.readlines()
        print a
        ser.write('AT+CMGF=1\r\n')