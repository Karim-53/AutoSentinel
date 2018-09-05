#Doit etre lancé avant le GCS
import socket
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)

# TODO Créer un obj Autopilot.Cam.Param.StreamPort .StreamIp = 'auto'
# TODO automatiser la selection de l'@ip
my_server = '192.168.1.9'

client_socket = socket.socket()
client_socket.connect((my_server, 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
print('start')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        # Start recording, sending the output to the connection for 60
        # seconds, then stop
        camera.start_recording(connection, format='h264')
        camera.wait_recording(20)
        camera.stop_recording()
finally:
    connection.close()
    client_socket.close()
