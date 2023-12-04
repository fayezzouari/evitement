#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import math
import numpy as np
from geometry_msgs import Twist
class map:
    def __init__(self, x, y):
        self.x= x
        self.y=y
class position:
    def __init__(self, x, y, phi):
        self.x= x
        self.y=y
        self.phi=phi
            

def scan_callback(scan_data):
    coord= map(0.5,0.5)
    pos= position(0.05,0.05, 0)
    #if((x<map.x and x>0)and (y< map.y and y>0)):
    angles = np.arange(scan_data.angle_min, scan_data.angle_max + scan_data.angle_increment, scan_data.angle_increment)
    for i in range(len(scan_data.ranges)):
        r= scan_data.ranges[i]
        tetha= estwi(rad_deg(angles[i])+pos.phi)

        x= r*(math.cos(deg_rad(abs(tetha))))
        y= r*(math.sin(deg_rad(abs(tetha))))


        x+=pos.x
        if (tetha<0):
            y=pos.y-y
        else:
            y+=pos.y
        
        """if (scan_data.ranges[i])>0.23 and scan_data.ranges[i]<0.4:
            print(scan_data.ranges[i])
            print(rad_deg(angles[i]))"""
        if((x<coord.x and x>0 )and (y< coord.y and y>0)):
            if ((np.abs(x-pos.x)<0.1) and (np.abs(y-pos.y)<0.1)):
                print("OIOIOIOIOI")
                
               
            else:
                print('x=', x-pos.x, 'y=', y-pos.y)
                print('x=', x, 'y=', y)
                print("obstacle detected")
                print(tetha)
                print(rad_deg(angles[i]))
                print(round(scan_data.ranges[i], 3), i)
                



        

    print("doura")

def sign(number):
   if (number>0):
      return 1
   elif (number<0):
      return -1
   else:
      return 0

def estwi(ang):
    while abs(ang)>180:
        ang=ang/2
    return ang

def rad_deg(ang):
    return (ang*180)/3.14

def deg_rad(ang):
    return (ang*3.14)/180

def field_of_view(scan_data):
    return (scan_data.angle_max-scan_data.angle_min)*180.0/3.14

#find the max range and its index
def min_range_index(ranges):
    ranges = [x for x in ranges if not math.isnan(x)]
    return (min(ranges), ranges.index(min(ranges)) )

#find the max range 
def max_range_index(ranges):
    ranges = [x for x in ranges if not math.isnan(x)]
    return (max(ranges), ranges.index(max(ranges)) )

#find the average range
def average_range(ranges):
    ranges = [x for x in ranges if not math.isnan(x)]
    return ( sum(ranges) / float(len(ranges)) )

def average_between_indices(ranges, i, j):
    ranges = [x for x in ranges if not math.isnan(x)]
    slice_of_array = ranges[i: j+1]
    return ( sum(slice_of_array) / float(len(slice_of_array)) )


if __name__ == '__main__':
    
    #init new a node and give it a name
    rospy.init_node('scan_node', anonymous=True)
    #subscribe to the topic /scan. 
    rospy.Subscriber("scan", LaserScan, scan_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

