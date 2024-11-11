# Use a base image from dustynv/ros repository with the specified version
FROM ros:humble

# Update and upgrade the system packages
RUN apt update && apt upgrade -y && \
    apt install -y python3-pip libgl1 ros-humble-vision-opencv && \
    pip install opencv-python

# Set the working directory to your ROS 2 package
WORKDIR /root/ros2_ws

# Build WS
RUN colcon build

# Copy the run scrypt into the container and make it executable
COPY run.sh /root/run.sh
RUN chmod +x /root/run.sh