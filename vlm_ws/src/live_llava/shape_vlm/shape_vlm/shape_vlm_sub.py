"""
TO-DO:
1. Clean up code: change class names, rename variables/methods, add _ to internal methods/variables
2. Publishing to 'cmd_vel' works. Can use pyautogui to simlulate key press as backup
"""

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
import pyautogui
import time


class ShapeVLMSub(Node):

    def __init__(self):
        super().__init__('ShapeVLM_Sub')
        # self.subscriptionAll = self.create_subscription(String, 'VLM_Output', self.listener_callback, 10)
        self.subscriptionFormation = self.create_subscription(String, 'Formation', self.formation_placeholder, 10)
        self.path_status = ""

        # prevent unused variable warning
        # self.subscriptionAll
        self.subscriptionFormation

    def listener_callback(self, msg):
        # Subscribes to all VLLM output
        self.get_logger().info('%s' % msg.data)

    def formation_placeholder(self, msg):
        # Subscribes to path_status from subscriber
        self.get_logger().info('%s' % msg.data)
        self.path_status = msg.data


def main(args=None):
    rclpy.init(args=args)

    shape_vlm_sub = ShapeVLMSub()

    rclpy.spin(shape_vlm_sub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    shape_vlm_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    


