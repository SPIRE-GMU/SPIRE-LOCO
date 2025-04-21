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
Done on Jetson AGX Orin Devkit (requires Jetpack 6)
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
* https://blog.adriel.co.nz/2018/01/25/change-docker-data-directory-in-debian-jessie/
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

## Assigning MicroSD Card a Mount POoint
If setting the data-root for Docker to be your MicroSD card causes a duplicate of your MicroSD card to appear within your files/file explorer that will keep changing names, follow this forurm thread or following steps to fix it.
* https://askubuntu.com/questions/1451716/name-of-internal-hard-drive-keeps-changing

Use the fdisk command to see the device path of all hard disk partitions
'''
sudo fdisk -l
'''

Use the blkid command to show the current partition label and UUID of any disk partition with the device path.
'''
blkid file_path
'''

Add a label to the disk partition using the e2label or the tune2fs commands for ext2, ext3, and ext4 formatted partitions. Or use the ntfslabel for the ntfs format.
'''
sudo e2label file_path "drive_name"
sudo tune2fs -L "drive_name" file_path
sudo ntfslabel file_path drive_name
'''

Now that you can refer to the MicroSD card as the label from the previous step, add it to the /etc/fstab file.
'''
LABEL=drive_name /mount/point           ext4    defaults        0       2
'''

## Sign Recognition Experiment Setup with vlm_ws
Navigate inside the vlm_ws directory to colcon build and source setup files.
```
colcon build --packages-select live_llava
source install/setup.bash
```

Execute the VLM start node first, followed by the Publisher and Subscriber nodes, each in their separate terminal.
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
  * Keywords are in array called keywords (which are "sign" and "signs" by default)
* ros2 run py_pubsub live_llava_sub
  * Receives information from "path_status"
  * Stops the TurtleBot when "path_status" is "stop"
  * Note this is done by simulating pressing the "s" key whenever the subscriber node receives stop
  * The simulated "s" key press is for the CURRENT WINDOW IN FOCUS, so the terminal running teleop needs to be in-focus
 
## Robot Formation Recognition Experiment Setup with Agent Studio
Run the jetson-containers command.
```
jetson-containers run -v ~/NanoLLM:/workspace/NanoLLM  $(autotag nano_llm)
```

Run the following commands while connected to the internet (commands can be copy and pasted all together).
```
apt update
apt install -y gstreamer1.0-nice
apt-get install -y avahi-utils libnss-mdns 
service avahi-daemon stop
python3 -m nano_llm.studio
```

Once Agent Studio is running, copy the following node layout with the following specifications:
![Node Editor](https://github.com/user-attachments/assets/0fdd0bf1-1b7f-4645-bedc-6ca13a593852)
![llava-v1 5-7b](https://github.com/user-attachments/assets/fec5c28a-ed24-4706-95f5-b6cc40d0f6cd)
![AutoPrompt](https://github.com/user-attachments/assets/4f1c13f7-7d01-4f89-96cf-616bae9bead7)
![RateLimit](https://github.com/user-attachments/assets/4aa12e48-e865-4ae7-b579-638c5723dd9d)

Once the Agent Studio nodes are setup, presets can be saved and loaded at the top-right corner of Agent Studio. The command to run Agent Studio can use the --load prefix to load your preset.
```
python3 -m nano_llm.studio --load preset_name
```

