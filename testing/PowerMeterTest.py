# Imports
import webiopi
import time
import serial
import binascii
import math

class LCD_23017(object):
    # Timing constants
    E_PULSE = 0.0001
    E_DELAY = 0.0005

    def __init__(self, bus,addr):
        self.bus = bus
        self.addr =addr

        self.bus.write_byte_data(addr, 0x00, 0x00)
        self.bus.write_byte_data(addr, 0x01, 0xF8)

        self.PORTA = 0x12
        self.PORTB = 0x13
        
    def lcd_byte(self, data,mode):

        if mode :
            rs = 1
        else:
            rs = 0
            
        for nybble in (data & 0xf0, data << 4):
            
            self.bus.write_byte_data(self.addr, self.PORTB, rs)
            self.bus.write_byte_data(self.addr, self.PORTA, nybble)
            time.sleep(self.E_PULSE)       
            self.bus.write_byte_data(self.addr, self.PORTB, 0x02 | rs)
            self.bus.write_byte_data(self.addr, self.PORTA, nybble)
            time.sleep(self.E_PULSE)       
            self.bus.write_byte_data(self.addr, self.PORTB, rs)
            time.sleep(self.E_DELAY)
            self.bus.write_byte_data(self.addr, self.PORTB, 0x00)
            time.sleep(self.E_DELAY)
 
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
        for i in bytearray(message.ljust(self.width)):
            lcd_byte(i,self.LCD_CHR)


# Enable debug output
#webiopi.setDebug()

# Retrieve GPIO lib
GPIO = webiopi.GPIO
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

# Called by WebIOPi at script loading
def setup():
    webiopi.debug("Script with macros - Setup")
    # Setup GPIOs
    GPIO.setFunction(17, GPIO.OUT)
    GPIO.setFunction(0, GPIO.OUT)

    GPIO.output(17, GPIO.HIGH)

def readPowerMeterFactor():

    testing=[0x00]
    testing += ser.read(ser.inWaiting())

    testing=[0x00]
    GPIO.output(17, GPIO.HIGH)  # tx data

    x = 0.0
    for i in range(0, 500) :
        x = math.sin(x) * math.cos(x)

    testing=[0x00]
    buff = [0x01, 0x04, 0x07, 0xE7, 0x00, 0x04]
    crc = CalcCrcFast(buff, len(buff))
    buff = buff + crc

    print "%s%s" % ("1. TXD data = ",buff)

    GPIO.output(17, GPIO.HIGH)  # tx data
    #webiopi.debug(buff)

    for i in buff:
        ser.write(chr(i))

    x = 0.0
    for i in range(0, 1000) :
        x = math.sin(x) * math.cos(x)

    GPIO.output(17, 0) # receive data

    x = 0.0
    for i in range(0, 10000) :
        x = math.sin(x) * math.cos(x)

    testing += ser.read(ser.inWaiting())

    aa = len(testing)
    print "%s%s" % ("2. received data = ",testing)
    print "%s %d" % ("3. receaved No = ",aa)        

    a = 0
    b = 0
    c = 0
    d = 0

    if aa == 14 and ord(testing[1]) == 1 and ord(testing[2])== 4: 
        a  = ord(testing[4])*256 + ord(testing[5])
        b  = ord(testing[6])*256 + ord(testing[7])
        c  = ord(testing[8])*256 + ord(testing[9])
        d  = ord(testing[10])*256 +ord(testing[11])

    return (a, b, c, d)

# Looped by WebIOPi
def loop():
    webiopi.sleep(1)

# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("Script with macros - Destroy")
    # Reset GPIO functions

# Read from Serial
@webiopi.macro
def ReadSerial():
    webiopi.debug('ReadSerial')
    test = ""
    while ser.inWaiting() > 0 :
        buf = ser.read(1)
        webiopi.debug(buf)
        webiopi.debug(binascii.b2a_hex(buf))
        test += binascii.b2a_hex(buf).decode('ascii') + ' '

    return test

# Write str to Serial 
@webiopi.macro
def WriteSerial(str):
    webiopi.debug('macro!')
    ser.flushInput()
    webiopi.debug('Receive:')
    webiopi.debug(str);

    temp = str.split('%20') #space
    buf = []
    for i in temp:
        buf.append(strToHex(i))
    crc = CalcCrcFast(buf, len(buf))
    buf = buf + crc

    GPIO.output(17, GPIO.HIGH) #GPIO0 to high(RS485)
    for i in buf:
        ser.write(binascii.a2b_hex(hexToStr(i)))
    webiopi.debug(buf)
    GPIO.output(17, GPIO.LOW) #GPIO0 to low(RS485)
    return 'OK'

# ButtonCtrl
@webiopi.macro
def ButtonCtrl(out):
    webiopi.debug("button control : " + out)
    if out == 'ON':
        value = GPIO.HIGH
    else:
        value = GPIO.LOW        

    GPIO.output(0, value);
    
    return "OK" 

# Set Coil ON/OFF
@webiopi.macro
def CoilCtrl(out):
    webiopi.debug("Coil : " + str(out))

    GPIO.output(17, GPIO.HIGH)
    
    if out == 'on':
        buff = [0x01, 0x06, 0x01, 0xf4, 0xff, 0x00]
        crc = CalcCrcFast(buff, len(buff))
        buff = buff + crc

        webiopi.debug(bytes(buff))
        size = ser.write(bytes(buff))
        webiopi.debug(size)
    else:
        buff = [0x01, 0x06, 0x01, 0xf4, 0x00, 0xff]
        crc = CalcCrcFast(buff, len(buff))
        buff = buff + crc

        webiopi.debug(bytes(buff))
        size = ser.write(bytes(buff))
        webiopi.debug(size)

    x = 0.0; 
    y = 1.0; 
    z = 0.0;  

    for i in range(0, 1500) :
        z += math.sin(y) * math.sin(y)
        y = y - 0.001
        x = x + 0.001
    GPIO.output(17, GPIO.LOW)
    
    return 'OK' 

@webiopi.macro
def PM_read():

    testing=[0x00]
    print ser.inWaiting()
    testing += ser.read(ser.inWaiting())

    testing=[0x00]
    GPIO.output(17, GPIO.HIGH)  # tx data

    x = 0.0 
    for i in range(0, 1000) :
        x = math.sin(x) * math.cos(x)

    buff = [0x01, 0x04, 0x07, 0xD0, 0x00, 0x10]
    crc = CalcCrcFast(buff, len(buff))
    buff = buff + crc
    print(buff)

    for i in buff:
        ser.write(chr(i))
    
    x = 0.0 
    for i in range(0, 1000) :
        x = math.sin(x) * math.cos(x)
  
    GPIO.output(17, GPIO.LOW) # receive data

    x = 0.0 
    for i in range(0, 5000) :
        x = math.sin(x) * math.cos(x)

    print "%s%d" % ("Serial In Waiting = ",ser.inWaiting())

    testing += ser.read(ser.inWaiting())
  
    if( len(testing) >= 38):
        R_volt=testing[10:12]

        print 'Received Data ='
  
        print R_volt 
      
        I_r = ord(testing[4]) * 256 + ord(testing[5])
        I_s = ord(testing[6]) * 256 + ord(testing[7])
        I_t = ord(testing[8]) * 256 + ord(testing[9])

        V_r = ord(testing[10]) * 256 + ord(testing[11])
        V_s = ord(testing[12]) * 256 + ord(testing[13])
        V_t = ord(testing[14]) * 256 + ord(testing[15])

        P_re = ord(testing[16]) * 256 + ord(testing[17])
        Var = ord(testing[18]) * 256 + ord(testing[19])
        Pf  = ord(testing[20]) * 256 + ord(testing[21])
        Hz  = ord(testing[22]) * 256 + ord(testing[23])

        P_WattHour  = ord(testing[24]) * 65535*65536 + ord(testing[25])*65536
        P_WattHour += ord(testing[26]) * 256 + ord(testing[27])

        Var_WattHour  = ord(testing[28]) * 65535*65536 + ord(testing[29])*65536
        Var_WattHour += ord(testing[30]) * 256 + ord(testing[31])

        returnValue  = str(I_r)+':'
        returnValue += str(I_s)+':'
        returnValue += str(I_t)+':'

        returnValue += str(V_r)+':'
        returnValue += str(V_s)+':'
        returnValue += str(V_t)+':'

        returnValue += str(P_re)+':'
        returnValue += str(Var)+':'
        returnValue += str(Pf)+':'

        returnValue += str(P_WattHour)+':'
        returnValue += str(Var_WattHour)+':'

    else:
        returnValue = 'FALSE'   

    print returnValue


def PmReadOneByte():

    testing =[0x00]

    GPIO.output(17, GPIO.LOW)       
    #GPIO.output(17, GPIO.HIGH) #receive data

    # Read Register 2000 ~ 2008
    buff = [0x01, 0x04, 0x05, 0x20, 0x00, 0x02]
    num_to_read = ((buff[len(buff)-2] << 8) | (buff[len(buff)-1]))
    crc = CalcCrcFast(buff, len(buff))
    buff = buff + crc
    print(buff)

    ser.write('\x01')
    ser.write('\x04')
    ser.write('\x05')
    ser.write('\x20')
    ser.write('\x00')
    ser.write('\x02')
    ser.write('\x70')
    ser.write('\xCD')

    print "%s%d" % ("Serial In Waiting = ",ser.inWaiting())
    
    x = 0.0; 
    y = 1.0; 
    z = 0.0;  

    for i in range(0, 500) :
        z += math.sin(y) * math.sin(y)
        y = y - 0.001
        x = x + 0.001

    GPIO.output(17, GPIO.HIGH) #GPIO0 to low(RS485)
    time.sleep(0.5)  

    print "%s%d" % ("Serial In Waiting = ",ser.inWaiting())

    testing += ser.read(ser.inWaiting())
    #testing += ser.readlines()
    print testing


def PM_RelayCtrl(out):

    testing =[0x00]

    GPIO.output(17, GPIO.HIGH)
    
    if out == 0:
        buff = [0x01, 0x06, 0x01, 0xf4, 0xff, 0x00]
        crc = CalcCrcFast(buff, len(buff))
        buff = buff + crc
        print(buff)
        #size = ser.write(bytes(buff))
        ser.write('\x01')
        ser.write('\x06')
        ser.write('\x01')
        ser.write('\xf4')
        ser.write('\xff')
        ser.write('\x00')
        ser.write('\x88')
        ser.write('\x34')
        
    else:
        buff = [0x01, 0x06, 0x01, 0xf4, 0x00, 0xff]
        crc = CalcCrcFast(buff, len(buff))
        buff = buff + crc
        print(bytes(buff))
        #size = ser.write(bytes(buff))
        ser.write('\x01')
        ser.write('\x06')
        ser.write('\x01')
        ser.write('\xf4')
        ser.write('\x00')
        ser.write('\xff')
        ser.write('\x89')
        ser.write('\x84')
 
    x = 0.0; 
    y = 1.0; 
    z = 0.0;  

    for i in range(0,500) :
        z += math.sin(y) * math.sin(y)
        y = y - 0.001
        x = x + 0.001

    GPIO.output(17, GPIO.LOW)
    time.sleep(0.5)  

    print "%s%d" % ("Serial In Waiting = ",ser.inWaiting())

    testing += ser.read(ser.inWaiting())
    #testing += ser.readlines()
    print testing

def test_i2c():
    from datetime import datetime
    import smbus
    import webiopi
    import time
    import serial
    import binascii
    import math

    GPIO = webiopi.GPIO
    ser = serial.Serial("/dev/ttyAMA0", 9600,timeout=1.0)
    #ser.open()

    GPIO.setFunction(17, GPIO.OUT)
    GPIO.setFunction(0, GPIO.OUT)
    GPIO.output(17, GPIO.HIGH)

    driver1 = LCD_23017(bus=smbus.SMBus(1), addr=0x21)
    lcd1 = HD47780(driver=driver1, rows=2, width=16)
    lcd1.lcd_string("Eun Who P.E.",line=0)

    bus = smbus.SMBus(1)
    key_input = bus.read_byte_data(0x21,0x13)
    
    time.sleep(1)  # Wait until the next second
    loop_ctrl =1

    while loop_ctrl:
            
        key_input = bus.read_byte_data(0x21,0x13) | 0x07
        if key_input != 0xff:
            print key_input
            time.sleep(0.02)  # Wait until the next second
            key_input = bus.read_byte_data(0x21,0x13) | 0x07
            if key_input != 0xff:
                if key_input == 0xf7:
                    lcd1.lcd_string("U press SET", line = 1 )
                    PM_RelayCtrl(0)
                    time.sleep(0.7)
                elif key_input == 0xef:
                    lcd1.lcd_string("U press UP", line = 1 )
                    PM_RelayCtrl(1)                  
                    time.sleep(0.7)
                elif key_input == 0xdf:
                    lcd1.lcd_string("U press DOWN", line = 0 )
                    lcd1.lcd_string("Read data ", line = 1 )
                    PM_read()
                    time.sleep(0.7)
                elif key_input == 0xbf:
                    lcd1.lcd_string("U Press RIGHT", line = 1 )
                    lcd1.lcd_string("PM data read", line = 1 )
                    PmReadOneByte()
                    time.sleep(0.5)
                elif key_input == 0x7f:
                    ptPrimary,ptScale,ptSecond,Ct = readPowerMeterFactor()
                    print "%s %d" % ("a. ptPrimary = ",ptPrimary)
                    print "%s %d" % ("b. ptScale   = ",ptScale)
                    print "%s %d" % ("c. ptSecond  = ",ptSecond)
                    print "%s %d" % ("d. Ct        = ",Ct)        
                    lcd1.lcd_string("U Press ESC", line = 1 )

                        
    
def main():
    test_i2c()

if __name__ == "__main__":
    main()
