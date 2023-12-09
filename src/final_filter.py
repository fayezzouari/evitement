#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math
import numpy as np

class map:
    def __init__(self, x, y):
        self.x= x
        self.y=y

class position:
    def __init__(self, x, y, phi):
        self.x= x
        self.y=y
        self.phi=phi
            
global curr_x, curr_y, curr_phi
def robot_position(data):
    curr_x=data.linear.x
    curr_y=data.linear.y
    curr_phi=data.angular.x
    obs=rospy.Subscriber("scan", LaserScan, scan_callback)
    


def scan_callback(scan_data):
    
    coord= map(0.5,0.5)
    pos=position(curr_x, curr_y, curr_phi)
    #if((x<map.x and x>0)and (y< map.y and y>0)):
    angles = np.arange(scan_data.angle_min, scan_data.angle_max + scan_data.angle_increment, scan_data.angle_increment)
    
    rospy.init_node('scans_publisher')
    od = rospy.Publisher('obstacles_scans', Twist, queue_size=10)
    oi= rospy.Publisher("OIOIOI", Twist, queue_size=10)
    rate = rospy.Rate(1)  
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
                signal = Twist()
                # Set the data in signal
                signal.Char="OI"
                signal.x= x
                signal.y= y
                oi.publish(signal)
                rate.sleep()

            else:
                print('x=', x-pos.x, 'y=', y-pos.y)
                print('x=', x, 'y=', y)
                print("obstacle detected")
                print(tetha)
                print(rad_deg(angles[i]))
                print(round(scan_data.ranges[i], 3), i)
                signal = Twist()
                # Set the data in signal
                signal.x= x
                signal.y= y
                od.publish(signal)
                rate.sleep()

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


if __name__ == '__main__':
    
    #init new a node and give it a name
    rospy.init_node('coord_get', anonymous=True)
    #subscribe to the topic /scan. 
    rospy.Subscriber("master", Twist, robot_position)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

