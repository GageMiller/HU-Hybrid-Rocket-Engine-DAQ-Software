'''
Author: Gage Miller
Description:
This program allows the Harding University Hybrid Rocket engine team
to easily check the status of and collect data from the various sensor
on the engine. It also displays whether the engine control is armed.
The GUI is written in tkinter.
'''
import Components.Camera as camera
from tkinter import *
import tkinter as tk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv, time
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import serial, struct
from time import sleep

#Comment this import out when the load cell is not connected
import Components.LoadCell as loadCell

#Comment this line out when the load cell IS connected
#GPIO.setmode(GPIO.BOARD)

#Safe and arm switch GPIO setup
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

ser = serial.Serial('/dev/serial0',
                    baudrate=9600,
                    timeout=1)

class window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

data = []

#Writes the load cell data to a csv file when the export button is pressed
def writeLoadCellData():
    with open('load_cell_data.csv', mode='a+') as load_cell_data:
        load_cell_writer = csv.writer(load_cell_data, delimiter=',', quotechar='=', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            load_cell_writer.writerow(row)

root = Tk()
app = window(master=root)
app.master.geometry('1920x1080+0+0')
app.master.title("Hybrid Rocket Engine Data Acquisition Software")

open('load_cell_data.csv', 'w').close()

photoRed = ImageTk.PhotoImage(Image.open("/home/pi/Documents/HU-Hybrid-Rocket-Engine-DAQ-Software/Media/Red.png"))
photoGreen = ImageTk.PhotoImage(Image.open("/home/pi/Documents/HU-Hybrid-Rocket-Engine-DAQ-Software/Media/Green.png"))
imgLabel = Label(root, image=photoRed)
imgLabel.grid(row=1,column=3, ipadx=175)

#Checks whether the safe and arm switch is connected
def safeAndArmCheck(imgLabel):
    if(not GPIO.input(24)):
        imgLabel.configure(image=photoRed)
    else:
        imgLabel.configure(image=photoGreen)

loadCellTxt = Label(root, text="Load Cell")

xar = []
yar = []

style.use('ggplot')
fig = plt.figure(figsize=(14, 4.5), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
ylim = 100
ax1.set_ylim(0, ylim)
line, = ax1.plot(xar, yar, 'r', marker='o')

xar_p = [0]
yar_p = [0]

style.use('ggplot')
fig_p = plt.figure(figsize=(14, 4.5), dpi=100)
ax1_p = fig_p.add_subplot(1, 1, 1)
ylim = 500
ax1_p.set_ylim(0, ylim)
line_p, = ax1_p.plot(xar_p, yar_p, 'r', marker='o')

#Animates the live matplotlib plot of the load cell
def animate_l(i):
    #If load Cell is connected
    value = loadCell.getWeight(5)

    #If load cell not connected
    #value = 1

    if(not GPIO.input(24)):
        data.append([time.time(), value])
    yar.append(value)
    xar.append(i)
    line.set_data(xar, yar)
    ax1.set_xlim(0, i+1)
    ax1.set_ylim(0, max(yar))
    safeAndArmCheck(imgLabel)

    #received_data = ser.read()                                      #read serial port
    #print(int.from_bytes(received_data, "big"))                     #print received data

#Animates the live matplotlib plot of the load cell
def animate_p(i):
    #If pressure sensor is connected
    if ser.inWaiting:
        received_data = ser.readline()
    else:
        received_data = b''

    if(received_data is not b''):
        pressureValue = int(received_data[:3])
        volts = pressureValue * 5.0 / 1023.0
        PSI = 150.0*(volts-1.0)
        if(not GPIO.input(24)):
            data.append([time.time(), volts, PSI])
        if(volts >= 1.0):
            yar_p.append(PSI)                                
            xar_p.append(i)
            line_p.set_data(xar_p, yar_p)
        ax1_p.set_xlim(0, i+1)
        ax1_p.set_ylim(0, max(yar_p))

    

plotcanvas = FigureCanvasTkAgg(fig, app.master)
plotcanvas.get_tk_widget().grid(column=0, row=1, columnspan=2)

ani = animation.FuncAnimation(fig, animate_l, blit=False, interval=250)

plotcanvas_p = FigureCanvasTkAgg(fig_p, app.master)
plotcanvas_p.get_tk_widget().grid(column=0, row=0, columnspan=2)

ani_p = animation.FuncAnimation(fig_p, animate_p, blit=False, interval=250)

#Harding logo
img = Image.open("/home/pi/Documents/HU-Hybrid-Rocket-Engine-DAQ-Software/Media/HU-Logo.png")
photo = ImageTk.PhotoImage(img)
imgLabel1 = Label(root, image=photo)
imgLabel1.image = photo
imgLabel1.grid(row=0,column=3, sticky=tk.N,ipadx=175,ipady=150)

#Export button
B = Button(root, text ="Export Data", command = writeLoadCellData)
B.grid(row = 0, column=2)

#Only enable this when camera is in use
#camera.startLiveFeed()

root.mainloop()
        