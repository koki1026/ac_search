import pickle
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseArray
from std_msgs.msg import Bool



class makeExpertData(Node):
    def __init__(self):
        super().__init__('makeExpertData')

        # サブスクリプションの宣言
        '''
        # msg.linear.x = 現在速度
        # msg.angular.z = 現在角度
        # msg.angulear.x = 現在角速度
        '''
        self.create_subscription(Twist, '/asv/cmd_vel', self.cmd_vel_callback, 10)
        '''
        # msg.poses = [現在位置, 目標地点, 次の目標地点]
        '''
        self.create_subscription(PoseArray, '/asv/waypoints', self.waypoints_callback, 10)
        '''
        # エピソードの開始と終了を判定するコールバック
        '''
        self.create_subscription(Bool, '/asv/done', self.done_callback, 10)
        '''
        # 書き込み全体の終了を判定するコールバック
        '''
        self.create_subscription(Bool, '/asv/final', self.final_callback, 10)

        # 変数の宣言
        self.myVel = 0.0
        self.myAngle = 0.0
        self.myAngleVel = 0.0
        self.myPose = [0.0] * 2
        self.targetPose = [0.0] * 2
        self.nextTargetPose = [0.0] * 2
        self.windSpeed = 0.0
        self.windDirection = 0.0
        self.waveLevel = 0.0
        self.waveDirection = 0.0
        self.dane = True
        self.preDane = True

        #データの保存先
        self.action_data = []
        self.observation_data = []
        self.info_data = []
        
        # タイマーコールバック関数を宣言
        '''
        # 一秒ごとにaction, observation, next_observation, reward, done, infoを保存
        '''
        self.create_timer(1.0, self.timer_callback)

    def cmd_vel_callback(self, msg):
        self.myVel = msg.linear.x
        self.myAngle = msg.angular.z
        self.myAngleVel = msg.angular.x
    
    def waypoints_callback(self, msg):
        self.myPose[0] = msg.poses[0].position.x
        self.myPose[1] = msg.poses[0].position.y
        self.targetPose[0] = msg.poses[1].position.x
        self.targetPose[1] = msg.poses[1].position.y
        self.nextTargetPose[0] = msg.poses[2].position.x
        self.nextTargetPose[1] = msg.poses[2].position.y

    def done_callback(self, msg):
        self.dane = msg.data

    def final_callback(self, msg):
        if msg.data == True:
            self.save_data()

    def timer_callback(self):
        episode_status = self.episode_check()
        if episode_status == 0:
            self.reset() # エピソードの開始
        elif episode_status == 1:
            self.final_append() # エピソードの終了
        elif episode_status == 2:
            self.action_data.append([self.myVel, self.myAngle])
            self.observation_data.append([self.myPose[0], self.myPose[1], self.targetPose[0], self.targetPose[1]])
            self.info_data.append(0)

    def reset(self):
        pass
    def final_append(self):
        pass

    def episode_check(self):
        if self.preDane == False and self.dane == True:
            self.preDane = self.dane
            return 1
        elif self.preDane == True and self.dane == False:
            self.preDane = self.dane
            return 0
        elif self.preDane == False and self.dane == False:
            return 2
        else:
            return 3

    def save_data(self):
        path = 'rollout.pkl'
        with open(path, mode='wb') as f:
            pickle.dump([self.action_data, self.observation_data, self.info_data], f)

def main(args=None):
    rclpy.init(args=args)
    makeExpertData_node = makeExpertData()
    rclpy.spin(makeExpertData_node)
    makeExpertData_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
