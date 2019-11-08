#!/usr/bin/env python
#encoding:utf-8 
'''position_keeping ROS Node'''
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64, Int8
from math import pi, atan
import numpy
from numpy import *

class Position_keeping():

    def __init__(self):
        rospy.init_node('position_keeping', anonymous=True)
        rate = rospy.Rate(1) # 1hz
        rospy.Subscriber("/position_real", Float32MultiArray, self.Realposition)
        rospy.Subscriber("/set_point", Float32MultiArray, self.Setposition)
        rospy.Subscriber("/flag", Int8, self.Callback)
        rospy.Subscriber('/course_real', Float64, self.Realcourse)
        self.pub = rospy.Publisher('/course_desired', Float64, queue_size=10)
        self.radius = 5
        self.real_position = zeros(2)
        self.set_position = zeros(2)
        self.realcourse = 0.0
        rate.sleep()

        
    def millerToXY(self,lon,lat):
        xy_coordinate = []  
        L = 6381372*math.pi*2
        W = L
        H = L/2
        mill = 2.3
        x = lon*math.pi/180
        y = lat*math.pi/180
        y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
        x = (W/2)+(W/(2*math.pi))*x
        y = (H/2)-(H/(2*mill))*y
        xy_coordinate.append(float(round(x)))
        xy_coordinate.append(float(round(y)))
        return xy_coordinate
    
    def Realposition(self,msg):
       # rospy.loginfo("position keeping! wave glider position: %s", str(msg.data))
        pos = self.millerToXY(msg.data[0],msg.data[1])
        pos_1 = [-pos[1],pos[0]]
        self.real_position = pos_1
        rospy.loginfo(pos_1)

    def Setposition(self,msg):
        self.set_position = msg.data

    def Realcourse(self,msg):
        self.realcourse = msg.data

    def Callback(self,msg):
        if msg.data == 1:
            self.course_desired=self.p_s(self.set_position[0],self.set_position[1],self.real_position[0],self.real_position[1])
            self.pub.publish(self.course_desired)
            rospy.loginfo("position keeping! wave glider desired course: %s", str(self.course_desired))
        else:
            pass

    def p_s(self,setpoint_x,setpoint_y,realposition_x,realposition_y):

        '''calculate the desired course based on the real-time location and set point'''
        if (numpy.square(setpoint_x-realposition_x)+numpy.square(setpoint_y-realposition_y)) > numpy.square(self.radius):
            if setpoint_x == realposition_x and setpoint_y > realposition_y:
                phid = pi/2
            elif setpoint_x == realposition_x and setpoint_y < realposition_y:
                phid = -pi/2
            elif setpoint_x > realposition_x and setpoint_y >= realposition_y:
                phid = atan((setpoint_y-realposition_y)/(setpoint_x-realposition_x))
            elif setpoint_x < realposition_x and setpoint_y >= realposition_y:
                phid = atan((setpoint_y-realposition_y)/(setpoint_x-realposition_x)) + pi           
            elif setpoint_x < realposition_x and setpoint_y < realposition_y:
                phid = atan((setpoint_y-realposition_y)/(setpoint_x-realposition_x)) - pi           
            else:
                phid = atan((setpoint_y-realposition_y)/(setpoint_x-realposition_x))

        else:
            phid = self.realcourse
        return phid
            


if __name__ == '__main__':
    try:
        Position_keeping()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
