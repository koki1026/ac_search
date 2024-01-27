import math
import pickle
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool
import imitation.data.types as types
from imitation.data.types import TransitionsMinimal



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
        '''
        # pose.x = windSpeed
        # pose.y = windDirection
        # pose.z = waveLevel
        # pose.w = waveDirection
        '''
        self.create_subscription(Pose, '/asv/environment', self.environment_callback, 10)

        # 変数の宣言
        self.myVel = 0.0
        self.myAngle = 0.0
        self.myAngleVel = 0.0
        self.myPose = [0.0] * 2
        self.prePose = [0.0] * 2
        self.targetPose = [0.0] * 2
        self.nextTargetPose = [0.0] * 2
        self.windSpeed = 0.0
        self.windDirection = 0.0
        self.waveLevel = 0.0
        self.waveDirection = 0.0
        self.dane = True
        self.preDane = True
        self.action = [[0.0]*14]*4
        self.action_index = 0
        self.action_start = False
        self.render_size = 800

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

    def environment_callback(self, msg):
        self.windSpeed = msg.position.x
        self.windDirection = msg.position.y
        self.waveLevel = msg.position.z
        self.waveDirection = msg.orientation.x

    def done_callback(self, msg):
        self.dane = msg.data

    def final_callback(self, msg):
        if msg.data == True:
            self.save_data()

    def timer_callback(self):
        episode_status = self.episode_check()
        if episode_status == 0:
            self.reset() # エピソードの開始
            print("episode status" , episode_status)
        elif episode_status == 1:
            self.final_append(self.action_index,self.myVel,self.myAngle,self.myAngleVel,self.myPose,self.prePose)
            print("episode status" , episode_status)
        elif episode_status == 2:
            action, action_checker = self.makeActionData(self.action_index,self.myVel,self.myAngle,self.myAngleVel,self.myPose,self.prePose)
            observation = self.makeObservationData(self.myPose,self.myAngle,self.targetPose,self.nextTargetPose,self.windSpeed,self.windDirection,self.waveLevel,self.waveDirection)

            # 種々のデータを更新
            self.prePose = self.myPose
            self.action_index = (self.action_index-1)%4
            # データをアペンド
            if(action_checker):
                self.action_data.append(action)
                print ("action: ", self.action_data)

            self.observation_data.append(observation)
            print ("observation: ")
            print("episode status:", episode_status)
            self.info_data.append([0])

    def makeActionData(self,action_index,myVel,myAngle,myAngleVel,myPose,prePose):
        #速度と角速度について挿入
        print("action_index",action_index)
        self.action[action_index][0] = myVel
        self.action[action_index][1] = myAngleVel
        #距離と方向、そして向きについて挿入
        distance = np.linalg.norm(np.array(myPose) - np.array(prePose))
        radian = math.atan2(myPose[0]-prePose[0], myPose[1]-prePose[1])
        for i in range(4):
            self.action[(action_index+i)%4][2+i*3] = distance
            self.action[(action_index+i)%4][3+i*3] = radian
            self.action[(action_index+i)%4][4+i*3] = myAngle
        action = self.action[(action_index+3)%4]

        if action_index == 1:
            self.action_start = True
        action_bool = self.action_start
        return action,action_bool
    
    def makeObservationData(self,myPose,myAngle,targetPose,nextTargetPose,windSpeed,windDirection,waveLevel,waveDirection):
        img = np.zeros((self.render_size,self.render_size,3), np.uint8)
        img = cv2.circle(img, (int(self.render_size/2),int(self.render_size/2)), 5, (255,255,255), -1)
        img = self._point_render(myPose, myAngle, targetPose, img, 1, 0, 0, 5)
        img = self._point_render(myPose, myAngle, nextTargetPose, img, 0, 1, 0, 5)
        environment = np.array([windSpeed, windDirection, waveLevel, waveDirection], dtype=np.float32)
        observation = [environment, img]
        return observation
    
    def _point_render(self, myPos, myAng, target_point, img, r,g,b,radius=1):
        #target_pointのmyPosからの相対位置を計算
        Point = [0.0]*2
        Point[0] = target_point[0]-myPos[0]
        Point[1] = target_point[1]-myPos[1]
        #target_pointのmyPosからの相対距離を計算
        PointDistance = np.linalg.norm(Point)*10
        #myAngからの相対角度を計算
        PointAngle = np.arctan2(Point[1],Point[0])-myAng
        #target_pointを表す円を描画
        if(r==1):
            cv2.circle(img, (int(self.render_size/2+PointDistance*np.cos(PointAngle)),int(self.render_size/2+PointDistance*np.sin(PointAngle))), radius, (0,0,255), -1)
        if(g==1):
            cv2.circle(img, (int(self.render_size/2+PointDistance*np.cos(PointAngle)),int(self.render_size/2+PointDistance*np.sin(PointAngle))), radius, (0,255,0), -1)
        if(b==1):
            cv2.circle(img, (int(self.render_size/2+PointDistance*np.cos(PointAngle)),int(self.render_size/2+PointDistance*np.sin(PointAngle))), radius, (255,0,0), -1)
        #画像を返す
        return img

    def reset(self):
        self.action_index = 0
        self.prePose = [0.0] * 2
        self.action = [[0.0]*14]*4
        self.action_start = False

    #action を最後に４回アペンドする
    def final_append(self, action_index,myVel,myAngle,myAngleVel,myPose,prePose):
        for i in range(4):
            self.makeActionData(((action_index+i)%4),myVel,myAngle,myAngleVel,myPose,prePose)
            self.action_data.append(self.action[(action_index+i+3)%4])
            print ("action: ", self.action_data)
        observation = self.makeObservationData(self.myPose,self.myAngle,self.targetPose,self.nextTargetPose,self.windSpeed,self.windDirection,self.waveLevel,self.waveDirection)
        self.observation_data.append(observation)
        print ("observation: ")
        self.info_data.append([1])

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
        act = np.array(self.action_data)
        obs = np.array(self.observation_data, dtype=object)
        info = np.array(self.info_data)
        observation = types.maybe_wrap_in_dictobs(obs)
        data = TransitionsMinimal(observation, act, info)
        path = 'rollout.pkl'
        with open(path, mode='wb') as f:
            pickle.dump(data, f)

def main(args=None):
    rclpy.init(args=args)
    makeExpertData_node = makeExpertData()
    rclpy.spin(makeExpertData_node)
    makeExpertData_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
