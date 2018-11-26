#! /usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from my_summit_localization_pkg.srv import MyServiceMessage, MyServiceMessageResponse
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult, MoveBaseFeedback
import rosparam
import yaml



def feedback_callback(feedback):
    rospy.loginfo('[Feedback] Going to Goal Pose...')
    

def send_goal(label):
    
    
    # create the connection to the action server
    client = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    # waits until the action server is up and running
    client.wait_for_server()
    
    # creates a goal to send to the action server
    goal = MoveBaseGoal()
    # really important to set the map frame
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.position.x = rosparam.get_param(label+'/position/x')
    goal.target_pose.pose.position.y = rosparam.get_param(label+'/position/y')
    goal.target_pose.pose.position.z = rosparam.get_param(label+'/position/z')
    goal.target_pose.pose.orientation.x = rosparam.get_param(label+'/orientation/x')
    goal.target_pose.pose.orientation.y = rosparam.get_param(label+'/orientation/y')
    goal.target_pose.pose.orientation.z = rosparam.get_param(label+'/orientation/z')
    goal.target_pose.pose.orientation.w = rosparam.get_param(label+'/orientation/w')
    
    # sends the goal to the action server, specifying which feedback function
    # to call when feedback received
    client.send_goal(goal, feedback_cb=feedback_callback)
    
    client.wait_for_result()
    
    rospy.loginfo('[Result] State: %d'%(client.get_state()))

"""
Class provides a service called /get_coordinates.
The service retrieves the pose via a label, then call 
an action client, which moves the robot to the pose
"""

class MoveRobot(object):
    
    def __init__(self, srv_name="/get_coordinates"):
        self._srv_name = srv_name
        self._service = rospy.Service(self._srv_name, MyServiceMessage,
            self.srv_callback)
            
    def srv_callback(self, request):
        
        response = MyServiceMessageResponse()
        
        # load yaml file
        file = "/home/user/catkin_ws/src/my_summit_navigation_pkg/spots/spots.yaml"
        paramlist = rosparam.load_file(file, default_namespace=None)
        
        for params, ns in paramlist:
            for key, value in params:
                print('k: ', key)
                print('v: ', value)
                if key == request.label:
                    rosparam.upload_params(ns, params)
        
        # call action client
        send_goal(request.label)
        
        response.navigation_sucessfull = true
        
if __name__ == "__main__":
    
    rospy.init_node("Move_robot_node")
    goal = MoveRobot()
    rospy.spin()