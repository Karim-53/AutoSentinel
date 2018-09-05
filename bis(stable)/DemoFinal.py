import socket
import threading
from threading import Thread
import json
import time
import picamera
from pprint import pprint
import datetime
import subprocess
import pygame
import os
from yahia import *
from codekarim import *
from SaveStreamOffBoard_DroneSide import *
import numpy as np
import cv2
from picamera.array import PiRGBArray

print("Doit etre lancé avant le GCS")
my_server = '192.168.1.6'


PyYahia = "yahia.py"
imgW = 416
imgH = 400

LongeurMin = imgH * 1 / 3
LongeurMax = imgH * 2 / 3


def PlaySound(name):
    "Play a sound"
    print(name)
    pygame.mixer.music.load(name)
    pygame.mixer.music.play()
    return
    while pygame.mixer.music.get_busy() == True:
        continue
    return []


def TabaaTaswira():
    try:
        data = json.loads(yahia())
        print("_")
        print(json.dumps(data[" object"]))
        print(json.dumps(data[" object"]["bottle"]))
        val = data[" object"]["bottle"]
        # get bottle x1 y1 x2 y2
        x1 = val[0]
        y1 = val[1]
        x2 = val[2]
        y2 = val[3]

        #print((x1 + x2) / 2)
        #print((4 / 5) * imgW)
        # if not (x1+x2)/2 between (2/5)*W et (4/5)*W
        # turn 3ala ro7ek, continue
        if (x1 + x2) / 2 < (2.0 / 5.0) * imgW:
            PlaySound("RotateLeft.mp3")
            return

        if (x1 + x2) / 2 > (4.0 / 5.0) * imgW:
            PlaySound("RotateRight.mp3")
            return

        if y2 - y1 < LongeurMin:
            PlaySound("Avance.mp3")
            return

        if y2 - y1 > LongeurMax:
            PlaySound("Recule.mp3")
            return
        # else: dour 3leha
        PlaySound("TurnAround.mp3")
        return

    except Exception as e:
        print("YahiaExeption:")
        pprint(e)
        print("je voix rien<---------------------------")
        return


# Connect a client socket to my_server:8000
def SaveStreamOffBoard_DroneSide():
    global camera
    print(r'Streaming Thread started')
    print(my_server)
    # TODO Créer un obj Autopilot.Cam.Param.StreamPort .StreamIp = 'auto'
    # les drones auront des @ip fixes d'apres le tuteur
    try:
        
            # camera.resolution = (1024, 768)
            # camera.start_recording('./OnBoard.h264')

            while True:
                # TODO ajouter un bloc try
                print(r'client_socket.connect')
                client_socket = socket.socket()
                client_socket.connect((my_server, 8000))
                # Make a file-like object out of the connection
                print(r'connection')
                connection = client_socket.makefile('wb')
                print(r'start')
                try:
                    # camera.resolution = (640, 480)
                    # camera.framerate = 24
                    # Start a preview and let the camera warm up for 2 seconds
                    #camera.start_preview()
                    #time.sleep(2)
                    # Start recording, sending the output to the connection for 60
                    # seconds, then stop
                    camera.start_recording(connection, format='h264', splitter_port=2, resize=(320, 240))
                    try:
                        while True:
                            camera.wait_recording(10, splitter_port=2)
                            #time.sleep(10)
                    except Exception as e:
                        print("SaveStream_Erreur_2:")
                        pprint(e)
                    camera.stop_recording(splitter_port=2)
                finally:
                    pass
                try:
                    connection.close()
                    client_socket.close()
                    # camera.stop_recording()
                except:
                    pass
    except Exception as e:
        print("SaveStream_Erreur:")
        pprint(e)
        

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv2.dnn.readNetFromCaffe(prototxt="MobileNetSSD_deploy.prototxt.txt",
                               caffeModel="MobileNetSSD_deploy.caffemodel")
def yahia () :
    global camera
    time.sleep(0.5)
    camera.start_preview()
    # Camera warm-up time
    time.sleep(1)
    print("cap")
    #camera.capture('capture.jpg')
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
############################## MAIN
# todo++ while 3al kol

# TODO
# init algo background
# while no anomalie
# capture vid duree DureeVid
# lance algo background
# }


# todo++ decoup img autour de l'anomalie pour la classifier
malek_gentleman()

# Force le son sur le port Jack 3.5"
os.system("sudo amixer cset numid=3 1")
pygame.mixer.init()
#chbik bara degage 5an nkamel ne5dem, t7eb tchouf el 5edma ? n7ebech demain :p
try:
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.resolution = (imgW, imgH)
    camera.framerate = 24
    
    Thread(target=SaveStreamOffBoard_DroneSide).start()
    
    PlaySound("Start.mp3")
    print("TabaaTaswira()")
    while True:
        TabaaTaswira()
        print("loop")
except Exception as e:
    print("Erreur:")
    pprint(e)
