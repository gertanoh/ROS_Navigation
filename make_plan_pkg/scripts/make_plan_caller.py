#! /usr/bin/env python
import rospy
from nav_msgs.srv import GetPlan


def make_plan():
    
        
    rospy.init_node("plan_service_client")
    
    # wait for the service to be running
    rospy.wait_for_service("/move_base/make_plan")
    
    # create connection
    plan_srv = rospy.ServiceProxy("/move_base/make_plan", GetPlan)
    
    plan = GetPlan()
    # set up start
    
    # set up goal
    
    res = plan_srv()