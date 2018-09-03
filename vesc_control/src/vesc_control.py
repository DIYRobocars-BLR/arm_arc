#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import *

def talker():
    rospy.init_node('vesc_control_node', anonymous=True)
    pub = rospy.Publisher('/commands/motor/current', Float64, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        values=1.5
        rospy.loginfo(values)
        pub.publish(values)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
