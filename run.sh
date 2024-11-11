#!/bin/bash

# Source ROS 2 environment
source /opt/ros/$ROS_DISTRO/setup.bash

# Navigate to the workspace
cd /root/ros2_ws

# Build the workspace
colcon build

# Source the workspace
source /root/ros2_ws/install/setup.bash

# Loop to keep the container running
while true; do
    sleep 10
done