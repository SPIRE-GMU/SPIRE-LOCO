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
        #self.verticalToHorizonal(tb3_3,tb3_2)
        #self.horizonalToVertical(tb3_3,tb3_2)
        #self.verticalToTriangle(tb3_1)
        #self.triangleToVertical(tb3_1)

        choice = self.formation_choice()
        while choice != "0":
            match choice:
                case "1":
                    print("Running Option 1")
                    self.verticalToTriangle(tb3_1)
                case "2":
                    print("Running Option 2")
                    self.triangleToVertical(tb3_1)
                case "3":
                    print("Running Option 3")
                    self.verticalToHorizontal(tb3_3, tb3_2)
                case "4":
                    print("Running Option 4")
                    self.horizontalToVertical(tb3_3, tb3_2)
                case "5":
                    print("Running Option 5")
                    self.horizontalToVertical(tb3_3, tb3_2)
                    self.verticalToTriangle(tb3_1)
                case "6":
                    print("Running Option 6")
                    self.triangleToVertical(tb3_1)
                    self.verticalToHorizontal(tb3_3, tb3_2)
                case "7":
                    print("Running Option 7")
                    self.verticalToPointed(tb3_1, tb3_3)
                case "8":
                    print("Running Option 8")
                    self.pointedToVertical(tb3_1, tb3_3)
                case "9":
                    print("Running Option 9")
                    self.horizontalToVertical(tb3_3, tb3_2)
                    self.verticalToPointed(tb3_1, tb3_3)
                    
                case "10":
                    print("Running Option 10")
                    self.pointedToVertical(tb3_1, tb3_3)
                    self.verticalToHorizontal(tb3_3, tb3_2)
                case "11":
                    print("Running Option 11")
                    self.pause(twists, tb3_1, 1)
                    self.pause(twists, tb3_2, 1)
                    self.pause(twists, tb3_3, 1)
                case "12":
                    print("Running Tests")
                case "13":
                    print("Spinning")
                    self.spin(twists, tb3_2)
                    
            choice = self.formation_choice()
        exit()
        
    @staticmethod
    def formation_choice():
        user_choice = input("""
Formation Menu:
0. Exit
1. Vertical Line to Triangle 
2. Triangle to Vertical Line
3. Vertical Line to Horizontal Line
4. Horizontal Line to Vertical Line
5. Horizontal Line to Triangle
6. Triangle to Horizontal Line
7. Vertical Line to Pointed Triangle
8. Pointed Triangle to Vertical Line
9. Horizontal Line to Pointed Triangle
10. Pointed Triangle to Horinzontal Line
11. STOP
12. Testing
13. Spin Test
        """)
        return user_choice

    def pointedToVertical(self, robot, robot2):
        twists = Twist()
        self.negNinety(twists, robot)
        self.forward(twists, robot, 3)
        self.pause(twists, robot, 1)
        self.ninety(twists, robot)
        self.pause(twists, robot, 1)
        self.ninety(twists, robot2)
        self.ninety(twists, robot2)
        self.forward(twists, robot2, 2.7)
        self.pause(twists, robot2, 1)
        self.negNinety(twists, robot2)
        self.forward(twists, robot2, 3)
        self.pause(twists, robot2, 1)
        self.negNinety(twists, robot2)
        self.pause(twists, robot2, 1)

    def verticalToPointed(self, robot, robot2):
        twists = Twist()
        self.ninety(twists, robot)
        self.forward(twists, robot, 3)
        self.pause(twists, robot, 1)
        self.negNinety(twists, robot)
        self.pause(twists, robot, 1)
        self.forward(twists, robot2, 2.7)
        self.pause(twists, robot2, 1)
        self.negNinety(twists, robot2)
        self.forward(twists, robot2, 3)
        self.pause(twists, robot2, 1)
        self.ninety(twists, robot2)
        self.pause(twists, robot2, 1)

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

    def verticalToHorizontal(self,robot,robot2):
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

    def horizontalToVertical(self,robot,robot2):
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

    def spin(self,twist,robot):
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = -0.5; twist.angular.y = -0.5; twist.angular.z = -0.5
        robot.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    socket_Sub = socketSub()
    rclpy.spin(socket_Sub)
    socket_Sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
