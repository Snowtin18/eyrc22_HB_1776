#!/usr/bin/env python3


# Team ID:eYRC#HB#1776	
# Author List:Dhanvantraj M, Vinoth B, Winston Doss, Madhusudhanan K		
# Filename:		finalcontroller.py
#Theme:		Hola bot
#Functions: signal_handler, cleanup, endSignalCb, coordgen, graphgen, velocity,main

################### IMPORT MODULES #######################
import socket
import time
import signal		# To handle Signals by OS/user
import sys		
#for coordinates fxn
import cv2
import imutils
from imutils.video import VideoStream
import math
import numpy
from cv_basics.msg import aruco_data
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32

############################ Global Variables##################################

ip = ""     #Enter IP address of laptop after connecting it to WIFI hotspot

k=0
t=1

finalvel='x:'+str(0.00)+' y:'+str(0.00)+' z:'+str(0.00)
prev_vel_x,prev_vel_y,prev_vel_z=0,0,0

velocityPub=rospy.Publisher('/velocity',String,queue_size=10)
velData=String()

contourPub = rospy.Publisher('/contours', String, queue_size=10)
cData = String()

taskStatusPub = rospy.Publisher('/taskStatus', Int32, queue_size=10)
taskStatus = Int32()

penPub = rospy.Publisher('/penStatus', Int32, queue_size=10)
penData = Int32()


taskStatus.data = 0   #indicating start of the run
penData.data=0        #Indicating pen pulled up


#############################Functions##################################

def signal_handler(sig, frame):
    print('Clean-up !')
    cleanup()
    sys.exit(0)

def cleanup():
    global s
    s.close()
    print("cleanup done")

def endSignalCb(status):
	if(status.data):
		cleanup()

#coordinates generating f 
def coordgen(img_location):
	img = cv2.imread(img_location, cv2.IMREAD_UNCHANGED)
	img=imutils.resize(img,width=500,height=500)
	#convert to grey
	img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#fix threshhold
	thresh = 100
	ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
	#extract contours
	contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	global x_dL
	global y_dL
	global theta_dL
	global t

	global xListFinal
	global yListFinal
	global thetaListFinal


	x_dL=[]
	y_dL=[]
	theta_dL=[]
	i=0
	xList , yList , thetaList, xListFinal , yListFinal, thetaListFinal = [] , [] , [] , [], [], []

	for i in contours:  
		xList.clear()    
		yList.clear()
		for j in i:
			xList.append(int(j[0][0]))
			yList.append(int(j[0][1]))
			thetaList.append(0)
		xListFinal.append(xList)
		yListFinal.append(yList)
		thetaListFinal.append(thetaList)
	cData.data = str([xListFinal,yListFinal])
	contourPub.publish(cData)

	x_dL,y_dL,theta_dL=xListFinal[t],yListFinal[t],thetaListFinal[t]

	'''x_dL=[350,150,150,350]
	y_dL=[300,300,150,150]
	theta_dL=[0,0,0,0]'''

	'''for i in range(0,len(contours[1]),14):
		x_dLval=contours[1][i][0][0]
		y_dLval=500-(contours[1][i][0][1])
		x_dL.append(x_dLval)
		y_dL.append(y_dLval)
		theta_dL.append(0)'''

#graph generating 	
def graphgen():
	global x_dL
	global y_dL
	global theta_dL
	
	x_dL=[]
	y_dL=[]
	theta_dL=[]
	t=0
	while(t<=2*math.pi):
	
		x = 200*math.cos(t)
		y = 100*math.sin(2*t)
		theta = (math.pi/4)*math.sin(t)
		
		x+=250
		y+=250

		x_dL.append(x)
		y_dL.append(y)
		theta_dL.append(theta)
		
		t+=0.15

#velocity calculation

def velocity(msg):
	rospy.loginfo("Velocity function started execution")
	#x_dL,y_dL,theta_dL=coordgen('/home/winston/catkin_ws/src/hola_bot/scripts/snapchat.png')

	global k
	global t
	global prev_vel_x
	global prev_vel_y
	global prev_vel_z
	global finalvel
	global x_dL
	global y_dL
	global theta_dL
	global xListFinal
	global yListFinal
	global thetaListFinal

	holax=msg.x
	holay=msg.y
	theta=msg.theta

	x_d=x_dL[k]
	y_d=y_dL[k]
	theta_d=theta_dL[k]
	rospy.loginfo("x_d:{},y_d:{},theta_d:{}".format(x_d,y_d,theta_d))
	rospy.loginfo("x:{},y:{},theta:{}".format(holax,holay,theta))
	# Calculate Error from feedback
	ex=x_d-(holax)
	ey=y_d-(holay)
	etheta=((theta)-(theta_d))

	# Change the frame by using Rotation Matrix (If you find it required)
	betheta=(etheta)
	bex=(ex*math.cos(round(theta,1))+ey*math.sin(round(theta,1)))
	bey=ey*math.cos(round(theta,1))-ex*math.sin(round(theta,1))
	rospy.loginfo("bex:{},bey:{},betheta:{}".format(bex,bey,betheta))

	# Calculate the required velocity of bot for the next iteration(s)
	vel_x=6*bex#-0.5*(prev_vel_x)
	vel_y=6*bey #- 0.5*(prev_vel_y)
	vel_z=30*betheta #- 0.5*(prev_vel_z)
	#rospy.loginfo("vel_x:{},vel_y:{},vel_z:{}".format(vel_x,vel_y,vel_z))
	# Find the required force vectors for individual wheels from it.(Inverse Kinematics)
	uf=(vel_z+vel_x)/2
	ur=vel_z-(vel_x/2)-((math.sqrt(3)/2)*vel_y)
	ul=vel_z-(vel_x/2)+((math.sqrt(3)/2)*vel_y)
	rospy.loginfo("uf:{},ur:{},ul:{}".format(uf,ur,ul))
	uf=-uf
	ur=-ur
	ul=-ul

	prev_vel_x=vel_x
	prev_vel_y=vel_y
	prev_vel_z=vel_z

	#finalvel='x:'+str(round(ul,2))+' y:'+str(round(uf,2))+' z:'+str(round(ur,2))
	finalvel='x:'+str(round(ur,2))+' y:'+str(round(uf,2))+' z:'+str(round(ul,2))
	#finalvel='x:'+str(round(uf,2))+' y:'+str(round(ur,2))+' z:'+str(round(ul,2))
	#rospy.loginfo("hiii"+finalvel)

	# Modify the condition to Switch to Next goal (given position in pixels instead of meters)
	if(((abs(ex)-3)<=0) and ((abs(ey)-3)<=0) and ((abs(etheta)-0.5)<=0)):
		uf=0
		ur=0
		ul=0
		if(k==0):
			print("Pen pull down")#Write code for pen pull down
			penData.data=1 #Indicating pen pulled down
		k+=14
		if(k>=(len(x_dL))):
			#endsig=0
			#taskStatus.data=1
			#taskStatusPub.publish(taskStatus.data)
			t+=1
			k=0
			print("Pen pull up")
			penData.data=0 #Indicating pen pulled up
			#Pen pull up
			if(t>=(len(xListFinal))):
				taskStatus.data=1
				taskStatusPub.publish(taskStatus.data)
				rospy.signal_shutdown("Goals Reached")
			
			x_dL,y_dL,theta_dL=xListFinal[t],yListFinal[t],thetaListFinal[t]
			
			#cleanup()#check
			#rospy.signal_shutdown("Goals Reached!")


		time.sleep(4)
		rospy.loginfo("REEEEEEEEEEEEEAAAAAAAAAAAAAACCCCCCCCCCCCCCCCHHHHHHHHHHHHHHEEEEEEEEEEEEEEEEED")
		#finalvel='x:'+str(round(ul,2))+' y:'+str(round(uf,2))+' z:'+str(round(ur,2))
		finalvel='x:'+str(round(ur,2))+' y:'+str(round(uf,2))+' z:'+str(round(ul,2))
		
		#finalvel='x:'+str(round(uf,2))+' y:'+str(round(ur,2))+' z:'+str(round(ul,2))
	
	
	
	velocityPub.publish(finalvel)
	taskStatusPub.publish(taskStatus.data)
		
	


	    
################################main##################################################
def main():
	global finalvel
	rospy.init_node('Controller_node')
	flag=0
	if(flag==0):
		coordgen('/home/winston/catkin_ws/src/hola_bot/scripts/robotFinal.png')
	else:
		graphgen()
	rospy.Subscriber('/detected_aruco',aruco_data,velocity)
	rospy.Subscriber('/endSignal',Int32,endSignalCb)



	'''with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((ip, 8002))
		s.listen()
		conn,addr = s.accept()
		with conn:
			print(f"Connected by {addr}")
			while not rospy.is_shutdown():
				data= conn.recv(1024)
				rospy.Subscriber('/detected_aruco',aruco_data,velocity)
				rospy.Subscriber('/endSignal',Int32,endSignalCb)
				rospy.loginfo(data)
				rospy.loginfo("hiiiiiiii"+finalvel)
				conn.sendall(str.encode(str(finalvel)))
				time.sleep(0.1)
				key=cv2.waitKey(1) & 0xFF
				if key== ord("q"):
					break'''
	rospy.spin()
				
	
if __name__=='__main__':
	main()

