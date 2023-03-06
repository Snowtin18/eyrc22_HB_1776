#!/usr/bin/env python3

import socket
import time
import signal		
import sys		
#for coordinates fxn
import cv2
import imutils
from imutils.video import VideoStream
import math
import numpy
from cv_basics.msg import aruco_data
import rospy
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge


#######################Variables#########################################
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



#Initialize the video stream and allow the camera sensor to warm up
rospy.loginfo("[INFO] starting video stream...")

#Initializing publisher and odem message
aruco_publisher = rospy.Publisher('detected_aruco', aruco_data,queue_size=20)#Mention queue size if required
aruco_msg = aruco_data()

###############################FUNCTIONS#########################################

#getting coordinates
def coordinates(arucodictionary,arucoparams,vs):
    #Recieving frame and resize to 500x500
	frame = vs
	# detect ArUco markers in the input frame
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,arucodictionary, parameters=arucoparams)
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
			#Finding the Centroid
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            #Marking the centre
			cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
            #Displaying the ID
			cv2.putText(frame, str(markerID),
	       (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 255, 0), 2)
			#Getting the arena boundries
			if(markerID==4):
				global arenatopright
				arenatopright=topRight
			elif(markerID==8):
				global arenatopleft
				arenatopleft=topLeft
			elif(markerID==10):
				global arenabottomleft
				arenabottomleft=bottomLeft
			elif(markerID==12):
				global arenabottomright
				arenabottomright=bottomRight
			elif(markerID==6):
				global holax,holay,c_edge_x,c_edge_y
				holax=cX
				holay=cY
				c_edge_x = (topLeft[0] + bottomLeft[0]) / 2.0
				c_edge_y = (topLeft[1] + bottomLeft[1]) / 2.0
			else:
				continue				
		#marking the arena border
		cv2.line(frame,arenatopleft,arenatopright,(0,255,0),2)
		cv2.line(frame,arenatopright,arenabottomright,(0,255,0),2)
		cv2.line(frame,arenabottomright,arenabottomleft,(0,255,0),2)
		cv2.line(frame,arenabottomleft,arenatopleft,(0,255,0),2)
        #Getting the coordinates of the bot
		coordx=int(500*(holax-arenabottomleft[0])/(arenabottomright[0]-arenabottomleft[0]))
		coordy=int(500*(holay-arenabottomleft[1])/(arenatopleft[1]-arenabottomleft[1]))
		theta = (math.atan2((holay-c_edge_y),(holax-c_edge_x)))
		theta=-theta
		originalcoord=str(coordx)+","+str(coordy)+","+str(theta)
		#Display coordinates
		cv2.putText(frame, originalcoord,
	       (holax, holay), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, (0, 255, 0), 2)
		#cropping the arena from the frame and displaying it
		frame = frame[arenatopleft[1]:arenabottomleft[1], arenabottomleft[0]:arenabottomright[0]]
		cv2.imshow("Frame",frame)
		cv2.waitKey(1)
		#Aruco message to be published
		aruco_msg.x = coordx
		aruco_msg.y = coordy
		aruco_msg.theta = theta
        #Publishing aruco msgs
		aruco_publisher.publish(aruco_msg)
		return originalcoord
	
def callback(data):
	br = CvBridge()
	get_frame = br.imgmsg_to_cv2(data, "mono8")
	current_frame = cv2.resize(get_frame, (1000, 1000), interpolation = cv2.INTER_LINEAR)
	rospy.loginfo("Recieving camera feed")
	ARUCODICTIONARY = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_250"])
	ARUCOPARAMS = cv2.aruco.DetectorParameters_create()
	coord=coordinates(ARUCODICTIONARY,ARUCOPARAMS,current_frame)
	rospy.loginfo(coord)
	
	

###########################################MAIN#############################################################

def main():
	rospy.init_node('Aruco_feedback_node')
	rospy.Subscriber('/usb_cam/image_raw',Image,callback)
	rospy.spin()

	
if __name__=='__main__':
	main()
	
    
