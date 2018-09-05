# il faut d'abord lancer le script
# et ensuite, lancer le flux avec vlc
# tcp/h264://my_pi_address:8000/

# TODO lancer un thread pour l'envoi auto d'@ip   hostname -I
# TODO ptet faire n unit test pour verif 
import socket
import time
import picamera

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('wb')
# TODO : ajouter un time out au cas ou personne ne lance de requete GET vers la Pi
try:
    camera.start_recording(connection, format='h264')
    camera.wait_recording(60)
    camera.stop_recording()
finally:
    connection.close()
    server_socket.close()