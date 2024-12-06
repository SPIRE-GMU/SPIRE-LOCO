import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Header
from geometry_msgs.msg import TwistStamped
from rclpy.qos import qos_profile_system_default

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimalpsubscriber')
        self.declare_parameter('frame_id', '')
        self.frame_id = str(self.get_parameter('frame_id').value)
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(TwistStamped, 'cmd_vel_out', self.callback, qos_profile=qos_profile_system_default)

    def callback(self, outMsg):
        twists = Twist()
        twists.linear.x = outMsg.twist.linear.x; twists.linear.y = 1.0; twists.linear.z = 1.0
        twists.angular.x = 1.0; twists.angular.y = 1.0; twists.angular.z = outMsg.twist.linear.x
        self.publisher_.publish(twists)
def main(args=None):
    rclpy.init(args=args)
    try:
        minimal_subscriber = MinimalSubscriber()
        rclpy.spin(minimal_subscriber)
    except rclpy.exceptions.ROSInterruptException:
        pass
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()