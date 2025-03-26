import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
import socket
import time


class socketSub(Node):

    def __init__(self):
        super().__init__('socketSub')
        self.declare_parameter('frame_id', '')
        self.frame_id = str(self.get_parameter('frame_id').value)

        self.clock = 0

        #Publishs jetson /cmd_vel to turtlebot /cmd_vel
        tb3_1 = self.create_publisher(Twist, 'tb3_1/cmd_vel', 10)
        tb3_2 = self.create_publisher(Twist, 'tb3_2/cmd_vel', 10)
        tb3_3 = self.create_publisher(Twist, 'tb3_3/cmd_vel', 10)
        twists = Twist()
        self.pause(twists,tb3_1,0)
        self.pause(twists,tb3_2,0)
        self.pause(twists,tb3_3,0)
        #Uncomment lines for which you want to do 
        self.verticalToHorizonal(tb3_3,tb3_2)
        #self.horizonalToVertical(tb3_3,tb3_2)
        #self.verticalToTriangle(tb3_1)
        #self.triangleToVertical(tb3_1)



    def verticalToTriangle(self,robot):
        #Creates a Twist object with jetson /cmd_vel
        twists = Twist()
        time.sleep(3)
        self.ninety(twists,robot)
        self.forward(twists,robot,3)
        self.pause(twists,robot,1)
        self.negNinety(twists,robot)
        self.pause(twists,robot,0)

    def triangleToVertical(self,robot):
        twists = Twist()
        time.sleep(3)
        self.negNinety(twists,robot)
        self.forward(twists,robot,3.5)
        self.pause(twists,robot,1)
        self.ninety(twists,robot)
        self.pause(twists,robot,0)

    def verticalToHorizonal(self,robot,robot2):
        twists = Twist()
        time.sleep(3)
        self.verticalToTriangle(robot)
        self.forward(twists,robot,2.3)
        self.pause(twists,robot,0)

        self.negNinety(twists,robot2)
        self.forward(twists,robot2,3)
        self.pause(twists,robot2,1)
        self.negNinety(twists,robot2)
        self.pause(twists,robot2,0)
        self.forward(twists,robot2,2.5)
        self.ninety(twists,robot2)
        self.ninety(twists,robot2)
        self.pause(twists,robot2,0)

    def horizonalToVertical(self,robot,robot2):
        twists = Twist()
        time.sleep(3)
        self.forward(twists,robot2,2.5)
        self.pause(twists,robot2,1)
        self.ninety(twists,robot2)
        self.forward(twists,robot2,2.5)
        self.pause(twists,robot2,1)
        self.negNinety(twists,robot2)
        self.pause(twists,robot2,0)

        self.ninety(twists,robot)
        self.ninety(twists,robot)
        self.forward(twists,robot,2.5)
        self.pause(twists,robot,1)
        self.ninety(twists,robot)
        self.forward(twists,robot,3.5)
        self.pause(twists,robot,1)
        self.ninety(twists,robot)
        time.sleep(0.5)
        self.pause(twists,robot,0)


    def ninety(self,twist,robot):
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.5; twist.angular.y = 0.5; twist.angular.z = 0.5
        robot.publish(twist)
        time.sleep(3.5)
        
    def negNinety(self,twist,robot):
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = -0.5; twist.angular.y = -0.5; twist.angular.z = -0.5
        robot.publish(twist)
        time.sleep(3.5)

    def forward(self,twist,robot,sec):
        twist.linear.x = 0.1; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        robot.publish(twist)
        time.sleep(sec)

    def pause(self,twist,robot,sec):
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        robot.publish(twist)
        time.sleep(sec)


    

def main(args=None):
    rclpy.init(args=args)
    socket_Sub = socketSub()
    rclpy.spin(socket_Sub)
    socket_Sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
