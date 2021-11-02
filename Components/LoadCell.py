from hx711 import HX711
import RPi.GPIO as GPIO
import sys

def cleanAndExit():
    #print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    #print("Bye!")
    sys.exit()

referenceUnit = 92

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

def getWeight(value):
    return hx.get_weight(value)