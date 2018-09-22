import sys , os
import threading
import subprocess
import time
import  cv2
import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import imutils


class DetectBackground(threading.Thread):
    def __init__(self , imagePath):
        threading.Thread.__init__(self)
        self.image = imagePath
    def run(self):
        print ( "**********Dection Background********** ")
        subprocess.Popen(["./darknet","detect","cfg/yolov3.cfg","yolov3.weights",self.image.encode("utf-8")],stdout=subprocess.PIPE)
        print ("****** Background Detection Finished ********")
        time.sleep(50000)
        return 0
def Main() :

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]

    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe(prototxt="MobileNetSSD_deploy.prototxt.txt",
                                   caffeModel="MobileNetSSD_deploy.caffemodel")
    vs = VideoStream(src=0).start()
    fps = FPS().start()
    cout = 0
    path =os.getcwd()
    while True :
        image = vs.read()
        imagepath = path+"/frame.png"
        imagepath = path+"/frame.png"
        cv2.imwrite(imagepath,image)
        image = imutils.resize(image, width=400)
        h,w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image,0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0,detections.shape[2]) :
            confidence = detections[0,0,i,2]
            if confidence > 0.2 :
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                cv2.rectangle(image, (startX, startY), (endX, endY),
                              COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
        cv2.imshow("Video", image)
        fps.update()
        cout += 1
        if ( cout == 100 ):
            # Background Thread
            background = DetectBackground((imagepath).encode("utf-8"))
            background.start()
            print("Yaya so cool")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            background.join()
            break
        fps.stop()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    Main()