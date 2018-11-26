#! /usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_srvs.srv import Empty, EmptyResponse




pose_x = 0
pose_y = 0
pose_z = 0
orien_x = 0
orien_y = 0
orien_z = 0


def pose_callback(data):
    
    
    global pose_x, pose_y, pose_z
    global orien_x, orien_y, orien_z
    
    pose_x = data.pose.pose.position.x
    pose_y = data.pose.pose.position.y
    pose_z = data.pose.pose.position.z
    
    orien_x = data.pose.pose.orientation.x
    orien_y = data.pose.pose.orientation.y
    orien_z = data.pose.pose.orientation.z
    
    

def srv_callback(request):
    
    global pose_x, pose_y, pose_z
    global orien_x, orien_y, orien_z
    
    rospy.loginfo("printing the pose and the orientation on the screen")
    rospy.loginfo("Pose :" + str(pose_x) + "," + str(pose_y) + "," + str(pose_z))
    rospy.loginfo("Orientation :" + str(orien_x) + "," + str(orien_y) + "," 
    + str(orien_z))
    
    return EmptyResponse()

def run():
    
    
    rospy.init_node("pose_estimate_service_server")
    
    rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, pose_callback)
    service = rospy.Service("get_pose_srv", Empty, srv_callback)
    
    
    rospy.spin()
    
    
if __name__ == "__main__":
    run()
    