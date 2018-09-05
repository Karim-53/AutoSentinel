#M1-R001-1


# TODO ajouter un UT (unit test) pour s'assurer que la camera marche
# TODO UT verifier la taille du fichier output !=0 et l'effacer
#                              omxplayer -i RecordingVideo.h264

#convert using shell: MP4Box -add RecordingVideo.h264 filename.mp4

import picamera

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.start_recording('./RecordingVideo.h264')#output = dossier actuel

#		* ``'h264'`` - Write an H.264 video stream
#        * ``'mjpeg'`` - Write an M-JPEG video stream
#        * ``'yuv'`` - Write the raw video data to a file in YUV420 format
#        * ``'rgb'`` - Write the raw video data to a file in 24-bit RGB format
#        * ``'rgba'`` - Write the raw video data to a file in 32-bit RGBA format
#        * ``'bgr'`` - Write the raw video data to a file in 24-bit BGR format
#        * ``'bgra'`` - Write the raw video data to a file in 32-bit BGRA format

#You may find RGB captures rather slow. If this is the case, please try the 'rgba' format instead.

camera.wait_recording(60)
#unlike time.sleep() it will continually check for recording errors
#(e.g. an out of disk space condition) while it is waiting. If we had
#used time.sleep() instead, such errors would only be raised by the stop_recording()
#call (which could be long after the error actually occurred).


camera.stop_recording()

#++
#Recording to a circular stream
#This is similar to Recording video to a stream but uses a special kind of in-memory stream provided by the picamera library. The PiCameraCircularIO class implements a ring buffer based stream, specifically for video recording. This enables you to keep an in-memory stream containing the last n seconds of video recorded (where n is determined by the bitrate of the video recording and the size of the ring buffer underlying the stream).
#3.15. Overlaying text on the output
