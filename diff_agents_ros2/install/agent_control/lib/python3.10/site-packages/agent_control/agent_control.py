import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import numpy as np

class AgentControlNode(Node):
    def __init__(self):
        super().__init__('agent_control_node')
        self.vehicle_control_sub = self.create_subscription(
            Twist,
            'agent_control_topic',
            self.vehicle_control_callback,
            10
        )

        self.vehicle_command_pub = self.create_publisher(
            Twist,
            'agent_command_topic',
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
        self.linear_speed = 0.0
        self.angular = 0.0

        self.current_yaw = 0.0  # 現在のグローバルな角度

    def vehicle_control_callback(self, msg):
        # head_quarterノードから受け取った速度と角速度
        self.linear_speed = msg.linear.x
        self.angular = msg.angular.z


    def update_agent_command(self):
        #agentの現在角と目標角の差異を保存
        #差異角と目標速度をもとにベクトルを作成
        #x速度とz速度を生成
        vehicle_command = Twist()
        vehicle_command.linear.x = self.linear_speed * np.sin(np.radians(self.angular))
        vehicle_command.angular.z = self.linear_speed * np.cos(np.radians(self.angular))
        self.vehicle_command_pub.publish(vehicle_command)

def main(args=None):
    rclpy.init(args=args)
    vehicle_control_node = AgentControlNode()
    rclpy.spin(vehicle_control_node)
    vehicle_control_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()