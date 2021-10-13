#import LoadCell
from hx711 import HX711
import RPi.GPIO as GPIO
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv, time, sys
import cv2

class window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)


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
        
root = Tk()
app = window(master=root)
app.master.geometry('1200x700+200+100')
app.master.title("Hybrid Rocket Engine Data Acquisition Software")
loadCellTxt = Label(root, text="Load Cell")
#loadCellTxt.pack()

xar = []
yar = []

style.use('ggplot')
fig = plt.figure(figsize=(14, 4.5), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
ylim = 100
ax1.set_ylim(0, ylim)
line, = ax1.plot(xar, yar, 'r', marker='o')
#ser = serial.Serial('com3', 9600)

def animate(i):
    value = hx.get_weight(5)
    yar.append(value)
    xar.append(i)
    line.set_data(xar, yar)
    ax1.set_xlim(0, i+1)
    ax1.set_ylim(0, max(yar))
    #with open('load_cell_data.csv', mode='w') as load_cell_data:
        #load_cell_writer = csv.writer(load_cell_data, delimiter=',', quotechar='=', quoting=csv.QUOTE_MINIMAL)
        #load_cell_writer.writerow([time.time(), value])

plotcanvas = FigureCanvasTkAgg(fig, app.master)
plotcanvas.get_tk_widget().grid(column=1, row=1)
ani = animation.FuncAnimation(fig, animate, interval=100, blit=False)

root.mainloop()