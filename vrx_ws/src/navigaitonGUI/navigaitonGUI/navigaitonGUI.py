import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Int32MultiArray
import numpy as np
import matplotlib.pyplot as plt
from visualization_msgs.msg import MarkerArray, Marker
from std_msgs.msg import Bool
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
    marker_child.header.frame_id = "wamv/wamv/base_link/front_left_camera_sensor"
    marker_child.header.stamp = self.get_clock().now().to_msg()
    marker_child.ns = label
    marker_child.id = idx
    marker_child.type = Marker.SPHERE
    marker_child.action = Marker.ADD
        
    marker_child.pose.position.x = position[0]*0.1
    marker_child.pose.position.y = position[1]*0.1
    marker_child.scale.x = marker_child.scale.y = marker_child.scale.z = 1.0
    if(idx == self.goal_index): #ゴールの色は赤色
        marker_child.color.r = 1.0
        marker_child.color.g = 0.0
        marker_child.color.b = 0.0
        marker_child.color.a = 1.0
    elif(idx == self.goal_index+1): #ゴールの色は赤色
        marker_child.color.r = 1.0
        marker_child.color.g = 1.0
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
        marker_child.mesh_resource = "file:///home/gaia-22/ac_search/vrx_ws/src/navigaitonGUI/mesh/WAM-V-Base.dae"
        marker_child.mesh_use_embedded_materials = True

    return marker_child


class NavigaitonGUI(Node):
    def __init__(self):
        super().__init__('navigation_GUI_node')

        self.marker_pub = self.create_publisher(
            MarkerArray,
            "/vrx_markers",
            10
        )
        self.index_pub = self.create_publisher(
            Int32MultiArray,
            "/index_node",
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
        self.done = False
        self.done_pub = self.create_publisher(
            Bool,
            "/wamv/done",
            10
        )

        self.goalPosX = 0.0 #ゴールのx位置を保存
        self.goalPosY = 0.0 #ゴールのy位置を保存
        self.myPos = [0.0]*2
        self.myPos0 = [0.0]*2
        self.myAng = 0.0 #自分の角度を保存
        self.myAngOri = [0.0]*4
        self.buoys_size = 38
        self.buoys = [[0.0]*2]*self.buoys_size
        self.goal_index = 0
        self.my_index = self.buoys_size+1

    def imu_data_callback(self,msg):
        self.myAngOri[0] = msg.orientation.x
        self.myAngOri[1] = msg.orientation.y
        self.myAngOri[2] = msg.orientation.z
        self.myAngOri[3] = msg.orientation.w
        angle_ = euler_from_quaternion(msg.orientation)
        self.myAng = angle_[2]
        
    def pose_data_callback(self, msg):
        self.myPos[0] = msg.poses[self.my_index].position.x
        self.myPos[1] = msg.poses[self.my_index].position.y
        self.goalPosX = msg.poses[self.goal_index].position.x
        self.goalPosY = msg.poses[self.goal_index].position.y
        markers = MarkerArray()
        markers.markers.append(rviz_marker(self, self.myPos0, "wam_v", 100))
        for i in range(self.buoys_size):
            self.buoys[i][0] = msg.poses[i].position.x - self.myPos[0]
            self.buoys[i][1] = msg.poses[i].position.y - self.myPos[1]
            distance = np.linalg.norm(self.buoys)
            radian = math.atan2(self.buoys[i][1], self.buoys[i][0])
            angle = radian - self.myAng
            rela_buoy = [0.8]*2
            rela_buoy[0] = np.cos(angle)*distance
            rela_buoy[1] = np.sin(angle)*distance
            markers.markers.append(rviz_marker(self, rela_buoy, "marker: "+str(i), i))
        
        self.marker_pub.publish(markers)

        goal_dis = [0.0]*2
        goal_dis[0] = np.abs(self.myPos[0]-self.goalPosX)
        goal_dis[1] = np.abs(self.myPos[1]-self.goalPosY)
        if(np.linalg.norm(goal_dis) < 3.0):
            if(self.goal_index == self.buoys_size-30):
                self.done = True
                self.goal_index -= 1
                done = Bool()
                done.data = self.done
                self.done_pub.publish(done)
            self.goal_index+=1
        index_array = Int32MultiArray()
        data_array = []
        data_array.append(int(self.my_index))
        data_array.append(int(self.goal_index))
        index_array.data = data_array
        self.index_pub.publish(index_array)

       
def main(args=None):
    rclpy.init(args=args)
    navigation_GUI_node = NavigaitonGUI()
    rclpy.spin(navigation_GUI_node)
    navigation_GUI_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
