import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Header
from geometry_msgs.msg import TwistStamped
from rclpy.qos import qos_profile_system_default

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.declare_parameter('frame_id', '')
        self.frame_id = str(self.get_parameter('frame_id').value)
        self.publisher_ = self.create_publisher(TwistStamped, 'cmd_vel_out', 10)
        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.callback, qos_profile=qos_profile_system_default)

    def callback(self, inMsg):
        outMsg = TwistStamped()
        outMsg.header = Header()
        outMsg.header.stamp = self.get_clock().now().to_msg()
        outMsg.header.frame_id = self.frame_id
        outMsg.twist = inMsg
        self.publisher_.publish(outMsg)
        self.gete_logger().info(f'L: {outMsg.twist.linear}. A: {outMsg.twist.angular}')

def main(args=None):
    rclpy.init(args=args)
    try:
        minimal_publisher = MinimalPublisher()
        rclpy.spin(minimal_publisher)
    except rclpy.exceptions.ROSInterruptException:
        pass
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()