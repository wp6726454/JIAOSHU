#!/usr/bin/env python
'''lmu ROS Node'''
# license removed for brevity
# encoding:utf-8

import rospy
from std_msgs.msg import Float64
import serial
import numpy as np
import math
from math import sin, cos, atan
import math



def talker():
    '''atmosphere Publisher'''
    rospy.init_node('atmosphere', anonymous=True)
    tempreture_pub = rospy.Publisher('/tempreture', Float64, queue_size=10)
    pressure_pub = rospy.Publisher('/pressure', Float64, queue_size=10)
    windspeed_pub = rospy.Publisher('/windspeed', Float64, queue_size=10)
    winddirection_pub = rospy.Publisher('/winddirection', Float64, queue_size=10)
    #wind_pub = rospy.Publisher('/wind', Float64, queue_size=10)
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():

        ser=serial.Serial('/dev/ttyUSB0',4800)
        data = str(ser.readline())
        eve = str(data).strip().split(",")
        if eve[0] == "$WIMDA":
            temp = float(eve[3])
            press = float(eve[5])
            if eve[17] == '':
                windspeed = 0
                winddirection = 0
            else:
                windspeed = float(eve[17])
                winddirection = float(eve[13])
            pressure_pub.publish(temp)
            tempreture_pub.publish(press)
            windspeed_pub.publish(windspeed)
            winddirection_pub.publish(winddirection)
            rospy.loginfo(temp)
            rospy.loginfo(press)
            rospy.loginfo(windspeed)
            rospy.loginfo(winddirection)
        else:
            continue
        rate.sleep()
                

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
