# Imports
import webiopi
import time
import serial
import binascii
import math
import RPi.GPIO as GPIO

from webiopi.devices.digital import MCP23017


mcp0 = MCP23017(slave=0x20)
mcp1 = MCP23017(slave=0x21)

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

mcp0.digitalWrite(0,1)
mcp0.digitalWrite(1,0)
mcp0.digitalWrite(2,1)

"""
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
"""

class EW_LCD_23017(object):

    def __init__(self):
        mcp1.digitalWrite(9,0)  # RW
        mcp1.digitalWrite(10,0)  # RW

    def lcd_byte(self, data,mode):

        E_DELAY = 0.0005
        E_PULSE = 0.0001

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
        time.sleep(E_DELAY)  
        mcp1.digitalWrite(9,1)      # CE
        time.sleep(E_PULSE)  
        mcp1.digitalWrite(9,0)
        time.sleep(E_DELAY)  
        
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
        time.sleep(0.0001)  
        mcp1.digitalWrite(9,1)
        time.sleep(E_PULSE)  
        mcp1.digitalWrite(9,0)
        time.sleep(E_DELAY)  

 
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

def setup():
    webiopi.debug("Script with macros - Setup")
    # Setup GPIOs
    GPIO.setFunction(17, GPIO.OUT)
    GPIO.setFunction(0, GPIO.OUT)

    GPIO.output(17, GPIO.HIGH)


def test_i2c():
    from datetime import datetime
    import webiopi
    import time
    import serial
    import binascii
    import math

    GPIO = webiopi.GPIO

    GPIO.setFunction(17, GPIO.OUT)
    GPIO.setFunction(0, GPIO.OUT)
    GPIO.output(17, GPIO.HIGH)

    #driver1 = LCD_23017(bus=smbus.SMBus(1), addr=0x21)
    driver1 = EW_LCD_23017( )
    lcd1 = HD47780(driver=driver1, rows=2, width=16)
    lcd1.lcd_string("Eun Who P.E.",line=0)

    time.sleep(1)  # Wait until the next second
    loop_ctrl =1

    while loop_ctrl:
            
        if ( int(mcp1.digitalRead(11)) == 0):
            lcd1.lcd_string("U press SET", line = 1 )
        elif ( int(mcp1.digitalRead(12)) == 0) :
            lcd1.lcd_string("U press UP", line = 1 )
        elif ( int(mcp1.digitalRead(13)) == 0) :
            lcd1.lcd_string("U press DOWN", line = 1 )
            lcd1.lcd_string("Read data ", line = 0 )
        elif ( int(mcp1.digitalRead(14)) == 0) :
            lcd1.lcd_string("U Press RIGHT", line = 1 )
            lcd1.lcd_string("PM data read", line = 0 )
        elif ( int(mcp1.digitalRead(15)) == 0) :
            lcd1.lcd_string("U Press ESC", line = 1 )

        time.sleep(0.5)
                        
    
def main():
    test_i2c()

if __name__ == "__main__":
    main()
