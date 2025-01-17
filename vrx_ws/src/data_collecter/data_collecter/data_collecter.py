# Collect expert data 
import rclpy
import math
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu

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

class dataCollecter(Node):
    def __init__(self):
        super().__init__('data_collect_node')

        #declare parameter
        self.myPose = [0.0] * 2
        self.targetPose = [0.0] * 2
        self.nextTargetPose = [0.0] * 2
        self.PoseMember = [self.myPose, self.targetPose, self.nextTargetPose]
        self.windSpeed = 0.0
        self.windDirection = 0.0
        self.waveLevel = 1.0
        self.waveDirection = 0.0
        self.done = True
        self.myVel = 0.0
        self.myAngle = 0.0
        self.myAngleVel = 0.0
        self.left_thrust = 0.0
        self.right_thrust = 0.0


        #decleare parameter for culcrate
        self.myAccel = 0.0
        self.next_index = 0
        self.NowTime = 0.0
        self.PreTime = 0.0
        self.prePose = [0.0] * 2

        #make publisher
        self.twist_pub = self.create_publisher(
            Twist,
            "expert/asv/cmd_vel",
            10
        )
        self.pose_pub = self.create_publisher(
            PoseArray,
            "expert/asv/waypoints",
            10
        )
        self.done_pub = self.create_publisher(
            Bool,
            "expert/asv/done",
            10
        )
        self.environment_pub = self.create_publisher(
            Pose,
            "expert/asv/environment",
            10
        )
        self.thrust_pub = self.create_publisher(
            Pose,
            "expert/asv/thrust",
            10
        )

        #make subscriber
        self.collect_imu_sub = self.create_subscription(
            Imu,
            '/world/sydney_regatta/model/wamv/link/wamv/imu_wamv_link/sensor/imu_wamv_sensor/imu',
            self.imu_callback,
            10
        )
        self.collect_Pose_sub = self.create_subscription(
            PoseArray,
            'vrx/pose',
            self.waypoints_callback,
            10
        )
        self.collect_Pose_sub = self.create_subscription(
            Bool,
            'vrx/done',
            self.done_callback,
            10
        )
        self.collect_wind_direction_sub = self.create_subscription(
            Float32,
            '/vrx/debug/wind/direction',
            self.wind_direction_callback,
            10
        )
        self.collect_wind_speed_sub = self.create_subscription(
            Float32,
            '/vrx/debug/wind/speed',
            self.wind_speed_callback,
            10
        )
        self.collect_index_sub = self.create_subscription(
            Int32,
            '/vrx/index',
            self.index_callback,
            10
        )
        self.collect_thrust_sub = self.create_subscription(
            Float64,
            '/wamv/thrusters/left/thrust',
            self.left_thrust_callback,
            10
        )
        self.collect_thrust_sub = self.create_subscription(
            Float64,
            '/wamv/thrusters/right/thrust',
            self.right_thrust_callback,
            10
        )

        # 速度を計算するためのタイマー
        self.writeTimer = self.create_timer(
            0.1,
            self.onTick
        )

    def onTick(self):
        self.myVel = math.sqrt((self.myPose[0]-self.prePose[0])**2 + (self.myPose[1]-self.prePose[1])**2) / 0.1
        self.prePose = self.myPose.copy()

    def imu_callback(self, msg):
        self.myAngleVel = msg.angular_velocity.z
        self.myAngle = euler_from_quaternion(msg.orientation)[2]
        TwistMsg = Twist()
        TwistMsg.linear.x = self.myVel
        TwistMsg.angular.z = self.myAngle
        TwistMsg.angular.x = self.myAngleVel
        self.twist_pub.publish(TwistMsg)

    def waypoints_callback(self, msg):
        self.myPose[0] = msg.poses[0].position.x
        self.myPose[1] = msg.poses[0].position.y

        self.targetPose[0] = msg.poses[1+self.next_index].position.x
        self.targetPose[1] = msg.poses[1+self.next_index].position.y
        self.nextTargetPose[0] = msg.poses[2+self.next_index].position.x
        self.nextTargetPose[1] = msg.poses[2+self.next_index].position.y

        PoseArrayMsg = PoseArray()
        for i in range(3):
            pose  = Pose()
            pose.position.x = self.PoseMember[i][0]
            pose.position.y = self.PoseMember[i][1]
            PoseArrayMsg.poses.append(pose)
        self.pose_pub.publish(PoseArrayMsg)

    def done_callback(self, msg):
        self.done = msg.data
        done = Bool()
        done.data = self.done
        self.done_pub.publish(done)

    def wind_direction_callback(self, msg):
        self.windDirection = msg.data
    
    def wind_speed_callback(self, msg):
        self.windSpeed = msg.data
        EnvironmentMsg = Pose()
        EnvironmentMsg.orientation.x = self.windSpeed
        EnvironmentMsg.orientation.y = np.radians(self.windDirection) -self.myAngle
        EnvironmentMsg.orientation.z = self.waveLevel
        EnvironmentMsg.orientation.w = np.radians(self.waveDirection) - self.myAngle
        self.environment_pub.publish(EnvironmentMsg)

    def index_callback(self, msg):
        self.next_index = msg.data

    def left_thrust_callback(self, msg):
        self.left_thrust = msg.data
        ThrustMsg = Pose()
        ThrustMsg.position.x = self.left_thrust
        ThrustMsg.position.y = self.right_thrust
        self.thrust_pub.publish(ThrustMsg)

    def right_thrust_callback(self, msg):
        self.right_thrust = msg.data


def main(args=None):
    rclpy.init(args=args)
    data_collect_node = dataCollecter()
    rclpy.spin(data_collect_node)
    data_collect_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()