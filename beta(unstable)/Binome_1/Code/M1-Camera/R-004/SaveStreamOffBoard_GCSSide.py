import socket
import subprocess
import os
import time
from pprint import pprint
###############################


defaultTimeout = 1
SleepBeforeNewTentative = 1

########################################################################################################
def Camera_Cx():
   "établir la connexion avec la camera"
   print("Cx to camera...")

   #DroneIp = '192.168.1.7' # FIXME Cx au drone avec une @ fixe ne marche pas
   # TODO ping DroneIp before establiching connection
   connection=0
   server_socket=0
   try:
       # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0) means all interfaces)
       server_socket = socket.socket()
       print("1/4")
       server_socket.bind(('0.0.0.0', 8000))
       print("2/4")
       server_socket.listen(0)
       print("3/4")

       # Accept a single connection and make a file-like object out of it
       connection = server_socket.accept()[0].makefile('rb')
       print("4/4")
   except Exception as e:
       print("server_socket err:")
       pprint(e)
       try:
           print('a')
           connection.close()
       except Exception:
           pass
       try:
           server_socket.close()
       except Exception:
           pass
       #return 0,0
   finally:
       return connection,server_socket


def Camera_RunPlayer():
    "lancer le streaming OffBoard"
    player = 0
    try:
        # Run a viewer with an appropriate command line.
        # FIXME [0000000002e58520] core libvlc: Lancement de vlc avec l'interface par d�faut. Utilisez ��cvlc�� pour d�marrer VLC sans interface.
        # FIXME [0000000004a2b810] core input error: Invalid PCR value in ES_OUT_SET_(GROUP_)PCR !
        StreamingCmdLine = [r'C:\Program Files\VideoLAN\VLC\vlc.exe', '--demux', 'h264', '-']
        #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-'] #Uncomment the mplayer version if you would prefer to use mplayer instead of VLC
        player = subprocess.Popen(StreamingCmdLine, stdin=subprocess.PIPE)
    except Exception as e:
        print("Erreur lors de l'ouverture du VLC")
        pprint(e)
    finally:
        return player
########################################################################################################






socket.setdefaulttimeout(defaultTimeout) #print(socket.getdefaulttimeout())
connection = 0
server_socket = 0

while True:
    try:
        connection,server_socket = Camera_Cx()
        pprint(connection)
        if not connection:
            print("Erreur lors de la connexion au drone")
            time.sleep(SleepBeforeNewTentative)
            continue

        player = 0
        fVideoOffBoard = 0
        while True:
            # Repeatedly read 1Kb of data from the connection and write it to
            data = connection.read(1024)
            if not data:
                break
            if player:
                player.stdin.write(data)
            else:
                player = Camera_RunPlayer()
            if fVideoOffBoard:
                fVideoOffBoard.write(data)
            else:
                # TODO Manage file: chaque jour un fichier ?
                fVideoOffBoard = open(os.getcwd() + r'\OffBoard.h264', 'ab')
                # ab: appending in binary format. The file pointer is at the end of the file if the file exists.
                # That is, the file is in the append mode. If the file does not exist, it creates a new file for writing.
        player.terminate()# FIXME may rise exeption
        fVideoOffBoard.close()# FIXME may rise exeption
    except Exception as e:
        print("GCS err:")
        pprint(e)