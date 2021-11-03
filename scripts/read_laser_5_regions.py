#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan


class LaserReader:
    regions = []

    def __init__(self, name):
        self.laserscan_sub = rospy.Subscriber(
            '/iris_model/laser/scan', LaserScan, self._laserscan_callback)
        rospy.loginfo_once('[LaserReader] Ready...')

    def _laserscan_callback(self, data):
        # laserscan reads from right to left.
        # degrees = 720/5 -> 144
        self.regions = [
            min(min(data.ranges[0:143]), 10),
            min(min(data.ranges[144:287]), 10),
            min(min(data.ranges[288:431]), 10),
            min(min(data.ranges[432:575]), 10),
            min(min(data.ranges[576:719]), 10),
        ]
        rospy.loginfo(self.regions)


if __name__ == '__main__':
    rospy.init_node('iris_laser_reader')
    LaserReader(rospy.get_name())
    rospy.spin()
