import os

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class StartVLLM(Node):

    def __init__(self):
        super().__init__('start_vllm')
        self.path_status = ""  # Should be "Clear" or "Stop"
        self.start_live_llava()

    def start_live_llava(self):
        os.system("""
            jetson-containers run $(autotag nano_llm) \
                python3 -m nano_llm.agents.video_query --api=mlc \
                    --model liuhaotian/llava-v1.5-7b \
                    --max-context-len 256 \
                    --max-new-tokens 32 \
                    --video-input /dev/video0 \
                    --video-output display://0 \
                    | tee ~/output.txt
            """)

def main(args=None):
    rclpy.init(args=args)

    start_vllm = StartVLLM()

    rclpy.spin(start_vllm)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    start_vllm.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
