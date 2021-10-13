#import LoadCell
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv, time
import cv2

class window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
root = Tk()
app = window(master=root)
app.master.geometry('1200x700+200+100')
app.master.title("Hybrid Rocket Engine Data Acquisition Software")
#loadCellTxt = Label(root, text="Load Cell")
#loadCellTxt.pack()

xar = []
yar = []

style.use('ggplot')
fig = plt.figure(figsize=(14, 4.5), dpi=100)
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_ylim(0, 100)
line, = ax1.plot(xar, yar, 'r', marker='o')
#ser = serial.Serial('com3', 9600)

def animate(i):
    #ser.reset_input_buffer()
    #data = ser.readline().decode("utf-8")
    #data_array = data.split(',')
    #yvalue = float(data_array[1])
    yar.append(99-i)
    xar.append(i)
    line.set_data(xar, yar)
    ax1.set_xlim(0, i+1)


plotcanvas = FigureCanvasTkAgg(fig, app.master)
plotcanvas.get_tk_widget().grid(column=1, row=1)
ani = animation.FuncAnimation(fig, animate, interval=1000, blit=False)

root.mainloop()