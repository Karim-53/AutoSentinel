import socket
import json
import time
import picamera
from pprint import pprint
import datetime
import subprocess
import pygame
import os
from yahia import *

# ip du serveur my_server:8000
my_server = '192.168.1.9'

print("Doit etre lancé avant le GCS")

# Force le son sur le port Jack 3.5"
os.system("sudo amixer cset numid=3 1")
pygame.mixer.init()

PyYahia = "yahia.py"
imgW = 400
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
    output = ""
    # ImgFileName = str(datetime.datetime.now()) + ".png"
    # camera.capture(ImgFileName)
    # lance la classification
    # data = json.loads(yahia(ImgFileName))
    # data = json.loads("{ \" object\":{\"chair\": [10, -8, 377, 393], \"diningtable\": [0, 1, 399, 399], \"bottle\": [153, 3, 350, 283]}}")
    try:
        data = json.loads(yahia())
        print("_")
        print(json.dumps(data[" object"]))
        print(json.dumps(data[" object"]["bottle"]))
        # for key, val in data[" object"]:
        #    print(json.dumps(key))
        #    if key=="bottle":
        #        print(val)
        val = data[" object"]["bottle"]
        # TODO get bottle x1 y1 x2 y2
        x1 = val[0]
        y1 = val[1]
        x2 = val[2]
        y2 = val[3]

        print((x1 + x2) / 2)
        print((4 / 5) * imgW)
        # if not (x1+x2)/2 between (2/5)*W et (4/5)*W
        # turn 3ala ro7ek, continue
        if (x1 + x2) / 2 < (2.0 / 5.0) * imgW:
            # RotateLeft.mp3
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


############################## MAIN
# les drones auront des @ip fixes d'apres le tuteur
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (400, 400)
        camera.framerate = 30
        camera.start_recording('./OnBoard.h264')

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
                #camera.start_preview()
                #time.sleep(2)
                camera.start_recording(connection, format='h264', splitter_port=2, resize=(320, 240))
                try:
                    while True:
                        camera.wait_recording(10)
                except Exception as e:
                    print("Erreur:")
                    pprint(e)
                camera.stop_recording(splitter_port=2)
            finally:
                pass
            try:
                connection.close()
                client_socket.close()
                camera.stop_recording()
            except:
                pass
except Exception as e:
    print("Erreur:")
    pprint(e)

# todo++ while 3al kol

# TODO
# init algo background
# while no anomalie
# capture vid duree DureeVid
# lance algo background
# }


# todo++ decoup img autour de l'anomalie pour la classifier
try:
    # with picamera.PiCamera() as camera:
    #    camera.resolution = (imgW, imgH)
    #    camera.framerate = 30
    # camera.start_preview()
    # time.sleep(2) # Camera warm-up time
    PlaySound("Start.mp3")
    print("TabaaTaswira()")
    while True:
        TabaaTaswira()
        print("loop")
except Exception as e:
    print("Erreur:")
    pprint(e)
