import rospy
from sensor_msgs.msg import LaserScan
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np

def lidar_callback(scan):
    # Plot the lidar data
    angles = np.arange(scan.angle_min, scan.angle_max + scan.angle_increment, scan.angle_increment)
    plt.polar(angles, scan.ranges, 'b.')

    # Display the plot
    plt.title('Lidar Scan')
    plt.pause(0.001)
    plt.clf()  # Clear the plot for the next iteration

rospy.init_node('lidar_visualizer')

# Set up the RPLidar
lidar = RPLidar('/dev/ttyUSB0')  # Replace with the correct port for your system

# Create a subscriber to listen for new lidar scans
lidar_sub = rospy.Subscriber('/scan', LaserScan, lidar_callback)

# Loop to continuously get and plot lidar data
for scan in lidar.iter_scans():
    # Update the timestamp
    scan.header.stamp = rospy.Time.now()

    # Publish the message
    lidar_callback(scan)

# Close the lidar connection when the script is terminated
lidar.stop()
lidar.disconnect()
