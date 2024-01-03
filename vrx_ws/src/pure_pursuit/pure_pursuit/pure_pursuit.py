import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Float64
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


class PurePursuit(Node):
    def __init__(self):
        super().__init__('pure_pursuit_node')

        self.right_thruster_pub = self.create_publisher(
            Float64,
            "/wamv/thrusters/right/thrust",
            10
        )

        self.left_thruster_pub = self.create_publisher(
            Float64,
            "/wamv/thrusters/left/thrust",
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
        self.myPos0 = [0.0]*2
        self.myAng = 0.0 #自分の角度を保存

        self.goal_index = 0
        self.my_index = 0
        self.alfa = 0.0
        self.ld = 0.0

        self.left_thruster = 0.0
        self.right_thruster = 0.0

    def imu_data_callback(self,msg):
        angle_ = euler_from_quaternion(msg.orientation)
        self.myAng = angle_[2]
        
    def pose_data_callback(self, msg):
        self.myPos[0] = msg.poses[self.my_index].position.x
        self.myPos[1] = msg.poses[self.my_index].position.y
        self.goalPosX = msg.poses[self.goal_index].position.x
        self.goalPosY = msg.poses[self.goal_index].position.y

        distance = [0.0]*2
        distance[0] = self.goalPosX-self.myPos[0]
        distance[1] = self.goalPosY-self.myPos[1]

        self.alfa = math.atan2(distance[0],distance[1]) - self.myAng
        self.ld = np.linalg.norm(distance)

        sin_alfa = math.asin(self.alfa)
        if(self.ld!=2*sin_alfa):
            if(self.alfa<0):
                self.right_thruster = ((self.ld+2*sin_alfa)/(self.ld-2*sin_alfa))*1000
                self.left_thruster = 1000
            else:
                self.left_thruster = ((self.ld-2*sin_alfa)/(self.ld-2*sin_alfa))*1000
                self.right_thruster = 1000
            self.right_thruster_pub.publish(self.right_thruster)
            self.left_thruster_pub.publish(self.left_thruster)


       
def main(args=None):
    rclpy.init(args=args)
    pure_pursuit_node = PurePursuit()
    rclpy.spin(pure_pursuit_node)
    pure_pursuit_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
