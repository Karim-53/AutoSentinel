import numpy as np
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import cv2
# Ceci les differentes classes dans notre classifieurs
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
# Ceci génere les differentes coulours de façon aléatoire
# 	Draw samples from a uniform distribution.
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
#TODO: A tester avec le cfg YOLOv3

#net = cv2.dnn.readNetFromDarknet(cfgFile="yolov3.cfg",darknetModel="yolov3.weights")
net = cv2.dnn.readNetFromCaffe(prototxt="MobileNetSSD_deploy.prototxt.txt",
                               caffeModel="MobileNetSSD_deploy.caffemodel")
# On lit maintenant l'image
#TODO : Utiliser le frame / video
#image = cv2.imread("images/example_02.jpg")
#(h,w)=image.shape[:2];
# TODO : Detection Deep learning Video
vs = VideoStream(src=0).start()
fps = FPS().start() 
while True :
    image = vs.read()
    image = imutils.resize(image, width=400)
    h,w = image.shape[:2] 
    #What's a blob is a group of pixels sharing a number of proprity
    blob = cv2.dnn.blobFromImage(image,0.007843, (300, 300), 127.5)
    # Tout est prét pour la detection , on passe le blob dans le réseau
    net.setInput(blob)
    #  the .forward method is used to forward-propagate
    # our image and obtain the actual classification.
    detections = net.forward()

    for i in np.arange(0,detections.shape[2]) :
        confidence = detections[0,0,i,2]
        if confidence > 0.2 :
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("[INFO] {}".format(label))
            # Dessiner le triangle
            cv2.rectangle(image, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    cv2.imshow("Video", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
fps.update()
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destryAllWindows()
vs.stop()




