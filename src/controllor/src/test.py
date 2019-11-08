#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32MultiArray

def callback(data):
    rospy.loginfo(rospy.get_caller_id()+'I heard %s',data.data)

def listener():
    rospy.init_node("test",anonymous=True)
    rospy.Subscriber("/position_real", Float32MultiArray, callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
