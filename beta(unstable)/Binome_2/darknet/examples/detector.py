# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care

import sys, os
sys.path.append("/home/ubuntu/darknet/python")

import darknet as dn
import pdb

dn.set_gpu(0)
net = dn.load_net(b"/home/ubuntu/darknet/cfg/yolov3.cfg", b"/home/ubuntu/darknet/yolov3.weights", 0)
meta = dn.load_meta(b"/home/ubuntu/darknet/cfg/coco.names")
r = dn.detect(net, meta, "data/bedroom.jpg")
print (r)

# And then down here you could detect a lot more images like:
r = dn.detect(net, meta, "data/eagle.jpg")
print (r)
r = dn.detect(net, meta, "data/giraffe.jpg")
print (r)
r = dn.detect(net, meta, "data/horses.jpg")
print (r)
r = dn.detect(net, meta, "data/person.jpg")
print (r)

