#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

def talker():
    pub=rospy.Publisher("/course_desired", Float64,queue_size=10)
    rospy.init_node("course_desired",anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        course_desired=0
        rospy.loginfo(course_desired)
        pub.publish(course_desired)
        rate.sleep()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
