import cv2
from imutils.video import VideoStream
import picamera
import time
import imutils
import datetime

class VideoCamera(object):
	def __init__(self):
		# Using OpenCV to capture from device 0. If you have trouble capturing
		# from a webcam, comment the line below out and use a video file
		# instead.
		self.video = VideoStream(src=0).start()
		time.sleep(2.0)
		self.firstFrame = None
		# If you decide to use video.mp4, you must have this file in the folder
		# as the main.py.
		# self.video = cv2.VideoCapture('video.mp4')
	
	def __del__(self):
		self.video.stop()
	
	def process_image(self):
		frame = self.video.read()
		# frame = frame if args.get("video", None) is None else frame[1]
		text = "Sem Movimentos"

		# if the frame could not be grabbed, then we have reached the end
		# of the video
		# if frame is None:
		# 	break

		# resize the frame, convert it to grayscale, and blur it
		frame = cv2.resize(frame, (500,500), cv2.INTER_AREA)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (9, 9), 0)

		# if the first frame is None, initialize it
		if self.firstFrame is None:
			self.firstFrame = gray

		# compute the absolute difference between the current frame and
		# first frame
		frameDelta = cv2.absdiff(self.firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)

		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < 500:
				continue

			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			text = "Movimento detectado"
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

		# draw the text and timestamp on the frame
		cv2.putText(frame, "Status de Monitoramento: {}".format(text), (10, 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		
		return frame

	def get_frame(self):
		# We are using Motion JPEG, but OpenCV defaults to capture raw images,
		# so we must encode it into JPEG in order to correctly display the
		# video stream.
		image = self.process_image()
#		image = self.video.read()
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()
	
