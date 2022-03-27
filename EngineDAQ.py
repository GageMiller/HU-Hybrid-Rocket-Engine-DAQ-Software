'''
Author: Gage Miller
Description:
This program allows the Harding University Hybrid Rocket engine team
to easily check the status of and collect data from the various sensor
on the engine. It also displays whether the engine control is armed.
The GUI is written in tkinter.
'''
import Components.LoadCell as loadCell
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

#Safe and arm switch GPIO setup
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

#Animates the live matplotlib plot of the load cell
def animate(i):
    value = loadCell.getWeight(5)
    if(not GPIO.input(24)):
        data.append([time.time(), value])
    yar.append(value)
    xar.append(i)
    line.set_data(xar, yar)
    ax1.set_xlim(0, i+1)
    ax1.set_ylim(0, max(yar))
    safeAndArmCheck(imgLabel)

plotcanvas = FigureCanvasTkAgg(fig, app.master)
plotcanvas.get_tk_widget().grid(column=0, row=1, columnspan=2)

ani = animation.FuncAnimation(fig, animate, blit=False, interval=250)

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
        