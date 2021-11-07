import cv2, threading, time
import RPi.GPIO as GPIO

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        camPreview(self.previewName, self.camID)

def startLiveFeed():
   thread1 = camThread("Camera 1", 0)
   thread1.start()

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))
    
    while(cam.isOpened()):
        ret, frame = cam.read()
        if ret:
            # write the frame
            if(not GPIO.input(24)):
                out.write(frame)

            cv2.imshow(previewName,frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cam.release()
    out.release()
    cv2.destroyWindow(previewName)