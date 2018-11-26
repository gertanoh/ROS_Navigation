#! /usr/bin/env python
import rospy
import time
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult, MoveBaseFeedback



def feedback_callback(feedback):
    
    rospy.loginfo('[Feedback] Going to Goal Pose...')



def send_goal():
    
    # initializes the action client node
    rospy.init_node('move_base_action_client')
    
    # create the connection to the action server
    client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    # waits until the action server is up and running
    client.wait_for_server()
    
    # creates a goal to send to the action server
    goal = MoveBaseGoal()
    # really important to set the map frame
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = 1.16
    goal.target_pose.pose.position.y = -4.76
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.75
    goal.target_pose.pose.orientation.w = 0.66
    
    # sends the goal to the action server, specifying which feedback function
    # to call when feedback received
    client.send_goal(goal, feedback_cb=feedback_callback)
    
    client.wait_for_result()
    
    rospy.loginfo('[Result] State: %d'%(client.get_state()))
    
    
if __name__ == "__main__":
    send_goal()