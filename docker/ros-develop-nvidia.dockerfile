FROM osrf/ros:noetic-desktop-full

# Use bash instead of sh
SHELL ["/bin/bash", "-c"]

# Update Ubuntu Software repository
RUN apt update \
    && apt upgrade -y

RUN apt install -y git  wget \    
    python3-dev \
    python3-pip \
    python3-rospkg \
    ros-$ROS_DISTRO-navigation \
    ros-$ROS_DISTRO-gmapping \
    ros-$ROS_DISTRO-robot-state-publisher \
    ros-$ROS_DISTRO-gazebo-ros-pkgs \
    ros-$ROS_DISTRO-teleop-twist-keyboard \
    ros-$ROS_DISTRO-tf \
    ros-$ROS_DISTRO-xacro \
    ros-$ROS_DISTRO-diagnostic-updater \
    ros-$ROS_DISTRO-ddynamic-reconfigure \
    ros-$ROS_DISTRO-ros-control \
    ros-$ROS_DISTRO-ros-controllers \
    ros-$ROS_DISTRO-joint-state-publisher \
    ros-$ROS_DISTRO-joint-state-publisher-gui \
    ros-$ROS_DISTRO-teleop-twist-keyboard

# Python 3 dependencies
RUN pip3 install \
        rosdep \
        rospkg 

# Create and initialise ROS workspace
RUN mkdir -p /ros_ws/src
COPY ./ /ros_ws/src/iris_model

WORKDIR /ros_ws

RUN cd /ros_ws \
    && mkdir build \
    && source /opt/ros/$ROS_DISTRO/setup.bash \
    && rosdep update \
    && rosdep install --from-paths src --ignore-src -r -y \
    && catkin_make install

# Clear 
RUN apt clean \
    && rm -rf /var/lib/apt/lists/* 

COPY ./ros_entrypoint.sh /