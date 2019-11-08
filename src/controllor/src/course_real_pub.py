#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
import random
def talker():
    pub=rospy.Publisher("/course_real_1", Float64,queue_size=10)
    rospy.init_node("course_real_1",anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        course_desired=random.uniform(0,1)
        rospy.loginfo(course_desired)
        pub.publish(course_desired)
        rate.sleep()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
