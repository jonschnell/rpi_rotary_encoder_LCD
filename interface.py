import time
import RPi.GPIO as GPIO
from encoder import Encoder
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

version = "PWNB v0.0"

def pageSelect(value, direction):
    print("PAGE: {}, DIRECTION: {}".format(value, direction))
    #toPrint = "PAGE: " + str(value)
    lcd.clear()
    #lcd.write_string(toPrint)
    if value == 0:
        lcd.write_string(version)
    elif value == 1:
        wifi()
    elif value == 2:
        bluetooth()
    elif value == 3:
        nfc()


e1 = Encoder(18, 24, pageSelect)

lcd.write_string(version)

def wifi():
    lcd.write_string("WIFI")

def bluetooth():
    lcd.write_string("BLUETOOTH")

def nfc():
    lcd.write_string("NFC")

try:
    while True:
        time.sleep(.25)
        if GPIO.input(23) == 0:
            print("click")
        #print("Value is {}".format(e1.getValue()))
except Exception:
    pass

GPIO.cleanup()
