## Create a Workspace
```
mkdir -p ~/ro2_ws/src
cd ~/ros2_ws/src
```
## Create a Package
```
ros2 pkg create --build-type ament_python py_pubsub
cd ~/ros2_ws/src/py_pubsub/py_pubsub
nano socketPub.py
nano socketSub.py
```
_*** The code for socketPub.py and socketSub.py can be found in the ros2_ws folder. ***_
### Add Entry Points
```
cd ~/ros2_ws/src/py_pubsub
nano setup.py
```
Change the contents of setup.py to reflect the following changes:
```
entry_points={
        'console_scripts': [
                'talker = py_pubsub.socketPub:main',
                'listener = py_pubsub.socketSub:main',
        ],
},
```
## Build and Source the Workspace
```
cd ~/ros2_ws
colcon build --packages-select py_pubsub
echo 'source ~/ros2_ws/install/setup.bash' >> ~/.bashrc
```
# Running the Multi-Robot System using Sockets
The following commands should be executed to run the MRS.

## Running the Master Robot
Open a new terminal and  bring up the master robot.
```
ros2 launch turtlebot3_bringup robot.launch.py
```
_*** Should say Run! if successfully brought up ***_

Open a new terminal and run the following commands to be able to move the master robot.
```
ros2 run turtlebot3_teleop teleop_keyboard
```
Open a new terminal and run the socket publisher.
```
cd ~/ros2_ws
ros2 run py_pubsub talker
```
## Running the Listener Robot

Open a new terminal and bring up the listener robot.
```
ros2 launch turtlebot3_bringup robot.launch.py
```
Open a new terminal and run the socket subscriber.
```
cd ~/ros2_ws
ros2 run py_pubsub listener
```
