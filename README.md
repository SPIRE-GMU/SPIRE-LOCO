# SPIRE-LOCO

Project Description

# Hardware/Software Requirements
* 2-3 TurtleBot3 Burger Robots (Raspberry Pi 3 Model B+ running Ubuntu 22.04 Server with ROS2 Humble Hawksbill)
* TurtleBot3 Burger Robot (Jetson Development Kit running Ubuntu 22.04 with ROS 2 Humble Hawksbill)
* C270 HD Webcam

# Robot Operating System Set Up
Follow the Installation process on the [ROS 2 Documentation: Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) website and the Quick Start Guide on the [ROBOTIS e-Manual](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/) website.
Specifically,
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
