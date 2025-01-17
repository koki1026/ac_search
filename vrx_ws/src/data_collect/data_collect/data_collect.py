import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Float64
from std_msgs.msg import Float32
from std_msgs.msg import Bool
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
        super().__init__('data_collect_node')

        self.declare_parameter("data_write",False)
        self.DATA_WRITE = False

        self.declare_parameter("wave_direction",0.0)
        self.declare_parameter("wave_gain",3.0)
        self.declare_parameter("wave_period",5)
        self.declare_parameter("wave_stepness",0)
        self.waveParameterDirection = self.get_parameter("wave_direction").value #波の方向
        self.waveParameterGain = self.get_parameter("wave_gain").value #波の上がり方
        self.waveParameterPeriod = self.get_parameter("wave_period").value #波の周期（*2s）
        self.waveParameterStepness = self.get_parameter("wave_stepness").value #波のピークの尖り具合

        self.done = True

        # エピソードの開始を受け取るコールバック関数
        self.done_sub = self.create_subscription(
            Bool,
            '/wamv/done',
            self.done_callback,
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

        self.collect_windSpeed_sub = self.create_subscription(
            Float32,
            '/vrx/debug/wind/speed',
            self.wind_speed_data_callback,
            10
        )

        self.collect_windDirection_sub = self.create_subscription(
            Float32,
            '/vrx/debug/wind/direction',
            self.wind_direction_data_callback,
            10
        )

        self.writeTimer = self.create_timer(
            0.01,
            self.onTick
        )

        self.goalPosX = 0.0 #ゴールのx位置を保存
        self.goalPosY = 0.0 #ゴールのy位置を保存
        self.myPosX = 0.0 #自分のx位置を保存
        self.myPosY = 0.0 #自分のy位置を保存
        self.PosDegX = 0.0 #ゴールまでのx距離を保存
        self.PosDegY = 0.0 #ゴールまでのy距離を保存
        self.myVelX = 0.0 #自分のX方向速度を保存
        self.myVelY = 0.0 #自分のY方向速度を保存
        self.myAng = 0.0  #現在のyaw角を保存
        self.myAngVel = 0.0 #自分のxy平面角速度を保存
        self.myLeftTPos = 0.0 #自分の左スラスター出力（横）を保存
        self.myRightTPos = 0.0 #自分の右スラスター出力（横）を保存
        self.myLeftTTrust = 0.0 #自分の左スラスター出力（縦）を保存
        self.myRightTTrust = 0.0 #自分の右スラスター出力（縦）を保存
        self.windSpeed = 0.0
        self.windDirection = 0.0

        self.PoseHeaderStamp = 0.0
        self.ImuHeaderStamp = 0.0

    def done_callback(self,msg):
        self.done = msg.data
        

    def imu_data_callback(self,msg):
        time = msg.header.stamp.sec + ((msg.header.stamp.nanosec/1000000)*0.001)
        timeDlta = time - self.ImuHeaderStamp
        self.ImuHeaderStamp = time
        angle_ = euler_from_quaternion(msg.orientation)
        self.myAngVel = (angle_[2] - self.myAng) * np.reciprocal(timeDlta)
        self.myAng = angle_[2]
        
    def pose_data_callback(self,msg):
        time = msg.header.stamp.sec + ((msg.header.stamp.nanosec/1000000)*0.001)
        timeDlta = time - self.PoseHeaderStamp
        self.PoseHeaderStamp = time
        self.myVelX = (msg.poses[4].position.x - self.myPosX) * np.reciprocal(timeDlta)
        self.myVelY = (msg.poses[4].position.y - self.myPosY) * np.reciprocal(timeDlta)
        self.myPosX = msg.poses[4].position.x
        self.myPosY = msg.poses[4].position.y
        self.goalPosX = msg.poses[0].position.x
        self.goalPosY = msg.poses[0].position.y
        self.PosDegX = self.goalPosX - self.myPosX
        self.PosDegY = self.goalPosY - self.myPosY

    def left_thraster_pos_data_callback(self,msg):
        self.myLeftTPos = msg.data

    def right_thraster_pos_data_callback(self,msg):
        self.myRightTPos = msg.data

    def left_thraster_trust_data_callback(self,msg):
        self.myLeftTTrust = msg.data

    def right_thraster_trust_data_callback(self,msg):
        self.myRightTTrust = msg.data

    def wind_direction_data_callback(self,msg):
        self.windDirection = msg.data

    def wind_speed_data_callback(self,msg):
        self.windSpeed = msg.data

    def onTick(self):
        self.DATA_WRITE = self.get_parameter("data_write").value
        if(self.DATA_WRITE):
            datalist = [str(self.goalPosX), " ", str(self.goalPosY), " ", str(self.myPosX), " ", str(self.myPosY), " ", str(self.PosDegX), " ", str(self.PosDegY), " ", str(self.myVelX), " ", str(self.myVelY), " ", str(self.myAng), " ", str(self.myAngVel), " ", str(self.myLeftTPos), " ", str(self.myLeftTTrust), " ", str(self.myRightTPos), " ", str(self.myRightTTrust), " ", str(self.waveParameterDirection), " ", str(self.waveParameterGain), " ", str(self.waveParameterPeriod), " ", str(self.waveParameterStepness), " ", str(self.windDirection), " ", str(self.windSpeed),'\n']
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
