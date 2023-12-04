#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import math



if __name__ == '__main__':
    
    #init new a node and give it a name
    rospy.init_node('scan_node', anonymous=True)
    #subscribe to the topic /scan. 
    rospy.Subscriber("scan", LaserScan, scan_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
