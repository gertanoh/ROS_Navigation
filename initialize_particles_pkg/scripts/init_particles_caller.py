#! /usr/bin/env python
import rospy
from std_srvs.srv import Empty


def init_particle():
    
    rospy.init_node("init_particle_client")
    
    rospy.wait_for_service("/global_localization")
    
    init_srv = rospy.ServiceProxy("/global_localization", Empty)
    
    res = init_srv()
    
    rospy.loginfo("Particles initialized")
    # rospy.spin()
    
if __name__ == "__main__":
    init_particle()
    