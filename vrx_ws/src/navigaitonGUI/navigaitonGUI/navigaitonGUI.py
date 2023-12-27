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

#すべてのトピックをサブスクライブしてひとつにまとめる
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

class NavigaitonGUI(Node):
    def __init__(self):
        super().__init__('navigation_GUI_node')

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

        self.writeTimer = self.create_timer(
            2,
            self.onTick
        )

        self.goalPosX = 0.0 #ゴールのx位置を保存
        self.goalPosY = 0.0 #ゴールのy位置を保存
        self.myPosX = 0.0 #自分のx位置を保存
        self.myPosY = 0.0 #自分のy位置を保存
        self.myAng = 0.0 #自分の角度を保存
        self.buoys_size = 39
        self.buoys = [[0]*2]*self.buoys_size
        self.goal_index = 0

    def imu_data_callback(self,msg):
        angle_ = euler_from_quaternion(msg.orientation)
        self.myAng = angle_[2]
        
    def pose_data_callback(self, msg):
        self.myPosX = msg.poses[40].position.x
        self.myPosY = msg.poses[40].position.y
        self.goalPosX = msg.poses[self.goal_index].position.x
        self.goalPosY = msg.poses[self.goal_index].position.y
        for i in range(39):
            self.buoys[i][0] = msg.poses[i].position.x
            self.buoys[i][1] = msg.poses[i].position.y


    def onTick(self):
        plt.figure()

        #座標をプロット
        x_values = [buoy[0] for buoy in self.buoys]
        y_values = [buoy[1] for buoy in self.buoys]
        plt.scatter(x_values, y_values, color='black', label='buoys')
        plt.scatter(self.goalPosX, self.goalPosY, color='red', label='goal')
        plt.scatter(self.myPosX, self.myPosY, color='blue', label='state')
        
        

        #タイトルとラベル
        plt.title('buoy&boat')
        plt.xlabel('X_axis')
        plt.ylabel('Y_axis')

        #グリッドの表示
        plt.grid(True)

        plt.show()


       
def main(args=None):
    rclpy.init(args=args)
    navigation_GUI_node = NavigaitonGUI()
    rclpy.spin(navigation_GUI_node)
    navigation_GUI_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
