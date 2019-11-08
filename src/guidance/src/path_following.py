#!/usr/bin/env python
#encoding:utf-8 
'''path_following ROS Node'''
import rospy
from std_msgs.msg import Float32MultiArray, Float64, Int8
from gui.msg import pf
import math
from math import pi, acos, atan
from numpy import *
import numpy as np

class Path_following():

    def __init__(self):
        rospy.init_node('path_following', anonymous=True)
        rate = rospy.Rate(1) # 1hz
        self.pub = rospy.Publisher('/course_desired', Float64, queue_size=10)
        rospy.Subscriber("/position_real", Float32MultiArray, self.Realposition)
        rospy.Subscriber("/waypoints", pf, self.Pointswayfun)
        rospy.Subscriber('/course_real', Float64, self.Realcourse) 
        rospy.Subscriber("/flag", Int8, self.Callback)
        self.radius = 4
        self.deta = 5
        self.realposition = np.random.rand(1,2)
        self.pointsway = np.random.rand(5,2)
        self.realcourse = 0.0
        rate.sleep()
       
    def p_s(self,setpoint_x,setpoint_y,realposition_x,realposition_y):

        '''calculate the desired course based on the real-time location and set point'''
        if (np.square(setpoint_x-realposition_x)+np.square(setpoint_y-realposition_y)) > np.square(self.radius):
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
        
    def millerToXY(self,lon,lat):
        xy_coordinate = []  # 转换后的XY坐标集
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
        pos = self.millerToXY(msg.data[0],msg.data[1])
        pos_1 = [pos[0],-pos[1]]
        self.realposition = np.array(pos_1)
        
    def Pointswayfun(self,msg):
        self.pointsway = np.array([msg.p_1,msg.p_2,msg.p_3,msg.p_4,msg.p_5])

    def Realcourse(self,msg):
        self.realcourse = msg.data

    def Callback(self,msg):
        if msg.data == 2:
            self.course_desired=self.p_s(self.p_f()[0],self.p_f()[1],self.realposition[1],self.realposition[0])
            self.pub.publish(self.course_desired)
            rospy.loginfo("path following! wave glider desired course: %s", str(self.course_desired))
        else:
            pass

    def p_f(self):
#该函数用来确认航迹段上的LOS点
#判断当前航迹段

        d=np.zeros(len(self.pointsway))  
        for i in range(len(self.pointsway)):
            d[i]=np.linalg.norm(self.pointsway[i]-self.realposition)
        d=list(d)
        b = d.index(min(d)) #寻找最近轨迹点的位置
        rospy.loginfo(b) 
        if b==0:

            A=self.pointsway[b+1,1]-self.pointsway[b,1]
            B=self.pointsway[b,0]-self.pointsway[b+1,0]
            C=self.pointsway[b+1,0]*self.pointsway[b,1]-self.pointsway[b,0]*self.pointsway[b+1,1]
            #求垂足
            y0=(B*B*self.realposition[0]-A*B*self.realposition[1]-A*C)/(A*A+B*B)
            x0=(-A*B*self.realposition[0]+A*A*self.realposition[1]-B*C)/(A*A+B*B)
            yd=y0-np.sign(self.pointsway[b,0]-self.pointsway[b+1,0])*np.sqrt(np.square(self.deta)/np.square(1+(abs(self.pointsway[b,1]-self.pointsway[b+1,1])/\
            (self.pointsway[b,0]-self.pointsway[b+1,0]))))
            xd=x0-np.sign(self.pointsway[b,1]-self.pointsway[b+1,1])*(abs((self.pointsway[b,1]-self.pointsway[b+1,1])/(self.pointsway[b,0]-self.pointsway[b+1,0])))*\
            (y0-yd)

        elif b==len(self.pointsway)-1:

            A=self.pointsway[b,1]-self.pointsway[b-1,1]
            B=self.pointsway[b-1,0]-self.pointsway[b,0]
            C=self.pointsway[b,0]*self.pointsway[b-1,1]-self.pointsway[b-1,0]*self.pointsway[b,1]
            #求垂足
            y0=(B*B*self.realposition[0]-A*B*self.realposition[1]-A*C)/(A*A+B*B)
            x0=(-A*B*self.realposition[0]+A*A*self.realposition[1]-B*C)/(A*A+B*B)
            yd=y0-np.sign(self.pointsway[b-1,0]-self.pointsway[b,0])*np.sqrt(np.square(self.deta)/np.square(1+(abs(self.pointsway[b-1,1]-self.pointsway[b,1])/\
            (self.pointsway[b-1,0]-self.pointsway[b,0]))))
            xd=x0-np.sign(self.pointsway[b-1,1]-self.pointsway[b,1])*(abs((self.pointsway[b-1,1]-self.pointsway[b,1])/(self.pointsway[b-1,0]-self.pointsway[b,0])))*\
            (y0-yd)     

        else:

            PbPt = self.realposition-self.pointsway[b]
            PbPb_1 = self.pointsway[b-1]-self.pointsway[b]
            PbPb1 = self.pointsway[b+1]-self.pointsway[b]

            if self.angle(PbPt, PbPb_1) < self.angle(PbPt, PbPb1):
                A=self.pointsway[b,1]-self.pointsway[b-1,1]
                B=self.pointsway[b-1,0]-self.pointsway[b,0]
                C=self.pointsway[b,0]*self.pointsway[b-1,1]-self.pointsway[b-1,0]*self.pointsway[b,1]
                #求垂足
                y0=(B*B*self.realposition[0]-A*B*self.realposition[1]-A*C)/(A*A+B*B)
                x0=(-A*B*self.realposition[0]+A*A*self.realposition[1]-B*C)/(A*A+B*B)
                yd=y0-np.sign(self.pointsway[b-1,0]-self.pointsway[b,0])*np.sqrt(np.square(self.deta)/np.square(1+(abs(self.pointsway[b-1,1]-self.pointsway[b,1])/\
                (self.pointsway[b-1,0]-self.pointsway[b,0]))))
                xd=x0-np.sign(self.pointsway[b-1,1]-self.pointsway[b,1])*(abs((self.pointsway[b-1,1]-self.pointsway[b,1])/(self.pointsway[b-1,0]-self.pointsway[b,0])))*\
                (y0-yd)
                   

            else:

                A=self.pointsway[b+1,1]-self.pointsway[b,1]
                B=self.pointsway[b,0]-self.pointsway[b+1,0]
                C=self.pointsway[b+1,0]*self.pointsway[b,1]-self.pointsway[b,0]*self.pointsway[b+1,1]
                #求垂足
                y0=(B*B*self.realposition[0]-A*B*self.realposition[1]-A*C)/(A*A+B*B)
                x0=(-A*B*self.realposition[0]+A*A*self.realposition[1]-B*C)/(A*A+B*B)
                yd=y0-np.sign(self.pointsway[b,0]-self.pointsway[b+1,0])*np.sqrt(np.square(self.deta)/np.square(1+(abs(self.pointsway[b,1]-self.pointsway[b+1,1])/\
                (self.pointsway[b,0]-self.pointsway[b+1,0]))))
                xd=x0-np.sign(self.pointsway[b,1]-self.pointsway[b+1,1])*(abs((self.pointsway[b,1]-self.pointsway[b+1,1])/(self.pointsway[b,0]-self.pointsway[b+1,0])))*\
                (y0-yd)      

        return np.array([xd,yd]) 
       

    def angle(self,a,b):
        c = np.dot(a,b)
        d = np.dot(a,a)
        e = np.sqrt(d)
        f = np.dot(b,b)
        g = np.sqrt(f)
        h = c/(e*g)
        z = acos(h)
        return z

 

if __name__ == '__main__':
    try:
        Path_following()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
