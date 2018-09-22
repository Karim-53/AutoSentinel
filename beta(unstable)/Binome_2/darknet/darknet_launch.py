import subprocess , sys
proc = subprocess.Popen(["./darknet","detect","cfg/yolov3.cfg","yolov3.weights","data/a.jpg"],stdout=subprocess.PIPE)

