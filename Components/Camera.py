from PIL import Image, ImageTk
import cv2, threading, time

class camThread(threading.Thread):
    def __init__(self, name, camID, label):
        threading.Thread.__init__(self)
        self.name = name
        self.camID = camID
        self.label = label
    def run(self):
        camera = cv2.VideoCapture(self.camID)
        show_frames(self.name, camera, self.label)

def startThreads(label1, label2):
   thread1 = camThread("Camera 1", 0, label1)
   thread2 = camThread("Camera 2", 2, label2)
   thread1.start()
   thread2.start()

def show_frames(name, camera, label):
    while camera.isOpened():
        # Get the latest frame and convert into Image
        cv2image= cv2.cvtColor(camera.read()[1],cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image = img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        # Repeat after an interval to capture continiously
        #label.after(20, show_frames(name, camera, label))
    #show_frames(name, camera, label)



