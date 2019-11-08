#!/usr/bin/env python
'''thrust_control ROS Node'''
import rospy
from std_msgs.msg import Float64,Int8
import pigpio
from PID import PID
import json
import fileinput
import time

class PID_controllor():

    def __init__(self):
        rospy.init_node('pwmbuilder', anonymous=True)
        rate = rospy.Rate(5) # 5hz
        self.course_real = 0.0
        self.course_desired = 0.0
        self.thrust_pub = rospy.Publisher('/thrust', Float64, queue_size=10)
        rospy.Subscriber("/course_real", Float64, self.callback_real)
        rospy.Subscriber("/course_desired", Float64, self.callback_desired)
        rospy.Subscriber("/switch",Int8,self.callback_switch)
        rate.sleep()
        self.controllor = PID(13, 6, 0.01, -15, 15, -0.5, 0.5)
        self.pi = pigpio.pi()
        self.pi.set_PWM_frequency(23,50)  
        self.pi.set_PWM_range(23,20000)
        
    def callback_switch(self,msg):
        if msg.data == 1:
            #while not rospy.is_shutdown():
            #calculate thrust by PID
            F =- self.controllor.update(self.course_real, self.course_desired)
            self.thrust_pub.publish(F)
        
            #calculate pwm signal
            #dc=21.09*F+1497
            if F>0:
                dc=-0.6*F*F+21.7*F+1525
            elif F<0:
                dc=0.8*F*F+24.3*F+1475
            else:
                dc=1500
            dc=float(dc)
            dc=int(dc)
            self.pi.set_PWM_dutycycle(23,dc)
            rospy.loginfo("the PWM signal is %f", dc)
            '''
            dc_save='dc.json'
            with open(dc_save,'a') as dc_obj:
                dc_obj.write('\n'+str(dc))
            count = len(open(dc_save, 'r').readlines())
            if count < 200:
                pass
            else:
                for line in fileinput.input('dc.json', inplace=1):
                    if not fileinput.isfirstline():
                        print(line.replace('\n',''))
                for line in fileinput.input('dc.json', inplace=1):
                    if not fileinput.isfirstline():
                        print(line.replace('\n',''))

            dc_read=[]
            with open(dc_save,'r') as f:
                for line in f:
                    if line.count('\n')==len(line):
                        pass
                    else:
                        dc_read.append(line.strip('\n'))
            dc_read = list(map(float, dc_read))
            if count<4:
                last_dc=dc
            else:
                dc_read.reverse()
                last_dc=dc_read[1]
                last_dc=int(last_dc)

            if last_dc < dc:
                for i in range(last_dc,dc):
                    self.pi.set_PWM_dutycycle(23,i)
                    time.sleep(0.02)
            elif last_dc > dc:
                for i in range(last_dc,dc, -1):
                    self.pi.set_PWM_dutycycle(23,i)
                    time.sleep(0.02)
            else:
                self.pi.set_PWM_dutycycle(23,dc)       
            '''
                
        elif msg.data == 0:
            self.pi.set_PWM_dutycycle(23,1500)
        else:
            pass

    def callback_real(self, msg): 
        rospy.loginfo("the real course now is : %f", msg.data)
        self.course_real= msg.data
        
    def callback_desired(self, msg): 
        rospy.loginfo("the desired course now is : %f", msg.data)
        self.course_desired = msg.data

if __name__ == '__main__':
    try:
        PID_controllor()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass


