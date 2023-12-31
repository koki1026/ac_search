import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Float64
from std_msgs.msg import Float32
import numpy as np
import matplotlib.pyplot as plt
from visualization_msgs.msg import MarkerArray, Marker
# wave, goal , my, thruster l,r,lv,rv
def euler_from_quaternion(quaternion):                                                                   
        """クオータニオンからオイラー角を計算する関数                                                        
        Converts quaternion (w in last place) to euler roll, pitch, yaw                                           
        quaternion = [x, y, z, w]                                                                                 
        Bellow should be replaced when porting for ROS 2 Python tf_conversions is done.                           
        """                                                                                                      
        x = quaternion.x                                                                                          
        y = quaternion.y                                                                                          
        z = quaternion.z                                                                                          
        w = quaternion.w                                                                                          
                                                                                                                  
        sinr_cosp = 2 * (w * x + y * z)                                                                           
        cosr_cosp = 1 - 2 * (x * x + y * y)                                                                       
        roll      = np.arctan2(sinr_cosp, cosr_cosp)                                                              
                                                                                                                  
        sinp  = 2 * (w * y - z * x)                                                                               
        pitch = np.arcsin(sinp)                                                                                   
                                                                                                                  
        siny_cosp = 2 * (w * z + x * y)                                                                           
        cosy_cosp = 1 - 2 * (y * y + z * z)                                                                       
        yaw = np.arctan2(siny_cosp, cosy_cosp)                                                                    
                                         
        return roll, pitch, yaw

def rviz_marker(self, position: np.ndarray, label: str, idx: int):
    marker_child = Marker()
    marker_child.header.frame_id = "wamv/wamv/base_link"
    marker_child.header.stamp = self.get_clock().now().to_msg()
    marker_child.ns = label
    marker_child.id = idx
    marker_child.type = Marker.SPHERE
    marker_child.action = Marker.ADD
        
    marker_child.pose.position.x = position[0]*0.5
    marker_child.pose.position.y = position[1]*0.5
    marker_child.scale.x = marker_child.scale.y = marker_child.scale.z = 1.0
    print(position[0])
    if(idx == self.goal_index): #ゴールの色は赤色
        marker_child.color.r = 1.0
        marker_child.color.g = 0.0
        marker_child.color.b = 0.0
        marker_child.color.a = 1.0
    elif(idx == self.goal_index-1): #スタートの色は青色
        marker_child.color.r = 0.0
        marker_child.color.g = 0.0
        marker_child.color.b = 1.0
        marker_child.color.a = 1.0
    else: #他のマーカは黄色
        marker_child.color.r = 0.0
        marker_child.color.g = 0.0
        marker_child.color.b = 1.0
        marker_child.color.a = 1.0
    
    if(idx == 100):
        marker_child.type = Marker.MESH_RESOURCE
        marker_child.mesh_resource = "file:///home/koki-22/ac_search/vrx_ws/src/navigaitonGUI/mesh/WAM-V-Base.dae"
        marker_child.mesh_use_embedded_materials = True
        marker_child.pose.orientation.x = 
        marker_child.pose.orientation.y
        marker_child.pose.orientation.z
        marker_child.pose.orientation.w

    return marker_child


class NavigaitonGUI(Node):
    def __init__(self):
        super().__init__('navigation_GUI_node')

        self.marker_pub = self.create_publisher(
            MarkerArray,
            "/vrx_markers",
            10
        )

        self.collect_imu_sub = self.create_subscription(
            Imu,
            '/world/sydney_regatta/model/wamv/link/wamv/imu_wamv_link/sensor/imu_wamv_sensor/imu',
            self.imu_data_callback,
            10
        )
        self.collect_Pose_sub = self.create_subscription(
             PoseArray,
             '/world/sydney_regatta/dynamic_pose/info',
             self.pose_data_callback,
             10
        )

        self.goalPosX = 0.0 #ゴールのx位置を保存
        self.goalPosY = 0.0 #ゴールのy位置を保存
        self.myPos = [0.0]*2
        self.myAng = 0.0 #自分の角度を保存
        self.myAngOri = [0.0]*4
        self.buoys_size = 38
        self.buoys = [[0.0]*2]*self.buoys_size
        self.goal_index = 0

    def imu_data_callback(self,msg):
        angle_ = euler_from_quaternion(msg.orientation)
        self.myAng = angle_[2]
        
    def pose_data_callback(self, msg):
        self.myPos[0] = msg.poses[self.buoys_size+1].position.x
        self.myPos[1] = msg.poses[self.buoys_size+1].position.y
        self.goalPosX = msg.poses[self.goal_index].position.x
        self.goalPosY = msg.poses[self.goal_index].position.y
        markers = MarkerArray()
        markers.markers.append(rviz_marker(self, self.myPos, "wam_v", 100))
        for i in range(self.buoys_size):
            self.buoys[i][0] = msg.poses[i].position.x
            self.buoys[i][1] = msg.poses[i].position.y
            markers.markers.append(rviz_marker(self, self.buoys[i], "marker: "+str(i), i))

        self.marker_pub.publish(markers)

       
def main(args=None):
    rclpy.init(args=args)
    navigation_GUI_node = NavigaitonGUI()
    rclpy.spin(navigation_GUI_node)
    navigation_GUI_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
