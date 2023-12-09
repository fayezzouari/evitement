#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def publisher():
    # Initialize the ROS node
    rospy.init_node('robot_coord', anonymous=True)

    # Create a publisher for the MyMessage topic
    pub = rospy.Publisher('master', Twist, queue_size=10)

    rate = rospy.Rate(0.1)  # 1 Hz
    coord = Twist()
    coord.linear.x = 0.25
    coord.linear.y = 0.26
    coord.angular.x = 90
    while not rospy.is_shutdown():
        # Create a Twist in
        coord.linear.x += 0.05
        coord.linear.y += 0.06
        coord.angular.x += 10
        if coord.angular.x==180:
            coord.angular.x=0

        # Publish the message
        pub.publish(coord)

        # Log for debugging
        rospy.loginfo("Published: %f %f %d", coord.linear.x, coord.linear.y, coord.angular.x)

        rate.sleep()


if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
