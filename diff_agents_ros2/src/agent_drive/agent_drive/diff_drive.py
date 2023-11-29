import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster, TransformStamped
from agent_messages.msg import AgentTf, AgentCmd  # your_msgsは適切なメッセージ定義に置き換える
import numpy as np
import math

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

class AgentTfPublisherNode(Node):
    def __init__(self, agent_index):
        super().__init__('agent_tf_publisher_node')
        self.agent_index = agent_index
        self.tf_broadcaster = TransformBroadcaster(self)

    def publish_tf(self):
        tf_msg = TransformStamped()
        tf_msg.header.stamp = self.get_clock().now().to_msg()
        tf_msg.header.frame_id = 'world'
        tf_msg.child_frame_id = f'agent_{self.agent_index}'
        tf_msg.transform.translation.x = 0.0  # 仮の座標（実際にはエージェントの座標にする）
        tf_msg.transform.translation.y = 0.0
        tf_msg.transform.translation.z = 0.0
        tf_msg.transform.rotation.x = 0.0
        tf_msg.transform.rotation.y = 0.0
        tf_msg.transform.rotation.z = 0.0
        tf_msg.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(tf_msg)

        agent_tf_msg = AgentTf()
        agent_tf_msg.x = tf_msg.transform.translation.x
        agent_tf_msg.y = tf_msg.transform.translation.y
        agent_tf_msg.z = tf_msg.transform.translation.z
        agent_tf_msg.roll, agent_tf_msg.pitch, agent_tf_msg.yaw = self.get_rpy_from_quaternion(tf_msg.transform.rotation)
        agent_tf_msg.agent_index = self.agent_index

        self.agent_tf_pub.publish(agent_tf_msg)

    def get_rpy_from_quaternion(self, quaternion):
        roll, pitch, yaw = euler_from_quaternion([quaternion.x, quaternion.y, quaternion.z, quaternion.w])
        return roll, pitch, yaw

def main():
    rclpy.init()
    agent_index = 1  # 各エージェントには一意のインデックスが必要
    agent_tf_publisher_node = AgentTfPublisherNode(agent_index)
    rclpy.spin(agent_tf_publisher_node)
    agent_tf_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()