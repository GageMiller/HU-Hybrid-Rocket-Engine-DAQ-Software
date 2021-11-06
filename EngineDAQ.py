import Components.LoadCell as loadCell
import Components.Camera as camera
import Components.Ignition as Ignition
from tkinter import *
import tkinter as tk
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv, time
from PIL import Image, ImageTk
import RPi.GPIO as GPIO


class window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

firstRun = True
root = Tk()
app = window(master=root)
app.master.geometry('1920x1080+0+0')
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

def animate(i):
    value = loadCell.getWeight(5)
    yar.append(value)
    xar.append(i)
    line.set_data(xar, yar)
    ax1.set_xlim(0, i+1)
    ax1.set_ylim(0, max(yar))
    #Data Saving
    if(GPIO.input(24)):
        with open('load_cell_data.csv', mode='w') as load_cell_data:
            load_cell_writer = csv.writer(load_cell_data, delimiter=',', quotechar='=', quoting=csv.QUOTE_MINIMAL)
            load_cell_writer.writerow([time.time(), value])

plotcanvas = FigureCanvasTkAgg(fig, app.master)
plotcanvas.get_tk_widget().grid(column=0, row=1, columnspan=2)
ani = animation.FuncAnimation(fig, animate, interval=100, blit=False)

img = Image.open("/home/pi/Documents/HU-Hybrid-Rocket-Engine-DAQ-Software/Media/HU-Logo.png")
photo = ImageTk.PhotoImage(img)
imgLabel = Label(root, image=photo)
imgLabel.image = photo
imgLabel.grid(row=0,column=3, sticky=tk.N,ipadx=175)

#Safe and Arm Check
if(GPIO.input(24)):
    img = Image.open("/home/pi/Documents/HU-Hybrid-Rocket-Engine-DAQ-Software/Media/Green.png")
    photo = ImageTk.PhotoImage(img)
    imgLabel = Label(root, image=photo)
    imgLabel.image = photo
    imgLabel.grid(row=2,column=3, ipadx=175)
else:
    img = Image.open("/home/pi/Documents/HU-Hybrid-Rocket-Engine-DAQ-Software/Media/Red.png")
    photo = ImageTk.PhotoImage(img)
    imgLabel = Label(root, image=photo)
    imgLabel.image = photo
    imgLabel.grid(row=2,column=3, ipadx=175)

label1 = Label(root)
label2 = Label(root)
label1.grid(row=0, column=0)
label2.grid(row=0, column=1)

if(firstRun == True):
    camera.startThreads(label1, label2)
    firstRun = False

root.mainloop()