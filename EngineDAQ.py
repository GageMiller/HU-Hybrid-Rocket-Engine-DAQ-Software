import Components.LoadCell as loadCell
import Components.Camera as camera
import Components.Ignition as Ignition
from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv, time
import cv2
from PIL import Image, ImageTk


class window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
 
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

def animate(i):
    value = loadCell.getWeight(5)
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

label = Label(root)
label.grid(row=0, column=0)
cap= cv2.VideoCapture(0)

def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)

show_frames()

root.mainloop()