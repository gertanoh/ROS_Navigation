#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Vector3
from geometry_msgs.msg import PoseWithCovarianceStamped


pub_move = None
sleep_rate = None
covariance = None
pub_pose = None


def move(side):
    
    global pub_move, sleep_rate
    index = 0
    
    while(index < side):
        
        pub_move.publish(Twist(Vector3(0.7, 0, 0), Vector3(0, 0, 0)))
        index += 1
        sleep_rate.sleep()

def turn(turn_sec):
    
    global pub_move, sleep_rate
    index = 0
    
    while(index < turn_sec):
        
        pub_move.publish(Twist(Vector3(0, 0, 0), Vector3(0, 0, 1.0)))
        index += 1
        sleep_rate.sleep()    

def stop():
    
    global pub_move, sleep_rate
    stop_sec = 2
    index = 0
    
    while(index < stop_sec):
        
        pub_move.publish(Twist(Vector3(0, 0, 0), Vector3(0, 0, 0)))
        index += 1
        sleep_rate.sleep()      


def pose_callback(data):
    
    global covariance
    covariance = data.pose.covariance


def perform_square():
    
    global pub_move, pub_pose, sleep_rate, covariance
    
    rospy.init_node("perform_square_node")
    
    pub_move = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, pose_callback)
    sleep_rate = rospy.Rate(4)
    stop_var = False
    
    while not stop_var:
    
        for index in range(4):
            
            move(5)
            stop()
            turn(6)
            sleep_rate.sleep()
        
        stop()
        
        rospy.loginfo("covariance : " + str(covariance))
        if covariance[0] < 0.65 and covariance[7] < 0.65 and covariance[35] < 0.65:
            stop_var = True
        else:
            rospy.loginfo("the covariance is high, let's try again")
        
    rospy.loginfo("The husky robot is localized")
    
    
    
if __name__ == "__main__":
    perform_square()
    
    