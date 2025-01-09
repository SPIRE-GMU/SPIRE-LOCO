#!/usr/bin/env bash
gnome-terminal --title "robot launch" -x bash -c "ros2 launch turtlebot3_bringup robot.launch.py" &
gnome-terminal --title "turtlebot teleop" -x bash -c "ros2 run turtlebot3_teleop teleop_keyboard" &
