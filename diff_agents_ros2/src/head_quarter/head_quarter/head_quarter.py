import rclpy
from rclpy.node import Node
from agent_messages.msg import AgentTF, AgentCmd
from geometry_msgs.msg import Twist

class GameMasterNode(Node):
    def __init__(self):
        super().__init__('game_master_node')
        self.agent_locations = {}  # エージェントの現在地を保存する辞書

        # エージェントの現在地を受け取るサブスクライバーを設定
        self.agent_location_sub = self.create_subscription(
            AgentTF,
            'agent_location_topic',
            self.agent_location_callback,
            10  # メッセージキューのサイズ
        )

        # ゲームマスターがエージェントに指示を出すトピックを作成
        self.agent_command_pub = self.create_publisher(
            AgentCmd,
            'agent_command_topic',
            10
        )

        # ゲームマスターが指示を出す周期（秒）
        self.command_update_interval = 5

        # タイマーを設定して一定周期ごとにエージェントに指示を出す
        self.command_update_timer = self.create_timer(
            self.command_update_interval,
            self.update_agent_commands
        )

    def agent_location_callback(self, msg):
        # エージェントの現在地を保存
        self.agent_locations[msg.agent_id] = {'x': msg.x, 'y': msg.y}

    def update_agent_commands(self):
        # 一定周期ごとにエージェントに速度と目標角度を指定
        for agent_id, location in self.agent_locations.items():
            # 仮の指示を生成（実際には適切な制御アルゴリズムに基づいて計算）
            command_msg = AgentCmd()
            command_msg.agent_index = agent_id
            command_msg.linar.x = 3.0  # 例として速度を3.0に指定
            command_msg.angular.z = 45.0  # 例として目標角度を45度に指定

            # エージェントに指示を出す
            self.agent_command_pub.publish(command_msg)

def main():
    rclpy.init()
    game_master_node = GameMasterNode()
    rclpy.spin(game_master_node)
    game_master_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()