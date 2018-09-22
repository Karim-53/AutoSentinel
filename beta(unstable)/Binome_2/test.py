import sys , os
import threading
import darknet as dn
def tread(image):
    print ( "**********Dection Background********** ")
    net = dn.load_net(b"yolov3.cfg", b"yolov3.weights", 0)
    meta = dn.oad_meta("coco.data")
    r = dn.detect(net, meta, self.image)
    print ("****** Background Detection Finished ********")
t = threading.Thread(name="papa0",target=tread())
t.start()
print("papa")