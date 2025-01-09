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

class VLMSub(Node):

    def __init__(self):
        super().__init__('VLM_Sub')
        # self.subscriptionAll = self.create_subscription(String, 'VLLM_Output', self.listener_callback, 10)
        self.subscriptionStop = self.create_subscription(String, 'VLLM_Stop', self.set_stop, 10)
        self.path_status = ""

        # prevent unused variable warning
        # self.subscriptionAll
        self.subscriptionStop

        # For stopping the TurtleBot
        # self.publisherVel = self.create_publisher(Twist, 'cmd_vel', 10)
        # self.twists = Twist()

    def listener_callback(self, msg):
        # Subscribes to all VLLM output
        self.get_logger().info('VLLM_Output Sub: "%s"' % msg.data)

    def set_stop(self, msg):
        # Subscribes to path_status from subscriber
        self.get_logger().info('%s' % msg.data)
        self.path_status = msg.data

        # Publishes velocity 0 to stop the TurtleBot
        if self.path_status == "Stop":
            # self.twists.linear.x = 0.0
            pyautogui.press("s")
        else:
            #self.twists.linear.x = 0.01
            pass
        #self.publisherVel.publish(self.twists)

def main(args=None):
    rclpy.init(args=args)

    vlm_sub = VLMSub()

    rclpy.spin(vlm_sub)
    
    # Only needed if using cmd_vel
    # vlm_sub.twists.linear.x = 0.0
    
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    vlm_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    


