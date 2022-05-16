import time
import RPi.GPIO as GPIO
from encoder import Encoder
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', 0x27)
GPIO.setmode(GPIO.BCM)

version = "PWNB v0.0"

def pageSelect(value, direction, click):
    print("PAGE: {}, DIRECTION: {}, CLICK: {}".format(value, direction, click))

    lcd.clear()

    if value == 0:
        lcd.write_string(version)
    elif value == 1:
        lcd.write_string("WIFI")
        if click == 1:
            wifi()
    elif value == 2:
        lcd.write_string("BLUETOOTH")
        if click == 1:
            bluetooth()
    elif value == 3:
        lcd.write_string("NFC")
        if click == 1:
            nfc()



e1 = Encoder(18, 24, 23, pageSelect)

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

except Exception:
    pass

GPIO.cleanup()
