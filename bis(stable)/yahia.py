import numpy as np
import cv2
import subprocess
import time
import picamera
from pprint import pprint
from picamera.array import PiRGBArray

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe(prototxt="MobileNetSSD_deploy.prototxt.txt",
                               caffeModel="MobileNetSSD_deploy.caffemodel")
def yahia () :
    global camera
    
    with picamera.PiCamera() as camera:
        camera.vflip = True
        camera.resolution = (400, 400)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        print("cap")
        camera.capture('capture.jpg')
        Stream = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(Stream,format="bgr")
        imm=Stream.array
        #pprint(imm)
        
        print("ok")
        
    #subprocess.Popen(["raspistill","-w","400","-h","400","-o","capture.jpg"],stdout=subprocess.PIPE)
    
    print("..")
    #image = cv2.imread("capture.jpg")
    image = imm
    
    #pprint(image)
    (h,w)=image.shape[:2]
    print("..1")
    blob = cv2.dnn.blobFromImage(cv2.resize(image,(300,300)),0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    JSON =" { "+'" object"' +":{ "
    for i in np.arange(0,detections.shape[2]) :
      
        confidence = detections[0,0,i,2]
        if confidence > 0.2 :
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            JSON = JSON + format( '"'+CLASSES[idx]+'"' + ":[" + startX.astype("str") + ","+ startY.astype("str") + ","+ endX.astype("str") + ","+ endY.astype("str") + "]" )
            if ( i in np.arange (0,detections.shape[2]-1 ) ):
              JSON = JSON + ","
            else :
                JSON = JSON + "}"
            print("[INFO] {}".format(JSON))
    JSON = JSON + "}"    
    return JSON

if __name__ == "__main__":
    a= yahia()
    print(a) 



