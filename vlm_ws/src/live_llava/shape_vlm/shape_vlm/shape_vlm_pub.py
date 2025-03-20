"""
TO-DO:
1. Clean up code: change class names, rename variables/methods, add _ to internal methods/variables
"""

import os
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class ShapeVLMPub(Node):

    def __init__(self):
        super().__init__('ShapeVLM_Pub')
        # self.publisherAll_ = self.create_publisher(String, 'VLM_Output', 10)
        self.publisherStop_ = self.create_publisher(String, 'Formation', 10)
        self.formation = String()

        # self.publish_all()
        self.publish_formation()

    def publish_all(self):
        while True:
            # Creates ROS2 String object and puts the last line from the VLM output as its data
            out = String()
            out.data = os.popen("tail -n 1 ~/output.txt").read()

            # Publishes all VLM output
            self.publisherAll_.publish(out)
            self.get_logger().info('VLM Output Pub: "%s"' % out.data)
            time.sleep(1)

    def publish_formation(self):
        keywords = ["triangle", "line"]
        start_s = ')'
        end_s = '('

        while True:
            # Reads the last lines form the VLM output and *tries to* get most of
            s = os.popen("tail -n 3 ~/output.txt").read()
            filter_s = s[s.find(start_s) + len(start_s):s.rfind(end_s)]

            # Creates ROS2 String object and puts the last lines from the VLM output as its data
            out = String()
            out.data = filter_s

            # If a keyword is in VLM output, publishes detected formation to topic "Formation"
            for word in keywords:
                if word in out.data.lower():
                    self.formation.data = word
            self.publisherStop_.publish(self.formation)
            self.get_logger().info('%s' % self.formation.data)
            # time.sleep(1)

    def publish_oof(self): # OOF = out of formation
        starting_formation = self.formation
        current_formation = ""
        oof_status = "in"


def main(args=None):
    rclpy.init(args=args)

    shape_vlm_pub = ShapeVLMPub()

    rclpy.spin(shape_vlm_pub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    shape_vlm_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
