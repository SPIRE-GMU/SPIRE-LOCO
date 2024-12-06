import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import qos_profile_system_default

import socket

class socketPub(Node):

    def __init__(self):
        super().__init__('socketPub')
        self.declare_parameter('frame_id', '')
        self.frame_id = str(self.get_parameter('frame_id').value)
        
        #Change ipaddr and port to jetson
        serverAddressPort   = ("192.168.0.215", 20001)
        #Creates a UDP server socket
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind(serverAddressPort)

        #Subscription to jetson /cmd_vel
        self.subscription = self.create_subscription(Twist,'/cmd_vel', self.callback, qos_profile=qos_profile_system_default)
        
        
    def callback(self, inMsg):
        #Waits for response from client
        bytesAddressPair = self.UDPServerSocket.recvfrom(1024)
        clientAddress = bytesAddressPair[1]
        #Uses client response address to send jetson /cmd_vel values
        self.UDPServerSocket.sendto(str.encode(f'{inMsg.linear.x},{inMsg.angular.z}'), clientAddress)

        #self.get_logger().info(f'L: {float(inMsg.linear.x)}, A: {float(inMsg.angular.z)}')

def main(args=None):
    rclpy.init(args=args)
    socket_Pub = socketPub()
    rclpy.spin(socket_Pub)
    socket_Pub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
