#!/usr/bin/env python3

import socket
import time	
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
import errno

############################Variables##################################

ip = ""     #Enter IP address of laptop after connecting it to WIFI hotspot
coord='x:'+str(0.00)+' y:'+str(0.00)+' z:'+str(0.00)

#############################Functions##################################

def signal_handler(sig, frame):
    print('Clean-up !')
    cleanup()
    sys.exit(0)

def cleanup():
    global s
    s.close()
    print("cleanup done")

def connection(val):
    global coord
    coord=val.data

def terminate(val):
    if(val.data==1):
        cleanup()
        rospy.signal_shutdown()


################################main##################################################

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, 8002))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        rospy.init_node('Connection_node')
        rospy.Subscriber('/velocity',String,connection)
        rospy.Subscriber('/taskStatus',Int32,terminate)
        while True:
            data=conn.recv(1024)
            print(data, coord)
            conn.sendall(str.encode(str(coord)))
            time.sleep(0.9)
            key=cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            '''data = conn.recv(1024)
            print(data, coord)
            conn.sendall(str.encode(str(coord)))
            time.sleep(0.9)
            key=cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break'''
        rospy.spin()