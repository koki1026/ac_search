'''
makeExpertData.pyのコールバック関数に仮データを渡してデバッグするためのクラス
'''
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose

class makeExpertData(Node):
    def __init__(self):
        self.myVel = 0.0
        self.myAngle = 0.0
        self.myAngleVel = 0.0
        self.myPose = [0.0] * 2
        self.targetPose = [0.0] * 2
        self.nextTargetPose = [0.0] * 2
        self.PoseMember = [self.myPose, self.targetPose, self.nextTargetPose]
        self.windSpeed = 0.0
        self.windDirection = 0.0
        self.waveLevel = 0.0
        self.waveDirection = 0.0
        # 動的パラーメータを宣言
        self.declare_parameter('done', 0)
        self.done = self.get_parameter('done').get_parameter_value().bool_value

        # 動的パラメータの更新関数を宣言
        self.writeTimer = self.create_timer(
            0.01,
            self.onTick
        )


        #make publisher
        self.twist_pub = self.create_publisher(
            Twist,
            "/asv/cmd_vel",
            10
        )
        self.pose_pub = self.create_publisher(
            PoseArray,
            "/asv/waypoints",
            10
        )
        self.done_pub = self.create_publisher(
            Bool,
            "/asv/done",
            10
        )

    def onTick(self):
        poses = PoseArray()
        for i in range(3):
            pose = Pose()
            pose.position.x = self.PoseMember[i][0]
            pose.position.y = self.PoseMember[i][1]
            pose.position.z = 0.0
            pose.orientation.x = 0.0
            pose.orientation.y = 0.0
            pose.orientation.z = 0.0
            pose.orientation.w = 0.0
            poses.poses.append(pose)
        TwistMsg = Twist()
        TwistMsg.linear.x = self.myVel
        TwistMsg.angular.z = self.myAngle
        TwistMsg.angular.x = self.myAngleVel
        self.done = self.get_parameter('done').get_parameter_value().integer_value
        self.done_pub.publish(self.done)
        self.pose_pub.publish(poses)
        self.twist_pub.publish(TwistMsg)
