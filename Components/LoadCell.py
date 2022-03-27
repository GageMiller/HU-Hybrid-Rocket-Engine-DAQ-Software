from hx711 import HX711

referenceUnit = 52251.39

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)


hx.reset()

hx.tare()

def getWeight(value):
    return hx.get_weight(value)