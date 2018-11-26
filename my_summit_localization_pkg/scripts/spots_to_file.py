#! /usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from my_summit_localization_pkg.srv import MyServiceMessage, MyServiceMessageResponse
import yaml


"""
Class provides a service that saves poses to a file
the service is named /save_spot. 
The service uses a custom service message,
# request 
string label # label of the spot
# response
bool sucess
string message

"""
class SaveSpots(object):
    def __init__(self, srv_name='/save_spot', label_1='turtle', label_2='table',
        label_3='room'):
        
        self._srv_name = srv_name
        self._pose = PoseWithCovarianceStamped()
        self._service = rospy.Service(self._srv_name, MyServiceMessage, 
        self.srv_callback)
        self._pub_pose = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, 
        self.sub_callback)
        
        # dict to write to file
        self._dict = {label_1: self._pose, label_2: self._pose, 
            label_3: self._pose }
            
    def sub_callback(self, data):
        self._pose = data
        
    def srv_callback(self, request):
        
        label = request.label
        response = MyServiceMessageResponse()
        label_1='turtle'
        label_2='table'
        label_3='room'
        
        
        if label == label_1:
            self._dict[label_1] = self._pose
            response.message = "Saved for turtle"
            
        elif label == label_2:
            self._dict[label_2] = self._pose
            response.message = "Saved for table"
            
        elif label == label_3:
            self._dict[label_3] = self._pose
            response.message = "Saved for room"
            
        elif label == "end":
            # end and save file
            with open('spots.yaml', 'w') as file:
                # yaml.dump(self._dict, file, default_flow_style=False)
                
                for key, value in self._dict.iteritems():
                    if value:
                        file.write(str(key) +':\n')
                        file.write(str(value) + '\n')
                
                        
                
                response.message = "Saved all requested poses"
        
        else:
            response.message = "No label with this name"
            
        response.navigation_sucessfull = True
        
        return response
        

if __name__ == "__main__":
    rospy.init_node('spot_recorder_node')
    save_spots = SaveSpots()
    rospy.spin()