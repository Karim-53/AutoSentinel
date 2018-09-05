#Doit etre lancé avant le GCS
#ne marche tj pas
import socket
import time

# Connect a client socket to my_server:8000
my_server = '192.168.1.9'



# TODO ajouter un bloc try
print(r'client_socket.connect')
client_socket = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
client_socket.bind((host, port))        # Bind to the port

# Make a file-like object out of the connection
print(r'connection')
connection = client_socket.makefile('wb')
print(r'start')
try:
    f = open(r"C:\Users\Karim\Google Drive\AAA\Projet Piste 10\Exemple\OnBoard.h264","rb")
    while True:
        data = f.read(1024)
        if not data:
            break
        connection.write(data)
        time.sleep(1)
        print(data)

finally:
    pass
try:
    connection.close()
    client_socket.close()
except:
    pass