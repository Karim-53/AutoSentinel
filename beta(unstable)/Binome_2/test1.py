import numpy as np
import cv2
import time
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe(prototxt="MobileNetSSD_deploy.prototxt.txt",
                               caffeModel="MobileNetSSD_deploy.caffemodel")
def yahia (image) :
    try :
        image = cv2.imread(image)
        (h,w)=image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image,(300,300)),0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0,detections.shape[2]) :
            JSON =" { " + " object : { "
            confidence = detections[0,0,i,2]
            if confidence > 0.2 :
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                JSON = JSON + format( CLASSES[idx] + ": { " + startX.astype("str") + ","+ startY.astype("str") + ","+ endX.astype("str") + ","+ endY.astype("str") + " }" )
                if ( i != len(detections.shape[1])):
                  JSON = JSON + ","
                else :
                  JSON = JSON + " } "
                print("[INFO] {}".format(JSON))
    except Exception as  e :
        return 0
    return JSON

if __name__ == "__main__":
    image ="images/example_04.jpg"
    a = yahia(image)
    print(a)

