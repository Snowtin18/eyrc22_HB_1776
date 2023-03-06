#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (KB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:1776			[ Team-ID ]
# Author List:Dhanvantraj.M,Vinoth.B,Winston Doss,Madhusudhanan.K		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:HB_1776.py
# Functions:main,callback
# 					[ Comma separated list of functions in this file ]
# Nodes:pub,sub		    Add your publishing and subscribing node


####################### IMPORT MODULES #######################
import sys
import traceback
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
##############################################################


def callback(data):
	"""
	Purpose:
	---
	This function should be used as a callback. Refer Example #1: Pub-Sub with Custom Message in the Learning Resources Section of the Learning Resources.
    You can write your logic here.
    NOTE: Radius value should be 1. Refer expected output in document and make sure that the turtle traces "same" path.

	Input Arguments:
	---
        `data`  : []
            data received by the call back function

	Returns:
	---
        May vary depending on your logic.

	Example call:
	---
        Depends on the usage of the function.
	"""
	global angle
	global ypos
	angle=data.theta
	ypos=data.y


def main():
	"""
	Purpose:
	---
	This function will be called by the default main function given below.
    You can write your logic here.

	Input Arguments:
	---
        None

	Returns:
	---
        None

	Example call:
	---
        main()
	"""
	rospy.init_node('move_turtle')
	pub=rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=10)
	
	sub=rospy.Subscriber('/turtle1/pose',Pose,callback)
	
	rate=rospy.Rate(160) #10hz
	
	vel=Twist() #twist variable created
	
	while not rospy.is_shutdown():
		
		if(angle>=0):
			vel.linear.x=1
			vel.angular.z=1
			rospy.loginfo(angle)
			rospy.loginfo("My TurtleBot moving in circle")
		elif(angle<=-(math.pi/2)):
			vel.linear.x=0
			rospy.loginfo(angle)
			rospy.loginfo("My TurtleBot is rotating")
		elif(round(angle,0)>=round(-(math.pi/2),0) and angle<0 ):
			vel.linear.x=1
			vel.angular.z=0
			rospy.loginfo(angle)
			rospy.loginfo("My TurtleBot moving in straight line")
		if(ypos<5.4 and angle<0):
			vel.linear.x=0
			pub.publish(vel)
			rospy.loginfo(angle)
			rospy.loginfo("DONE")
			rospy.signal_shutdown("DONE")
			
		pub.publish(vel)
		rate.sleep()


################# ADD GLOBAL VARIABLES HERE #################

angle=0
ypos=5.4

##############################################################


################# ADD UTILITY FUNCTIONS HERE #################



##############################################################


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS PART #########
if __name__ == "__main__":
    try:
        print("------------------------------------------")
        print("         Python Script Started!!          ")
        print("------------------------------------------")
        main()

    except:
        print("------------------------------------------")
        traceback.print_exc(file=sys.stdout)
        print("------------------------------------------")
        sys.exit()

    finally:
        print("------------------------------------------")
        print("    Python Script Executed Successfully   ")
        print("------------------------------------------")
