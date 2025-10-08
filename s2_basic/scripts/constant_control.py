#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

# import the message type to use
from std_msgs.msg import Int64, Bool
from geometry_msgs.msg import Twist


class Heartbeat(Node):
       def __init__(self) -> None:
              # initialize base class (must happen before everything else)
              super().__init__("heartbeat")
                     
              # a heartbeat counter
              self.hb_counter = 0
              # self.twist_counter = 0

              # create publisher with: self.create_publisher(<msg type>, <topic>, <qos>)
              self.hb_pub = self.create_publisher(Int64, "/heartbeat", 10)
              self.twist_pub = self.create_publisher(Twist, "/cmd_vel", 10)

              # create a timer with: self.create_timer(<second>, <callback>)
              self.hb_timer = self.create_timer(0.2, self.hb_callback)
              self.twist_timer = self.create_timer(0.2, self.twist_callback)

              # create subscription with: self.create_subscription(<msg type>, <topic>, <callback>, <qos>)
              self.motor_sub = self.create_subscription(Bool, "/health/motor", self.health_callback, 10)

              self.kill_sub = self.create_subscription(Bool, "/kill", self.kill_callback, 10)

       def twist_callback(self) -> None:

              # construct twist msg
              msg = Twist()
              msg.linear.x = 1000.0
              msg.linear.y = 0.1
              msg.linear.z = 0.01

              msg.angular.x = 1000.0
              msg.angular.y = 0.1
              msg.angular.z = 0.01

              self.twist_pub.publish(msg)

              # self.twist_counter += 1
              

       def hb_callback(self) -> None:
              """
              Heartbeat callback triggered by the timer
              """
              # construct heartbeat message
              msg = Int64()
              msg.data = self.hb_counter

              # publish heartbeat counter
              self.hb_pub.publish(msg)

              # increment counter
              self.hb_counter += 1

       def kill_callback(self, msg: Bool) -> None:
              """
              Sensor health callback triggered by subscription
              """
              if msg.data:
                     self.twist_timer.cancel()
                     self.hb_timer.cancel()
                     kill_msg = Twist()
                     kill_msg.linear.x = 0.0
                     kill_msg.linear.y = 0.0
                     kill_msg.linear.z = 0.0
                     kill_msg.angular.x = 0.0
                     kill_msg.angular.y = 0.0
                     kill_msg.angular.z = 0.0
                     self.twist_pub.publish(kill_msg)

       def health_callback(self, msg: Bool) -> None:
              """
              Sensor health callback triggered by subscription
              """
              if not msg.data:
                     self.get_logger().fatal("Heartbeat stopped")
                     self.hb_timer.cancel()



if __name__ == "__main__":
       rclpy.init()        # initialize ROS2 context (must run before any other rclpy call)
       node = Heartbeat()  # instantiate the heartbeat node
       rclpy.spin(node)    # Use ROS2 built-in schedular for executing the node
       rclpy.shutdown()    # cleanly shutdown ROS2 context