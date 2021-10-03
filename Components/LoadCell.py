#! /usr/bin/python2

import time
import sys
import csv

EMULATE_HX711=False

referenceUnit = 92

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    #print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    #print("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

#print("Tare done! Add weight now...")
with open('load_cell_data.csv', mode='w') as load_cell_data:
    while True:
        try:
            val = hx.get_weight(5)
            print(val)
            load_cell_writer = csv.writer(load_cell_data, delimiter=',', quotechar='=', quoting=csv.QUOTE_MINIMAL)
            load_cell_writer.writerow([time.time(), hx.get_weight(5)])

            hx.power_down()
            hx.power_up()
            #time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()