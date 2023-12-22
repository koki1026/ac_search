import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Float64
import numpy as np

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

class DatacollectNode(Node):
    def __init__(self):
        super().__init__('agent_control_node')

        self.declare_parameter("data_write",False)
        self.DATA_WRITE = False

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
        self.collect_LeftTPose_sub = self.create_subscription(
            Float64,
            '/wamv/thrusters/left/pos',
            self.left_thraster_pos_data_callback,
            10
        )
        self.collect_Pose_sub = self.create_subscription(
            Float64,
            '/wamv/thrusters/left/thrust',
            self.left_thraster_trust_data_callback,
            10
        )
        self.collect_Pose_sub = self.create_subscription(
            Float64,
            '/wamv/thrusters/right/pos',
            self.right_thraster_pos_data_callback,
            10
        )
        self.collect_Pose_sub = self.create_subscription(
            Float64,
            '/wamv/thrusters/right/thrust',
            self.right_thraster_trust_data_callback,
            10
        )

        self.writeTimer = self.create_timer(
            0.01,
            self.onTick
        )

        self.myAng = 0.0  #現在のyaw角を保存
        self.myPosX = 0.0 #自分のx位置を保存
        self.myPosY = 0.0 #自分のy位置を保存
        self.myLeftTPos = 0.0 #自分の左スラスター出力（横）を保存
        self.myRightTPos = 0.0 #自分の右スラスター出力（横）を保存
        self.myLeftTTrust = 0.0 #自分の左スラスター出力（縦）を保存
        self.myRightTTrust = 0.0 #自分の右スラスター出力（縦）を保存
        self.myVelX = 0.0 #自分のX方向速度を保存
        self.myVelY = 0.0 #自分のY方向速度を保存
        self.myAngVel = 0.0 #自分のxy平面角速度を保存
        self.goalPosX = 0.0 #ゴールのx位置を保存
        self.goalPosY = 0.0 #ゴールのy位置を保存
        self.PosDegX = 0.0 #ゴールまでのx距離を保存
        self.PosDegY = 0.0 #ゴールまでのy距離を保存
        self.SmyAng = "0.0"  #現在のyaw角を保存
        self.SmyPosX = "0.0" #自分のx位置を保存
        self.SmyPosY = "0.0" #自分のy位置を保存
        self.SmyLeftTPos = "0.0" #自分の左スラスター出力（横）を保存
        self.SmyRightTPos = "0.0" #自分の右スラスター出力（横）を保存
        self.SmyLeftTTrust = "0.0" #自分の左スラスター出力（縦）を保存
        self.SmyRightTTrust = "0.0" #自分の右スラスター出力（縦）を保存
        self.SmyVelX = "0.0" #自分のX方向速度を保存
        self.SmyVelY = "0.0" #自分のY方向速度を保存
        self.SmyAngVel = "0.0" #自分のxy平面角速度を保存
        self.SgoalPosX = "0.0" #ゴールのx位置を保存
        self.SgoalPosY = "0.0" #ゴールのy位置を保存
        self.SPosDegX = "0.0" #ゴールまでのx距離を保存
        self.SPosDegY = "0.0" #ゴールまでのy距離を保存

    def imu_data_callback(self,msg):
        angle_ = euler_from_quaternion(msg.orientation)
        self.myAng = angle_[2]
        self.SmyAng = str(self.myAng)
        
    def pose_data_callback(self,msg):
        self.myPosX = msg.poses[4].position.x
        self.myPosY = msg.poses[4].position.y
        self.goalPosX = msg.poses[0].position.x
        self.goalPosY = msg.poses[0].position.y
        self.SmyPosX = str(self.myPosX)
        self.SmyPosY = str(self.myPosY)
        self.SgoalPosX = str(self.goalPosX)
        self.SgoalPosY = str(self.goalPosY)

    def left_thraster_pos_data_callback(self,msg):
        self.myLeftTPos = msg.data
        self.SmyLeftTPos = str(self.myLeftTPos)

    def right_thraster_pos_data_callback(self,msg):
        self.myRightTPos = msg.data
        self.SmyRightTPos = str(self.myRightTPos)

    def left_thraster_trust_data_callback(self,msg):
        self.myLeftTTrust = msg.data
        self.SmyLeftTTrust = str(self.myLeftTTrust)

    def right_thraster_trust_data_callback(self,msg):
        self.myRightTTrust = msg.data
        self.SmyRightTTrust = str(self.myRightTTrust)

    def onTick(self):
        self.DATA_WRITE = self.get_parameter("data_write").value
        if(self.DATA_WRITE):
            datalist = [self.SgoalPosX, " ", self.SgoalPosY, " ", self.SmyPosX, " ", self.SmyPosY, " ", self.SPosDegX, " ", self.SPosDegY, " ", self.SmyAng, '\n']
            f = open('dataset.txt', 'a')
            f.writelines(datalist)
            f.close()
       
def main(args=None):
    rclpy.init(args=args)
    data_collect_node = DatacollectNode()
    rclpy.spin(data_collect_node)
    data_collect_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
