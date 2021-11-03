#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class ObstacleAvoider:
    regions = {}

    def __init__(self, name):
        self.command_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.laserscan_sub = rospy.Subscriber(
            '/iris_model/laser/scan', LaserScan, self._laserscan_callback)

    def _laserscan_callback(self, msg):
        self.regions = {
            'right':  min(min(msg.ranges[0:143]), 10),
            'front_right': min(min(msg.ranges[144:287]), 10),
            'front':  min(min(msg.ranges[288:431]), 10),
            'front_left':  min(min(msg.ranges[432:575]), 10),
            'left':   min(min(msg.ranges[576:719]), 10),
        }

        self.avoid()

    def avoid(self):
        msg = Twist()
        linear_x = 0
        angular_z = 0

        state_description = ''

        if self.regions['front'] > 1 and self.regions['front_left'] > 1 and self.regions['front_right'] > 1:
            state_description = 'nothing'
            linear_x = 0.6
            angular_z = 0
        elif self.regions['front'] < 1 and self.regions['front_left'] > 1 and self.regions['front_right'] > 1:
            state_description = 'front'
            linear_x = 0
            angular_z = 0.3
        elif self.regions['front'] > 1 and self.regions['front_left'] > 1 and self.regions['front_right'] < 1:
            state_description = 'front_right'
            linear_x = 0
            angular_z = 0.3
        elif self.regions['front'] > 1 and self.regions['front_left'] < 1 and self.regions['front_right'] > 1:
            state_description = 'front_left'
            linear_x = 0
            angular_z = -0.3
        elif self.regions['front'] < 1 and self.regions['front_left'] > 1 and self.regions['front_right'] < 1:
            state_description = 'front and front_right'
            linear_x = 0
            angular_z = 0.3
        elif self.regions['front'] < 1 and self.regions['front_left'] < 1 and self.regions['front_right'] > 1:
            state_description = 'front and front_left'
            linear_x = 0
            angular_z = -0.3
        elif self.regions['front'] < 1 and self.regions['front_left'] < 1 and self.regions['front_right'] < 1:
            state_description = 'front and front_left and front_right'
            linear_x = 0
            angular_z = 0.3
        elif self.regions['front'] > 1 and self.regions['front_left'] < 1 and self.regions['front_right'] < 1:
            state_description = 'front_left and front_right'
            linear_x = 0.3
            angular_z = 0
        else:
            state_description = 'unknown case'
            rospy.loginfo(self.regions)

        rospy.loginfo(state_description)
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.command_pub.publish(msg)


if __name__ == '__main__':
    rospy.init_node('checking_for_obstacles')
    ObstacleAvoider(rospy.get_name())
    rospy.spin()
