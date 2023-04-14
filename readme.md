Welcome to the repository for the project - "Holonomic Robot for 2-D plotting of Images and Mathematical functions".  
Project Description:
A holonomic robot was built using Omniwheels, which is controlled by an ESP32. A pen that can move up and down is mounted on the bot. The bot recieves velocity commands from the laptop through the WIFI to reach the desired position. The current position is obtained using a overhead camera that detects the Aruco marker mounted on the bot. This is communicated to the laptop, which containes the series of desired positions to draw the image or mathematical position. The Desired position and current position is compared to calculate the required velocity of the chassis. Which is then converted to wheel velocities and published to the bot through the WIFI.  

This project was done as part of the Eyantra Robotics Competition conducted by IIT Bombay.  

The codes needed for the final Implementation:  
The softwere is made of 3 python files running on ROS and and an Arduino code running on ESP32. Basic description of the code is done below.  

Arduino Code:  

ESP32_code_1esp.ino  

Recieves velocity of motors as string through the WIFI. Actuates the motors using it.  

Python files:  

aruco_final.py  

Setting up the overhead camera. Cropping the arena from the frame using the 4 aruco markers in the corners. This cropped frame is scaled to 500x500 pixels. The aruco marker on the bot is detected and its coordinates is calculated based on the corners of the aruco markers. This coordinates is the current position of the bot, which is published to connection_final.py.  

connection_final.py:  

The current position is recieved.The image or mathematical function is converted to set of coordinates. These are the desired coordinates. The differnce of desired and current position is calculated. This is converted to body frame and applied to a PD Controller. This is the desired chassis velocity, which is converted to wheel velocity using inverse kinematics. This velocity is published to connection_final.py  

connection_final.py:  

A websocket is initiated in the WIFI. The recieved velocity is sent to the esp32 board mounted on the bot through WIFI which is connected as Socket client.  



