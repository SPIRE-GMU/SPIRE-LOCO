#!/usr/bin/env python3


import rclpy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

msg = """
Communications Failed
"""


# Function responsible for using data taken from other robot, interpreting it, and using it to publish to personal diagnostics
def updater(data):
  
    # Data comes in difficult to read, make a string and split into a list
    data_list = str(data).split()

    # OS check to confirm settings
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    # 
    node = rclpy.create_node('publisher')
    pub = node.create_publisher('cmd_vel', Twist, queue_size=10)

    # Set the linear and angular velocities to their necessary values from the data_list variable
    target_linear_vel   = float(data_list[2])
    target_angular_vel  = float(data_list[-1])

    # Try this first, unless error, print "Communications Failed"
    try:
        # Initialize the message to be published
        twist = Twist()

        # Set the linear x to the value of target_linear_vel and the rest to 0 as the linear x is the only value taken into account from the robot motors
        twist.linear.x = target_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

        # Set the angular z to the value of target_angular_vel and the rest to 0 as the angular z is the only value taken into account from the robot motors
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = target_angular_vel

        # Publish the angular and linear velocities to the cmd_vel topic
        pub.publish(twist)

    except:
        print(msg)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


# Callback function called for subscriber. Logs caller ID and calls the updater function
def callback(data):

    # 
    self.get_logger(self.get_name())

if __name__=="__main__":

    # 
    rclpy.init(args=None)
    node = rclpy.create_node('teleop_listener')
    data = node.create_subscription('/tb3_0/cmd_vel', Twist, callback)
    rclpy.spin()
