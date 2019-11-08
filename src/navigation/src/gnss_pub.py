#!/usr/bin/env python
'''BD ROS Node'''
# license removed for brevity
import rospy
from std_msgs.msg import Float32MultiArray,Float64
import serial
import math
import json
import fileinput
#import numpy as np
#from math import sin, cos, atan

def talker():
    '''GNSS Publisher'''
    pub_pos = rospy.Publisher('/position_real', Float32MultiArray, queue_size=10)
    pub_speed = rospy.Publisher('/WGspeed', Float64, queue_size=10)
    rospy.init_node('gnss', anonymous=True)
    rate = rospy.Rate(5) # 5hz
    while not rospy.is_shutdown():
        try:
            ser=serial.Serial('/dev/ttyUSB2',9600)
        except Exception:
            print ('open serial failed.')
            exit(1)
        while True:
            s = ser.readline()
            am = str(s).strip().split(",")
            if am[0]=='#BESTPOSA':
                if len(am)<15:
                    continue
                else:
                    lon=float(am[12])
                    lat=float(am[11])
                    pos_1 = [lon, lat]
                    pos = Float32MultiArray(data=pos_1)
                    pub_pos.publish(pos)
                    rospy.loginfo(pos.data)
            elif am[0]=='$GPRMC':
                if len(am)<13 or am[7]=='':
                    continue
                else:
                    speed=float(am[7])
                    pub_speed.publish(speed)
                    rospy.loginfo(speed)
            rate.sleep()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

