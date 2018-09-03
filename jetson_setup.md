# sdroller
semi autonomous jogging stroller

### Jetson Env Setup
Please note that the development of this code is done on a modified MIT Racecar. Hence, some of the packages are specific to the MIT Racecar platform, for example the VESC drivers. This documentation covers these optional packages as well.
Packages specific to the Stroller-E will need to be installed and configured separately.
![MIT Racecar](images/MIT-Racecar-2.jpg)
The Racecar has the following components onboard which are used for this project:  
1. Nvidia Jetson TX2
2. Zed Stereo Cameras
3. VESC Motor Controller  

These additional components are present but not used:
4. Sweep LIDAR
5. Sparkfun Razor M0 IMU
6. Intel Realsense D435 Stereo Camera

The following steps detail the setup of the Jetson TX2 starting from flashing a fresh OS onto the board.

#### 1. Flash Jetpack 3.2.1 ( L4T 28.2.1)
Flash Ubuntu 16.04 onto the TX2 using Nvidia Jetpack 3.2.1. Please consult [official docs](https://docs.nvidia.com/jetpack-l4t/2_1/content/developertools/mobile/jetpack/jetpack_l4t/2.0/jetpack_l4t_install.htm) for this step. You can also check [this video](https://www.youtube.com/watch?v=D7lkth34rgM) from JetsonHacks.

#### 2. Install ROS
Please follow the [official ROS installation guide](http://wiki.ros.org/kinetic/Installation/Ubuntu) for this step. Note, there are multiple versions of ROS that can be installed. This project uses ROS Kinetic and installs ROS via the   `ros-kinetic-desktop-full` package.

After installation, set some ROS Environmental variables:
```
#setup ROS environment variables
$ grep -q -F ' ROS_MASTER_URI' ~/.bashrc ||  echo 'export ROS_MASTER_URI=http://localhost:11311' | tee -a ~/.bashrc
$ grep -q -F ' ROS_IP' ~/.bashrc ||  echo "export ROS_IP=$(hostname -I)" | tee -a ~/.bashrc
```  

If you get the following error;
`ERROR: cannot download default sources list from: https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/sources.list.d/20-default.list Website may be down.`
Then run this
```
# Certificates are messed up on the Jetson for some reason
$ sudo c_rehash /etc/ssl/certs
```


#### 3. Install Zed Driver
[Download](https://download.stereolabs.com/zedsdk/2.5/tegrax2) the executable for the Zed SDK into `~/software/`. Run the executable as so:
```
$ cd ~/software
$ chmod +x ZED_SDK_Linux_*.run
$ ./ZED_SDK_Linux_*.run
```

Follow instructions to complete Installation

#### 4. Optional Packages (Specific to Racecar)
##### Install Intel LibRealsense2 with patched kernel for Intel D435 Stereo Cam
Follow the instructions by JetsonHacks [here](https://github.com/jetsonhacks/buildLibrealsense2TX). You can also read
his [article](https://github.com/jetsonhacks/buildLibrealsense2TX) on installing librealsense for the new D400 series
stereo cameras by intel.

##### Install Catkin Tools
```
$ sudo apt-get update
$ sudo apt-get install python-catkin-tools
```
##### Setup GitHub
Setup SSH keys for your github account. Follow [this](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/) guide.

##### Install extra required ROS packages
`jstest-gtk` package is used to control the car using a joystick.
```
$ sudo apt-get -y install jstest-gtk
```
These packages are required for compiling racecar packages mentioned below. `rosdep` may not install these required packages.
```
$ sudo apt install ros-kinetic-ackermann* ros-kinetic-serial*
$ sudo apt install ros-kinetic-map-server ros-kinetic-move-base
```

##### Setup udev rules for vesc and imu
Create a udev rules file:
```
$ nano /etc/udev/rules.d
```
Paste the following content and save
```
# Alias the Sparkfun 9DoF as imu, and the electronic speed controller as VESC
ACTION=="add", ATTRS{idVendor}=="1b4f", ATTRS{idProduct}=="9d0f", SYMLINK+="imu"
ACTION=="add", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="5740", SYMLINK+="vesc"
```

##### Setup joystick
Joystick can be FrSky Taranis directly plugged into TX2 via USB, or a PlayStation 4 Bluetooth controller or it could be a teensy emulating a joystick (teensy reads signals from Taranis receiver).
When you plug in the joystick, you should see an entry for `js0` in `/dev/input`:
```
$ ls /dev/input/js0
/dev/input/js0
```

Calibrate the joystick as per [this document](https://opentx.gitbooks.io/manual-for-opentx-2-2/radio_joystick.html).

##### Install BLDC Tool for VESC
This tool will be used to flash the firmware for the VESC. The newer VESC Tool and it's firmwares and no longer compatible with the vesc driver ros node here.
Install dependencies:
```
$ sudo apt-get install qt5-default libudev-dev libqt5serialport5-dev -y
```
Clone and build bldc tool:
```
$ cd ~/software
$ git clone https://github.com/racecarj/bldc-tool
$ cd bldc-tool
$ cd bldc-tool
$ make clean && make
$ git clone https://github.com/racecarj/vesc-firmware
```
Run the tool as `./BLDC_Tool`. The VESC firmware is in ~/vesc-firmware/firmware. The RACECAR VESC configuration files are in ~/vesc-firmware/VESC-Configuration.

[source](https://github.com/RacecarJ/installBLDCTool/blob/master/installBLDCToolHost.sh)

#### 5. Setup the Racecar packages from MIT and JetsonHacks
Create a catkin workspace in the home directory. This folder will hold the code for the racecar. Clone all the repositories into the workspace.
```
# Create ws and get repositories
$ mkdir -p ~/racecar-ws/src
$ cd ~/racecar-ws/src
$ git clone https://github.com/RacecarJ/racecar-controllers.git
$ git clone https://github.com/stereolabs/zed-ros-wrapper.git
$ git clone https://github.com/mit-racecar/vesc
$ git clone https://github.com/mit-racecar/racecar
$ cd ../  

# Install dependencies. Unfortunately rosdep does not install all  dependencies.
$ rosdep install -a -y -r
$ rosdep install --from-paths src --ignore-src -r -y

# On the Jetson, there's currently an issue with using the dynamic runtime
# Typically this reports as "cannot find -lopencv_dep_cudart" in the error log
$ catkin config --cmake-args -DCUDA_USE_STATIC_CUDA_RUNTIME=OFF
```
`rosdep` should install the following packages:
```
ros-kinetic-ackermann*
ros-kinetic-serial*
ros-kinetic-urg-node
ros-kinetic-hector-mapping
ros-kinetic-robot-pose-ekf
ros-kinetic-ros-kinetic-rtabmap
ros-kinetic-rviz-imu-plugin
ros-kinetic-gmapping
ros-kinetic-rtabmap-ros
ros-kinetic-joy
ros-kinetic-razor-imu-9dof #This requires some steps to support newer M0 IMU
ros-kinetic-depthimage-to-laserscan
```
Finally, we build the Packages
```
$ catkin build
$ source devel/setup.bash
```

#### 6. Test the Packages
We are now going to test each package to confirm all the devices work.

##### VESC
Run the following command:
```
roslaunch vesc_driver vesc_driver_node.launch  port:="/dev/vesc"
```
There should be no errors. You should be able to subscribe to the `vesc` topics to see data and publish data to make the motor move.

On the Taranis X9D with OpenTX 2.2, the channels 1-8 represent joystick Axes 0-7 and channels 9-32 represent Buttons 0-23.

To teleoperate the car, button4 should be on! Then the Throttle is controlled by CH1-2, Steering CH3-4, and Button4 is CH13.