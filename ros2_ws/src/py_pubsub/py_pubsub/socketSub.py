import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

import socket

class socketSub(Node):

    def __init__(self):
        super().__init__('socketSub')
        self.declare_parameter('frame_id', '')
        self.frame_id = str(self.get_parameter('frame_id').value)
        
        #Creates UDP client socket
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        #Publishs jetson /cmd_vel to turtlebot /cmd_vel
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        #Use timer to constantly run callback
        self.timer = self.create_timer(0.2, self.callback)

    def callback(self):
        #Change ipaddr and port to jetson
        serverAddressPort   = ("192.168.0.215", 20001)
        #Sends blank message with client address to server
        self.UDPClientSocket.sendto(str.encode(""), serverAddressPort)
        #Receives jetson /cmd_vel
        msgFromServer = self.UDPClientSocket.recvfrom(1024)
        msg = msgFromServer[0].decode().split(',')  

        #Creates a Twist object with jetson /cmd_vel
        twists = Twist()
        twists.linear.x = float(msg[0]); twists.linear.y = 0.0; twists.linear.z = 0.0
        twists.angular.x = 0.0; twists.angular.y = 0.0; twists.angular.z = float(msg[1])
        self.publisher_.publish(twists)

        #self.get_logger().info(f'L: {float(twists.linear.x)}, A: {float(twists.angular.z)}')

def main(args=None):
    rclpy.init(args=args)
    socket_Sub = socketSub()
    rclpy.spin(socket_Sub)
    socket_Sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
