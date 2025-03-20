import os

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class StartShapeVLM(Node):

    def __init__(self):
        super().__init__('start_shape_vlm')
        self.start_shape_vlm()

    def start_shape_vlm(self):
        os.system("""
            jetson-containers run $(autotag dustynv/nano_llm) \
                python3 -m nano_llm.agents.video_query --api=mlc \
                    --model liuhaotian/llava-v1.5-13b \
                    --max-context-len 256 \
                    --max-new-tokens 64 \
                    --video-input /dev/video0 \
                    --video-output display://0 \
                    --prompt "There is a pink robot, blue robot, and a red robot. What formation do the robots make?" | tee ~/shape_vlm_output.txt
            """)

def main(args=None):
    rclpy.init(args=args)

    start_shape_vlm = StartShapeVLM()

    rclpy.spin(start_shape_vlm)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    start_shape_vlm.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
