# vesc_control

This package is for controlling the motor, by passing the commands to vesc_driver.

The vesc_driver subscribes to the following topics:
```
/commands/motor/brake  
/commands/motor/current [Amps]  
/commands/motor/duty_cycle [0 - 1]  
/commands/motor/position  
/commands/motor/speed
/commands/servo/position
```
Script vesc_control.py  publishes data for /commands/motor/current topic
and the data for this topic is in ampere's.

This script has been tested for current values of 1.5 and 2.5 Amps and the motor works.

### Steps to execute:
Launch the driver :
```
$ roslaunch vesc_driver vesc_driver_node.launch port:=/dev/ttyACM0
```
Make sure the port you pass as parameter is same as the port on which your vesc is connected.

Launch vesc_control:
```
$ rosrun vesc_control vesc_control.py
```
