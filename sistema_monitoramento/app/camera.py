import cv2
import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera = PiCamera()
        camera.framerate = 16
        self.rawCapture = PiRGBArray(camera, size=tuple(640, 480))
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        #self.video.release()
        print('del')
    
    def get_frame(self):
        image = self.camera.capture('image.jpeg')
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        return image.tobytes()