import time
import picamera


with picamera.PiCamera() as camera:
    camera.resolution = (400, 400)
    print('.')
    camera.start_preview()# ne marche que sur du hdmi
##  camera.start_recording('./OnBoard.h264')
    time.sleep(5)
    camera.capture('test3.jpg')