import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from pid import PID

class VehicleControlNode(Node):
    def __init__(self):
        super().__init__('vehicle_control_node')
        self.vehicle_control_sub = self.create_subscription(
            Twist,
            'vehicle_control_topic',
            self.vehicle_control_callback,
            10
        )

        self.vehicle_command_pub = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

        # ゲームマスターが指示を出す周期（秒）
        self.command_update_interval = 0.1

        # タイマーを設定して一定周期ごとにエージェントに指示を出す
        self.command_update_timer = self.create_timer(
            self.command_update_interval,
            self.update_agent_commands
        )

        # PID制御用のパラメータ（適切な値に調整が必要）
        self.kp = 1.0
        self.ki = 0.1
        self.kd = 0.01

        self.pid_controller = PID(self.kp, self.ki, self.kd)
        self.pid_controller.output_limits = (-1.0, 1.0)  # 出力の範囲（適宜調整）

        # 目標速度と角速度を保存
        self.linear_speed = 0.0
        self.angular = 0.0

        self.current_yaw = 0.0  # 現在のグローバルな角度

    def vehicle_control_callback(self, msg):
        # ノードから受け取った速度と角速度
        self.linear_speed = msg.linear.x
        self.angular = msg.angular.z


    def update_vehicle_command(self):
        self.vehicle_command_pub.publish()

def main(args=None):
    rclpy.init(args=args)
    vehicle_control_node = VehicleControlNode()
    rclpy.spin(vehicle_control_node)
    vehicle_control_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()