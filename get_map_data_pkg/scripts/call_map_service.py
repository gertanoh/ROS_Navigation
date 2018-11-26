#! /usr/bin/env python
import rospy
from nav_msgs.srv import GetMap

def print_dim_map():
    
    rospy.init_node("map_service_client")
    
    # wait for the service to be running
    rospy.wait_for_service("/static_map")
    
    # create connection
    map_srv = rospy.ServiceProxy("/static_map", GetMap)
    
    res = map_srv()
    
    width = res.map.info.width
    height = res.map.info.height
    resolution = res.map.info.resolution
    
    rospy.loginfo("dimensions of the map: " + str(width) + ", " + str(height))
    rospy.loginfo("resolution : " + str(resolution))
    
    rospy.spin()
    

if __name__ == "__main__":
    try:
        print_dim_map()
    except:
        pass