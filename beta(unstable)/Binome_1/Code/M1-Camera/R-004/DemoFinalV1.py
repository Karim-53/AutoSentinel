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
from SaveStreamOffBoard_DroneSide import *
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


############################## MAIN
# todo++ while 3al kol

# TODO
# init algo background
# while no anomalie
# capture vid duree DureeVid
# lance algo background
# }


# todo++ decoup img autour de l'anomalie pour la classifier
try:
    Thread(target=SaveStreamOffBoard_DroneSide).start()
    PlaySound("Start.mp3")
    print("TabaaTaswira()")
    while True:
        TabaaTaswira()
        print("loop")
except Exception as e:
    print("Erreur:")
    pprint(e)
