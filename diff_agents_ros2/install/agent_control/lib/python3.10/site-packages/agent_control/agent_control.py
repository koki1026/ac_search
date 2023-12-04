import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
import numpy as np

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

class AgentControlNode(Node):
    def __init__(self):
        super().__init__('agent_control_node')
        self.vehicle_control_sub = self.create_subscription(
            Twist,
            'agent_control_topic',
            self.vehicle_control_callback,
            10
        )

        self.imu_sub = self.create_subscription(
            Imu,
            'imu',
            self.imu_sensor_callback,
            10
        )

        self.vehicle_command_pub = self.create_publisher(
            Twist,
            'agent_command_topic',
            10
        )

        self.message_status = self.create_publisher(
            Twist,
            'angleDifference',
            10
        )

        # ゲームマスターが指示を出す周期（秒）
        self.command_update_interval = 1.0

        # タイマーを設定して一定周期ごとにエージェントに指示を出す
        self.command_update_timer = self.create_timer(
            self.command_update_interval,
            self.update_agent_command
        )

        # 目標速度と角速度を保存
        self.targetSpeed = 0.0
        self.targetAngularDeg = 0.0
        self.targetAngule = 0.0

        self.currentAngle = 0.0  # 現在のグローバルな角度

        self.angleDifference = self.targetAngule - self.currentAngle

    def vehicle_control_callback(self, msg):
        # head_quarterノードから受け取った速度と角速度
        self.targetSpeed = msg.linear.x
        self.targetAngularDeg = msg.angular.z
        self.targetAngule = np.radians(self.targetAngularDeg)


    def imu_sensor_callback(self, msg):
        angle_ = euler_from_quaternion(msg.orientation)
        self.currentAngle = angle_[2]
        self.angleDifference = self.currentAngle - self.targetAngule

    def update_agent_command(self):
        #agentの現在角と目標角の差異を保存
        #差異角と目標速度をもとにベクトルを作成
        #x速度とz速度を生成
        vehicle_command = Twist()
        vehicle_command.linear.x = abs(self.targetSpeed * np.cos(self.angleDifference))
        vehicle_command.angular.z = self.targetSpeed * np.sin(self.angleDifference)
        self.vehicle_command_pub.publish(vehicle_command)

        agentDifference_command = Twist()
        agentDifference_command.linear.x = self.targetSpeed
        agentDifference_command.linear.y = self.targetAngule
        agentDifference_command.linear.z = self.currentAngle
        agentDifference_command.angular.z = self.angleDifference
        self.message_status.publish(agentDifference_command)

def main(args=None):
    rclpy.init(args=args)
    vehicle_control_node = AgentControlNode()
    rclpy.spin(vehicle_control_node)
    vehicle_control_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()