"""
TO-DO:
1. Clean up code: change class names, rename variables/methods, add _ to internal methods/variables
"""

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
import pyautogui
import time

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        # self.subscriptionAll = self.create_subscription(String, 'VLLM_Output', self.listener_callback, 10)
        self.subscriptionStop = self.create_subscription(String, 'VLLM_Stop', self.set_stop, 10)
        self.path_status = ""

        # prevent unused variable warning
        # self.subscriptionAll
        self.subscriptionStop

        # For stopping the TurtleBot
        # self.publisherVelStop = self.create_publisher(Twist, 'cmd_vel', 10)

    def listener_callback(self, msg):
        # Subscribes to all VLLM output
        self.get_logger().info('VLLM_Output Sub: "%s"' % msg.data)

    def set_stop(self, msg):
        # Subscribes to path_status from subscriber
        self.get_logger().info('VLLM_Stop Sub: "%s"' % msg.data)
        self.path_status = msg.data

        # Publishes velocity 0 to stop the TurtleBot
        # twists = Twist()

        if self.path_status == "Stop":
            # twists.linear.x = 0
            pyautogui.press("s")
        else:
            pass
        # self.publisherVelStop.publish(twists)

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    # main()
    for x in range(0,9):
        pyautogui.press("s")
        time.sleep(1)


