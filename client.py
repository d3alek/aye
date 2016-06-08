from picamera import PiCamera
from picamera.array import PiRGBArray
import cv2
import time
import io
import socket
import struct
from fractions import Fraction

millis = lambda: int(round(time.time() * 1000))

def autoExposureLock(camera):
    camera.shutter_speed = 16560 #camera.exposure_speed
    camera.exposure_mode = 'off'
    gain = (Fraction(103, 64), Fraction(447, 256))  # camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = gain
    print("shutter_speed: %s, gain: %s" % (str(camera.exposure_speed), str(gain)))

consumer_socket = socket.socket()
consumer_socket.connect(('172.24.1.1', 8123))
consumer = consumer_socket.makefile('wb')

camera = PiCamera()
resolution = (320, 240)
camera.resolution = resolution
camera.framerate = 60
raw_capture = io.BytesIO()

time.sleep(2)
autoExposureLock(camera)

smoothing = 0.9
average_fps = 0

time.sleep(1)
start = time.time()

try:
    for frame in camera.capture_continuous(raw_capture, format="jpeg", use_video_port=True):

        consumer.write(struct.pack('<L', raw_capture.tell()))
        consumer.write(struct.pack('<Q', millis()))
        consumer.flush()
        raw_capture.seek(0)

        consumer.write(raw_capture.read())
        raw_capture.seek(0)
        raw_capture.truncate(0)

        time_taken = time.time() - start
        current_fps = 1./time_taken
        average_fps = average_fps * smoothing + current_fps * (1 - smoothing)        

        start = time.time()

finally:
    consumer.close()
    consumer_socket.close()

