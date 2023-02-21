#!/usr/bin/env python3

import cv2	
import numpy
import imutils
from imutils.video import VideoStream
import argparse
import sys
import time
import socket
import signal	

def signal_handler(sig, frame):
    print('Clean-up !')
    cleanup()
    sys.exit(0)

def cleanup():
    s.close()
    print("cleanup done")

ip = ""     #Enter IP address of laptop after connecting it to WIFI hotspot

ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
	default="DICT_ARUCO_ORIGINAL",
	help="DICT_4X4_250")
args = vars(ap.parse_args())


if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(
		args["type"]))
	sys.exit(0)
print("[INFO] detecting '{}' tags...".format(args["type"]))
#initializing detector parameters
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(2).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 1000 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=1000)
	# detect ArUco markers in the input frame
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,arucoDict, parameters=arucoParams)
	if(len(corners)>0):
		ids = ids.flatten()
		for (markerCorner, markerID) in zip(corners, ids):
			corners = markerCorner.reshape((4, 2))
			(topLeft,topRight,bottomRight,bottomLeft) = corners

			topRight = (int(topRight[0]), int(topRight[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))
			#Marking the marker and its center
			cv2.line(frame,topLeft,topRight,(0,255,0),2)
			cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
			cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
			cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
			#coordinates="x:"+str(cX)+" y:"+str(cY)

			cv2.putText(frame, str(markerID),
	       (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 255, 0), 2)
			#getting the arena boundries
			if(markerID==4):
				arenatopright=topRight
			elif(markerID==8):
				arenatopleft=topLeft
			elif(markerID==10):
				arenabottomleft=bottomLeft
			elif(markerID==12):
				arenabottomright=bottomRight
			elif(markerID==6):
				holax=cX
				holay=cY
			else:
				continue				
			print("[INFO] ArUco marker ID: {}".format(markerID))
		#marking the arena border
		cv2.line(frame,arenatopleft,arenatopright,(0,255,0),2)
		cv2.line(frame,arenatopright,arenabottomright,(0,255,0),2)
		cv2.line(frame,arenabottomright,arenabottomleft,(0,255,0),2)
		cv2.line(frame,arenabottomleft,arenatopleft,(0,255,0),2)
		print("BL:",arenabottomleft)
		print("TL:",arenatopleft)
		print("TR:",arenatopright)
		print("BR:",arenabottomright)
		#cropping the frame to focus the arena
		frame = frame[int(arenatopleft[1]):int(arenabottomright[1]), int(arenabottomleft[0]):int(arenatopright[0])]
		#resizing the 500x500 pixels
		frame = imutils.resize(frame, width=500,height=500)
		#detecting markers in cropped frame to get coordinates in resized frame
		(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,arucoDict, parameters=arucoParams)
		ids=ids.flatten()
		idindex=ids.index("6")
		id6corners=corners[idindex]
		corners = id6corners.reshape((4, 2))
		#Getting corners of ID:6  
		(htopLeft,htopRight,hbottomRight,hbottomLeft) = corners
		htopRight = (int(htopRight[0]), int(htopRight[1]))
		hbottomRight = (int(hbottomRight[0]), int(hbottomRight[1]))
		hbottomLeft = (int(hbottomLeft[0]), int(hbottomLeft[1]))
		htopLeft = (int(htopLeft[0]), int(htopLeft[1]))
		#center of ID:6
		holax = int((htopLeft[0] + hbottomRight[0]) / 2.0)
		holay = int((htopLeft[1] + hbottomRight[1]) / 2.0)
		coordinates="x:"+str(holax)+" y:"+str(holay)
		print(coordinates)
		cv2.putText(frame, coordinates,
	       (holax, holay), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 255, 0), 2)
		cv2.imshow("Frame",frame)	
		with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
			s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			s.bind((ip,8002))
			s.listen()
			conn,addr=s.accept()
			with conn:
				print(f"Connected by {addr}")
				data=conn.recv(1024)
				print(coordinates)
				print(data)
				conn.sendall(str.encode(str(coordinates)))
				time.sleep(1)
				s.close()
				
		key=cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
	
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

