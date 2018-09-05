# Doit etre lancé avant le GCS
import socket
import time
import picamera
from pprint import pprint


# Connect a client socket to my_server:8000
def SaveStreamOffBoard_DroneSide():
    print(r'Streaming Thread started')
    my_server = '192.168.1.9'
    print(my_server)
    # TODO Créer un obj Autopilot.Cam.Param.StreamPort .StreamIp = 'auto'
    # les drones auront des @ip fixes d'apres le tuteur
    try:
        with picamera.PiCamera() as camera:
            # camera.resolution = (1024, 768)
            camera.framerate = 24
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
                    camera.start_preview()
                    time.sleep(2)
                    # Start recording, sending the output to the connection for 60
                    # seconds, then stop
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
                    # camera.stop_recording()
                except:
                    pass
    except Exception as e:
        print("SaveStream_Erreur:")
        pprint(e)
