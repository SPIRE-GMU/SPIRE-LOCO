"""
TO-DO:
1. Clean up code: change class names, rename variables/methods, add _ to internal methods/variables
2. Add more precise text scrapping from output.txt
    start = ')'
    end = '('
    print(s[s.find(start)+len(start):s.rfind(end)])
"""

import os
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        # self.publisherAll_ = self.create_publisher(String, 'VLLM_Output', 10)
        self.publisherStop_ = self.create_publisher(String, 'VLLM_Stop', 10)
        self.path_status = String()  # Should be "Clear" or "Stop"
        # self.publishAll()
        self.publishStop()


    def publishAll(self):
        while True:
            # Creates ROS2 String object and puts the last line from the VLLM output as its data
            out = String()
            out.data = os.popen("tail -n 1 ~/output.txt").read()

            # Publishes all VLLM output
            self.publisherAll_.publish(out)
            self.get_logger().info('VLLM Output Pub: "%s"' % out.data)
            time.sleep(1)

    def publishStop(self):
        keywords = ["person", "people", "man", "men", "woman", "women", "stop"]

        while True:
            # Creates ROS2 String object and puts the last line from the VLLM output as its data
            out = String()
            out.data = os.popen("tail -n 1 ~/output.txt").read()

            # If stop is in VLLM output, publishes "Stop"/"Clear" to topic "VLLM_Stop"
            for word in keywords:
                if word in out.data.lower():
                    self.path_status.data = "Stop"
                    break
                else:
                    self.path_status.data = "Clear"
            self.publisherStop_.publish(self.path_status)
            self.get_logger().info('VLLM Stop Pub: "%s"' % self.path_status.data)
            time.sleep(1)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
