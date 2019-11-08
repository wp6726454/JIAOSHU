#!/usr/bin/env python
'''lmu ROS Node'''

# license removed for brevity
# encoding:utf-8

import binascii
import rospy
from std_msgs.msg import Float64
import serial
import numpy as np
from math import sin, cos, atan
import json
import fileinput
import math



def talker():
    '''lmu Publisher'''
    pub = rospy.Publisher('/course_real', Float64, queue_size=10)
    rospy.init_node('lmu', anonymous=True)
    rate = rospy.Rate(5) # 5hz

    while not rospy.is_shutdown():

            ser=serial.Serial('/dev/ttyUSB1',9600)
            data = str(binascii.b2a_hex(ser.read(28)))
            eve = data[49:53]
            head = data[0:2]
           # rospy.loginfo(data)
            if head != "77":
                pass
            else:
                course_1=float(eve)/10.0
                rospy.loginfo(course_1)
                course_out=course_1*math.pi/180
                rospy.loginfo(course_out)
                if course_out > math.pi:
                    real_course = course_out-2*math.pi
                elif course_out < -math.pi:
                    real_course = course_out+2*math.pi
                else:
                    real_course = course_out

                phi_publish=real_course
                pub.publish(phi_publish)
                rospy.loginfo("real course is :%f", phi_publish)
                rate.sleep()

'''
                phi_save='phi.json'
                with open(phi_save,'a') as phi_obj:
                    phi_obj.write('\n'+str(phi))
                count = len(open(phi_save, 'r').readlines())
                if count <200:
                    pass
                else:
                    for line in fileinput.input('phi.json', inplace=1):
                        if not fileinput.isfirstline():
                            print(line.replace('\n',''))
                    for line in fileinput.input('phi.json', inplace=1):
                        if not fileinput.isfirstline():
                            print(line.replace('\n',''))

                phi_read=[]
                with open(phi_save) as f:
                    for line in f:
                        if line.count('\n')==len(line):
                            pass
                        else:
                            phi_read.append(line.strip('\n'))
                phi_read = list(map(float, phi_read))
                if len(phi_read) < 10:
                    phi_publish=phi
                else:
                    phi_read.reverse()
                    phi_filter=phi_read[0:9]
                    phi_filter.remove(max(phi_filter))
                    phi_filter.remove(min(phi_filter))
                    phi_publish=sum(phi_filter)/len(phi_filter)
'''
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
