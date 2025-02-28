# Autonomous Robots, Visual Language Models, and Road Sign Tests

Autonomous Robots, Visual Language Models, and Road Sign Tests
Multi-robot systems (MRS) are used in a variety of real-world applications, such as transportation and manufacturing. The project will have a MRS consistsing of TurtleBots, with one being a leader to transmit commands to follower robots. The leader TurtleBot will have a Jetson AGX Orin Dev Kit (32GB) and a webcam. A visual language model (VLM) will be used to interpret the webcam feed and will influence the TurtleBots' movements. Lastly, penetration testing will be performed to attack the operating system (OS) of the TurtleBots, Robotic Operating System (ROS), and then progagate that attack to the VLM or vice versa.

https://github.com/user-attachments/assets/e8baf236-a0aa-4b21-82a9-e863e9d824c7

https://github.com/user-attachments/assets/19925b60-7dee-4737-ba67-0948f0baadc5

# Hardware/Software Requirements
* 2-3 TurtleBot3 Burger Robots (Raspberry Pi 3 Model B+ running Ubuntu 22.04 Server with ROS2 Humble Hawksbill)
* TurtleBot3 Burger Robot (Jetson Development Kit running Ubuntu 22.04 (Jetpack 6.1) with ROS 2 Humble Hawksbill)
* C270 HD Webcam
* Router

# Robot Operating System Set Up
Follow the Installation process on the [ROS 2 Documentation: Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) website and the Quick Start Guide on the [ROBOTIS e-Manual](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/) website. Specifically, follow the steps below.

_*** Ensure Auto Logon, Automatic Joining of Router, and SSH are enabled on all robots ***_
## Setup Sources and Install ROS 2 Package
```
locale (check for utf-8)
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop-full
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
```
## Install ROS 2 Dependencies and TurtleBot3 Packages
```
sudo apt-get install ros-humble-ros-gz
sudo apt install ros-humble-cartographer
sudo apt install ros-humble-cartographer-ros
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-dynamixel-sdk
sudo apt install ros-humble-turtlebot3-msgs
sudo apt install ros-humble-turtlebot3
sudo apt install python3-argcomplete python3-colcon-common-extensions libboost-system-dev build-essential
sudo apt install ros-humble-hls-lfcd-lds-driver
sudo apt install libudev-dev
echo 'export ROS_DOMAIN_ID=30' >> ~/.bashrc
```
## Install and Build ROS Packages
```
mkdir -p ~/turtlebot3_ws/src && cd ~/turtlebot3_ws/src
git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b ros2-devel https://github.com/ROBOTIS-GIT/ld08_driver.git
cd ~/turtlebot3_ws/src/turtlebot3
rm -r turtlebot3_cartographer turtlebot3_navigation2
cd ~/turtlebot3_ws/
source ~/.bashrc
colcon build --symlink-install --parallel-workers 1
echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc
```
## OpenCR USB Port Setting
```
sudo cp `ros2 pkg prefix turtlebot3_bringup`/share/turtlebot3_bringup/script/99-turtlebot3-cdc.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```
## Configure the LDS
On the Jetson run:
```
echo 'export LDS_MODEL=none' >> ~/.bashrc
```
On the Raspberry Pi run:
```
echo 'export LDS_MODEL=LDS-02' >> ~/.bashrc
```
## Setup OpenCR
```
sudo dpkg --add-architecture armhf
sudo apt update
sudo apt install libc6:armhf
echo 'export OPENCR_PORT=/dev/ttyACM0' >> ~/.bashrc
echo 'export OPENCR_MODEL=burger' >> ~/.bashrc
rm -rf ./opencr_update.tar.bz2kali
wget https://github.com/ROBOTIS-GIT/OpenCR-Binaries/raw/master/turtlebot3/ROS2/latest/opencr_update.tar.bz2
tar -xvf ./opencr_update.tar.bz2
cd ~/opencr_update
./update.sh $OPENCR_PORT $OPENCR_MODEL.opencr
```
## Finish Configuring /.bashrc
```
echo 'ROS_MASTER_URI=http://{ROS_MASTER_IP}:11311/' >> ~/.bashrc
echo 'ROS_HOSTNAME={ROS_MASTER_IP}' >> ~/.bashrc
echo 'TURTLEBOT3_MODEL=burger' >> ~/.bashrc
source ~/.bashrc
```
## Test TurtleBot3 Movement
```
ros2 launch turtlebot3_bringup robot.launch.py
ros2 run turtlebot3_teleop teleop_keyboard
```
# Multi-Robot System using FastDDS
The following commands should be executed to run the MRS.

## Running the Master Robot
Open a new terminal and create the FastDDS Discovery Server.
```
fastdds discovery --server-id 0 -l {master_ip_address}
```
Open a new terminal and  bring up the master robot.
```
export ROS_DISCOVERY_SERVER={master_ip_address}
ros2 launch turtlebot3_bringup robot.launch.py
```
_*** Should say Run! if successfully brought up ***_

Open a new terminal and run the following commands to be able to move the master robot.
```
export ROS_DISCOVERY_SERVER={master_ip_address}
ros2 run turtlebot3_teleop teleop_keyboard
```
## Running the Listener Robot
Open a new terminal and bring up the listener robot.
```
export ROS_DISCOVERY_SERVER={master_ip_address}
ros2 launch turtlebot3_bringup robot.launch.py
```
# Partitioning the MRS
Download [turtlebot3](https://github.com/ROBOTIS-GIT/turtlebot3) package from github and replace the preexisting turtlebot3 package with the new package.
Go into robot.launch.py in the turtlebot3_bringup and change the default namespace.
Change teleop_keyboard.py publisher to the new namespace.
```
cd ~/turtlebot3_ws/
colcon build --symlink-install --parallel-workers 1
```

# Performing SLAM using TurtleBot3
The following SLAM is performed utilizing the slam toolbox.

## Running the Master Robot
Open the FastDDS Server.
```
fastdds discovery --server-id 0 -l {master_ip_address}
```
## Running the Listener Robot
Install the slam toolbox.
```
sudo apt install ros-humble-slam-toolbox
```
Open a new terminal and bring up the robot.
```
ros2 launch turtlebot3_bringup robot.launch.py
```
Open a new terminal and bring up the robot's navigation system.
```
ros2 launch nav2_bringup navigation_launch.py
```
Open a new terminal and run the following command to create an asynchronous map.
```
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=/opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml use_sim_time:=false
```
Open a new terminal and run the following command to create an synchronous map.
```
ros2 launch slam_toolbox online_sync_launch.py slam_params_file:=/opt/ros/humble/share/slam_toolbox/config/mapper_params_online_sync.yaml use_sim_time:=false
```
Open a new terminal and open rviz to view the map.
```
ros2 run rviz2 rviz2 -d /opt/ros/humble/share/nav2_bringup/rviz/nav2_default_view.rviz
```

# Vision Language Model (VLM) Setup
## Download Jetson Containers & Associated Models
```
git clone https://github.com/dusty-nv/jetson-containers
bash jetson-containers/install.sh
```
Download and Run the Live LLava Model from Liuhaotian
```
jetson-containers run liuhaotian/llava-v1.5-7b
```

## Configuring Docker Daemon 
The purpose is to store the VLM models inside the SD card.
*  https://blog.adriel.co.nz/2018/01/25/change-docker-data-directory-in-debian-jessie/
* https://docs.docker.com/engine/daemon/

Within the daemon.json config file
```
{
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    },
    "data-root": "/media/ubu/sd_card/docker"
}
```

```
sudo systemctl restart docker 
```
## Run the vlm_ws as a ROS2 Node
Navigate inside the vlm_ws directory to colcon build and source setup files.
```
colcon build --packages-select live_llava
source install/setup.bash
```

Execute the VLM node first, followed by the Publisher and Subscriber nodes, each in their separate terminal.
```
ros2 run live_llava vlm_start
ros2 run live_llava vlm_pub
ros2 run live_llava vlm_sub
```
Notes on VLM ROS Nodes
* ros2 run py_pubsub live_llava_start
  * Sub Runs the command to start the vllm
  * May take a while
  * Opens another window to show camera and prompt+output
  * Output is shown in terminal and sent to ~/output.txt
* ros2 run py_pubsub live_llava_pub
  * Reads from output.txt and publishes "stop" or "clear" to the topic "path_status" when detecting certain keywords
* ros2 run py_pubsub live_llava_sub
  * Receives information from "path_status"
  * Stops the TurtleBot when "path_status" is "stop"
  * Note this is done by simulating pressing the "s" key whenever the subscriber node receives stop
  * The simulated "s" key press is for the CURRENT WINDOW IN FOCUS, so the terminal running teleop needs to be in-focus
