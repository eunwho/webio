# Eunwho Power Electronics
# www.eunwho.com
######################################
# project    : webControl
# filename   : script.py
# start      :	2013.07.~
# revisioned : 2014.12.29

# Imports
import os
import webiopi
import time
import datetime
import serial
import binascii
import math
import struct

import subprocess
import socket


from webiopi.devices.digital import MCP23017

def get_ip_address_2():
    '''
    Source:
    http://commandline.org.uk/python/how-to-find-out-ip-address-in-python/
    '''
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    ipaddr=s.getsockname()[0]

    return ipaddr


def send_email_2(txMessage):
    import datetime
    import smtplib
    from email.mime.text import MIMEText
    today = datetime.date.today()

    #addr_to = 'eunwho@naver.com'
    addr_to = 'jaejongmoon@gmail.com'
    gmail_user     = 'fromeunwho@gmail.com'
    gmail_password = 'ii11ii11'
    smtpserver     = smtplib.SMTP('smtp.gmail.com',587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user,gmail_password)

    ipaddr = get_ip_address_2()

    my_ip = 'This is alarm message from Power Station. :'
    my_ip += 'Your ip is %s' %  ipaddr
    my_ip += txMessage
    msg = MIMEText(my_ip)
    msg['Subject'] = 'IP For RaspberryPi on %s' % today.strftime('%b %d %Y')
    msg['From'] = gmail_user
    msg['To'] = addr_to
    smtpserver.sendmail(gmail_user, [addr_to], msg.as_string())
    smtpserver.quit()


GPIO = webiopi.GPIO

mcp0 = MCP23017(slave=0x20)
mcp1 = MCP23017(slave=0x21)

mcp0.digitalWrite(0,1)
mcp0.digitalWrite(1,1)
mcp0.digitalWrite(2,1)

mcp0.setFunction(0, 1)
mcp0.setFunction(1, 1)
mcp0.setFunction(2, 1)
mcp0.setFunction(3, 1)
mcp0.setFunction(4, 1)
mcp0.setFunction(5, 1)
mcp0.setFunction(6, 1)
mcp0.setFunction(7, 1)

mcp0.setFunction(8, 0)
mcp0.setFunction(9, 0)
mcp0.setFunction(10,0)
mcp0.setFunction(11,0)
mcp0.setFunction(12,0)
mcp0.setFunction(13,0)
mcp0.setFunction(14,0)
mcp0.setFunction(15,0)

mcp1.setFunction(0, 1)
mcp1.setFunction(1, 1)
mcp1.setFunction(2, 1)
mcp1.setFunction(3, 1)
mcp1.setFunction(4, 1)
mcp1.setFunction(5, 1)
mcp1.setFunction(6, 1)
mcp1.setFunction(7, 1)

mcp1.setFunction(8, 1)
mcp1.setFunction(9, 1)
mcp1.setFunction(10,1)
mcp1.setFunction(11,0)
mcp1.setFunction(12,0)
mcp1.setFunction(13,0)
mcp1.setFunction(14,0)
mcp1.setFunction(15,0)


def delay_usec():
    x=0.1 
    for i in range(0, 50) :
        x = math.sin(x) * math.cos(x)


class EW_LCD_23017(object):
    #E_DELAY = 0.0005
    #E_PULSE = 0.0001

    def __init__(self):
        mcp1.digitalWrite(9,0)  # RW
        mcp1.digitalWrite(10,0)  # RW

    def lcd_byte(self, data,mode):

        if mode :
            rs = 1
        else:
            rs = 0

        mcp1.digitalWrite(8,rs)     # RS  

        mcp1.digitalWrite(4,0)  
        mcp1.digitalWrite(5,0)  
        mcp1.digitalWrite(6,0)  
        mcp1.digitalWrite(7,0)  

        # high nibble setting
        if data &0x10 == 0x10:
            mcp1.digitalWrite(4,1)  
        if data &0x20 == 0x20:
            mcp1.digitalWrite(5,1)  
        if data &0x40 == 0x40:
            mcp1.digitalWrite(6,1)  
        if data &0x80 == 0x80:
            mcp1.digitalWrite(7,1)

        # Toggle Enable Port
        #time.sleep(E_DELAY)
        delay_usec()  
        mcp1.digitalWrite(9,1)      # CE
        delay_usec()  
        #time.sleep(E_PULSE)  
        mcp1.digitalWrite(9,0)
        #time.sleep(E_DELAY)  
        delay_usec()  
        
        # low nibble setting
        mcp1.digitalWrite(4,0)  
        mcp1.digitalWrite(5,0)  
        mcp1.digitalWrite(6,0)  
        mcp1.digitalWrite(7,0)  

        if data &0x01 == 0x01:
            mcp1.digitalWrite(4,1)  
        if data &0x02 == 0x02:
            mcp1.digitalWrite(5,1)  
        if data &0x04 == 0x04:
            mcp1.digitalWrite(6,1)  
        if data &0x08 == 0x08:
            mcp1.digitalWrite(7,1)

        # Toggle Enable Port
        #time.sleep(E_DELAY)  
        delay_usec()  
        mcp1.digitalWrite(9,1)
        #time.sleep(E_PULSE)  
        delay_usec()  
        mcp1.digitalWrite(9,0)
        #time.sleep(E_DELAY)  
        delay_usec()  


class HD47780(object):
    LCD_CHR = 1
    LCD_CMD = 0
    # Base addresses for lines on a 20x4 display
    LCD_BASE = 0x80, 0xC0, 0x94, 0xD4
    #LCD_BASE = 0x00, 0x40, 0x20, 0x54

    def __init__(self, driver, rows=2, width=16):
        self.rows = rows
        self.width = width
        self.driver = driver
        self.lcd_init()

    def lcd_init(self):
        # Initialise display
        lcd_byte = self.driver.lcd_byte
        for i in 0x33, 0x32, 0x28, 0x0C, 0x06, 0x01:
        #for i in 0x01, 0x06, 0x80, 0x01:
            lcd_byte( i,self.LCD_CMD)

    def lcd_string(self, message, line):
        # Send string to display
        lcd_byte = self.driver.lcd_byte
        lcd_byte(self.LCD_BASE[line], self.LCD_CMD)
        #for i in bytearray(message.ljust(self.width)):
        for i in bytearray(message.encode()):
            lcd_byte(i,self.LCD_CHR)


driver1 = EW_LCD_23017( )
lcd1 = HD47780(driver=driver1, rows=2, width=16)
lcd1.lcd_string('Eun Who P.E.',1)

# Enable debug output
webiopi.setDebug()

# Retrieve GPIO lib

ser = serial.Serial("/dev/ttyAMA0", 9600,timeout=1.0)

#CRC - Hi
auchCRCHi = [ 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,
    0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,
    0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,
    0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40, 0x00, 0xC1, 0x81, 0x40,
    0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0, 0x80, 0x41, 0x00, 0xC1,
    0x81, 0x40, 0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41,
    0x00, 0xC1, 0x81, 0x40, 0x01, 0xC0, 0x80, 0x41, 0x01, 0xC0,
    0x80, 0x41, 0x00, 0xC1, 0x81, 0x40]
#CRC - Lo
auchCRCLo = [ 0x00, 0xC0, 0xC1, 0x01, 0xC3, 0x03, 0x02, 0xC2, 0xC6, 0x06,
    0x07, 0xC7, 0x05, 0xC5, 0xC4, 0x04, 0xCC, 0x0C, 0x0D, 0xCD,
    0x0F, 0xCF, 0xCE, 0x0E, 0x0A, 0xCA, 0xCB, 0x0B, 0xC9, 0x09,
    0x08, 0xC8, 0xD8, 0x18, 0x19, 0xD9, 0x1B, 0xDB, 0xDA, 0x1A,
    0x1E, 0xDE, 0xDF, 0x1F, 0xDD, 0x1D, 0x1C, 0xDC, 0x14, 0xD4,
    0xD5, 0x15, 0xD7, 0x17, 0x16, 0xD6, 0xD2, 0x12, 0x13, 0xD3,
    0x11, 0xD1, 0xD0, 0x10, 0xF0, 0x30, 0x31, 0xF1, 0x33, 0xF3,
    0xF2, 0x32, 0x36, 0xF6, 0xF7, 0x37, 0xF5, 0x35, 0x34, 0xF4,
    0x3C, 0xFC, 0xFD, 0x3D, 0xFF, 0x3F, 0x3E, 0xFE, 0xFA, 0x3A,
    0x3B, 0xFB, 0x39, 0xF9, 0xF8, 0x38, 0x28, 0xE8, 0xE9, 0x29,
    0xEB, 0x2B, 0x2A, 0xEA, 0xEE, 0x2E, 0x2F, 0xEF, 0x2D, 0xED,
    0xEC, 0x2C, 0xE4, 0x24, 0x25, 0xE5, 0x27, 0xE7, 0xE6, 0x26,
    0x22, 0xE2, 0xE3, 0x23, 0xE1, 0x21, 0x20, 0xE0, 0xA0, 0x60,
    0x61, 0xA1, 0x63, 0xA3, 0xA2, 0x62, 0x66, 0xA6, 0xA7, 0x67,
    0xA5, 0x65, 0x64, 0xA4, 0x6C, 0xAC, 0xAD, 0x6D, 0xAF, 0x6F,
    0x6E, 0xAE, 0xAA, 0x6A, 0x6B, 0xAB, 0x69, 0xA9, 0xA8, 0x68,
    0x78, 0xB8, 0xB9, 0x79, 0xBB, 0x7B, 0x7A, 0xBA, 0xBE, 0x7E,
    0x7F, 0xBF, 0x7D, 0xBD, 0xBC, 0x7C, 0xB4, 0x74, 0x75, 0xB5,
    0x77, 0xB7, 0xB6, 0x76, 0x72, 0xB2, 0xB3, 0x73, 0xB1, 0x71,
    0x70, 0xB0, 0x50, 0x90, 0x91, 0x51, 0x93, 0x53, 0x52, 0x92,
    0x96, 0x56, 0x57, 0x97, 0x55, 0x95, 0x94, 0x54, 0x9C, 0x5C,
    0x5D, 0x9D, 0x5F, 0x9F, 0x9E, 0x5E, 0x5A, 0x9A, 0x9B, 0x5B,
    0x99, 0x59, 0x58, 0x98, 0x88, 0x48, 0x49, 0x89, 0x4B, 0x8B,
    0x8A, 0x4A, 0x4E, 0x8E, 0x8F, 0x4F, 0x8D, 0x4D, 0x4C, 0x8C,
    0x44, 0x84, 0x85, 0x45, 0x87, 0x47, 0x46, 0x86, 0x82, 0x42,
    0x43, 0x83, 0x41, 0x81, 0x80, 0x40]

# Calculate CRC
def CalcCrcFast(data, length) :
    uchCRCHi = 0xFF # high CRC byte initialized
    uchCRCLo = 0xFF # low CRC byte initialized
    uIndex = 0
    dataIndex = 0
    while length > 0 :
        uIndex = uchCRCHi ^ data[dataIndex]
        uchCRCHi = uchCRCLo ^ auchCRCHi[uIndex]
        uchCRCLo = auchCRCLo[uIndex]
        dataIndex = dataIndex + 1
        length = length -1;

    return [uchCRCHi, uchCRCLo]

#hex to string as it is.
def hexToStr(hex_value):
    return bytes( ("%02x" % hex_value), 'ascii')

def strToHex(str_value):
    return int(str_value,16)

def conv2Float(a):
    s = ''
    try:
        for n in a:
            b = str(hex(n))[2:]           
            if len(b) == 1:
                b = '0' + b
            s += b
        f = struct.unpack('!f',bytes.fromhex(s))[0]
    except:
        f = 0.0

    return f

def setLogFile():

    global dataFileName
    global dataFileLineNumber
    
    dataFileName = '/home/pi/LogData/Log-'
    dataFileName += datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    dataFileName += ".txt"

    dataFileLineNumber = 0;

    with open(dataFileName,'w') as fout:
        fout.write("Power Meter Monitoring System Data Log"+'\r'+'\n')

    with open(dataFileName,'a') as fout:
        fout.write("======================================"+'\r'+'\n')


def rxData( ):

    rxd=[0x00]
    rxd += ser.read(ser.inWaiting())

    GPIO.output(17, GPIO.HIGH)  # tx data

    x = 0.0
    for i in range(0, 500) :
        x = math.sin(x) * math.cos(x)

    rxd =[0x00]
    buff = [0x01, 0x04, 0x05, 0x1A, 0x00, 0x18]
    crc = CalcCrcFast(buff, len(buff))
    buff = buff + crc

    GPIO.output(17, GPIO.HIGH)  # tx data
    size = ser.write(bytes(buff))

    x = 0.0
    for i in range(0, 1000) :
        x = math.sin(x) * math.cos(x)

    GPIO.output(17, 0) # receive data

    x = 0.0
    for i in range(0, 15000) :
        x = math.sin(x) * math.cos(x)

    rxd += ser.read(ser.inWaiting())
    return rxd  


def PowerMeterProc( ):

    testing=rxData( )
  
    if (conv2Float(testing[ 4: 8])) == 0.0 and not (conv2Float(testing[ 8: 12])) == 0.0:
       
        f = open("/home/pi/LogData/rxdErrorLog.txt", 'a') 

        for n in testing:
            f.write(str(n)) 
            f.write(',')

        f.write('\r \n') 
        f.close() 
        if (conv2Float(testing[ 4: 8])) == 0.0:
            webiopi.sleep(0.3)
            testing = rxData( ) 


    if( mcp0.digitalRead(8) ):
        din = '0'
    else:
        din = '1'

    for i in range(7):
        if( mcp0.digitalRead(i+9) ):
            din += '0'
        else:
            din += '1'

    a = len(testing)

    if a < 54 :
        b = din
    else:
        b  = 'V_rs='+("%.1f" %(conv2Float(testing[ 4: 8]))) +':'
        b += 'V_st='+("%.1f" %(conv2Float(testing[ 8:12]))) +':'
        b += 'V_tr='+("%.1f" %(conv2Float(testing[12:16]))) +':'

        b += 'I_r=' +("%.1f" %(conv2Float(testing[16:20]))) +':'
        b += 'I_s=' +("%.1f" %(conv2Float(testing[20:24]))) +':'
        b += 'I_t=' +("%.1f" %(conv2Float(testing[24:28]))) +':'

        b += 'P_re='+("%.1f" %(conv2Float(testing[28:32])/1000)) +':'
        b += 'Pvar='+("%.1f" %(conv2Float(testing[32:36])/1000)) +':'

        b += 'pf='  +("%.1f" %(conv2Float(testing[36:40]))) +':'
        b += 'Hz='  +("%.1f" %(conv2Float(testing[40:44]))) +':'

        b += 'kWh=' +("%.1f" %(conv2Float(testing[44:48]))) +':'
        b += 'kVah='+("%.1f" %(conv2Float(testing[48:52]))) +':'

        b += din +':END'

    return b


# Called by WebIOPi at script loading
def setup():

    webiopi.debug("Script with macros - Setup")

    # Setup GPIOs
    GPIO.setFunction(17, GPIO.OUT)
    GPIO.setFunction(0, GPIO.OUT)
    GPIO.output(17, GPIO.HIGH)
    setLogFile()
 

firstOnDIN_1=1  
firstOnDIN_2=1  
firstOnDIN_3=1  
firstOnDIN_4=1  

startTime = time.time()
f_startTime = time.time()

#os.system("sudo halt")
# Looped by WebIOPi
def loop():

    global startTime
    global firstOn
    global f_startTime
    global dataFileLineNumber
    global dataFileName
    
    global firstOnDIN_1  
    global firstOnDIN_2  
    global firstOnDIN_3  
    global firstOnDIN_4  

    endTime = time.time()
    elapsedTime = endTime - startTime
 
    pilotLed = not mcp0.digitalRead(7)
    mcp0.digitalWrite(7,pilotLed)
    
    #driver1 = EW_LCD_23017( )
    #lcd1 = HD47780(driver=driver1, rows=2, width=16)

    if not mcp1.digitalRead(11):
        #get_ip_address_2():
        lcd1.lcd_string(get_ip_address_2(), 0 )
    
    dinCheck =[0,0,0,0] 
    if not mcp0.digitalRead(8):
        dinCheck[0] = 1
        if elapsedTime > 3600 or firstOnDIN_1 == 1 : 
            send_email_2(' ALARM DIN 1 ON ') 
            startTime = time.time()
            firstOnDIN_1 = 0

    if not mcp0.digitalRead(9):
        dinCheck[1] = 1
        if elapsedTime > 3600 or firstOnDIN_2 == 1 : 
            send_email_2(' ALARM DIN 2 ON ') 
            startTime = time.time()
            firstOnDIN_2 = 0

    if not mcp0.digitalRead(10):
        dinCheck[2] = 1
        if elapsedTime > 3600 or firstOnDIN_3 == 1 : 
            lcd1.lcd_string(" DIN 3 ON  ", 1 )
            send_email_2(' ALARM DIN 3 ON ') 
            startTime = time.time()
            firstOnDIN_3 = 0

    if not mcp0.digitalRead(11):
        dinCheck[3] = 1
        if elapsedTime > 3600 or firstOnDIN_4 == 1 : 
            lcd1.lcd_string(" DIN 4 ON  ", 1 )
            send_email_2('  ALARM DIN 4 ON ') 
            startTime = time.time()
            firstOnDIN_4 =  0 
    
    lcdMessage = ' ' 
    for x in dinCheck :   
        if x == 0 :
            lcdMessage += 'OFF '
        else:
            lcdMessage += ' ON '         
 
    lcd1.lcd_string(lcdMessage , 1 )


    f_endTime = time.time()
    f_elapsedTime = f_endTime - f_startTime


    if f_elapsedTime > 60 :
    #if f_elapsedTime > 20 :
        f_startTime = time.time() 

        if(dataFileLineNumber > 999):
        #if(dataFileLineNumber > 19):
            setLogFile()
        
        dataFileLineNumber += 1
        s= str(dataFileLineNumber)+'\t'
        
        try:
            with open(dataFileName,'a') as f:
                f.write(s)
            s = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'\t'    
            with open(dataFileName,'a') as f:
                f.write(s)

            d = PowerMeterProc()
            data_log = d +'\r'+'\n'
            with open(dataFileName,'a') as f:
                f.write(data_log)
        except:
            setLogFile()
            pass

        webiopi.debug(s)

    webiopi.sleep(10)


# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("Script with macros - Destroy")
    # Reset GPIO functions

# ButtonCtrl
@webiopi.macro
def startMonitor(out):
    mcp0.digitalWrite(0,0)
    mcp0.digitalWrite(1,1)
    return 'OK'

@webiopi.macro
def stopMonitor(out):
    mcp0.digitalWrite(0,1)
    mcp0.digitalWrite(1,0)
    return 'OK'

@webiopi.macro
def Relay3_On(out):
    mcp0.digitalWrite(2,0)
    return 'OK'

@webiopi.macro
def Relay3_Off(out):
    mcp0.digitalWrite(2,1)
    return 'OK'

@webiopi.macro
def CoilCtrl(out):  
    return PowerMeterProc( )

