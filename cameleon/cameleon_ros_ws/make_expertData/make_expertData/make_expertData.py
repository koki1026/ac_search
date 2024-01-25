import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from imitation.data.types import MaybeWrapDict
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseArray


class make_expertData(Node):
    #ノード名を宣言
    def __init__(self):
        super().__init__('make_expertData')
        self.create_subscription(Twist, '/asv/cmd_vel', self.cmd_vel_callback, 10) #imuによる角度情報をsubscribe
        self.create_subscription(PoseArray, '/asv/waypoints', self.waypoints_callback, 10) #waypointをsubscribe
        #変数を宣言
        self.myVel = 0.0
        self.myAngle = 0.0
        self.myAmgVel = 0.0
        self.myPose = [0.0]*2
        self.prePose = []*2
        self.goalPose = [0.0]*2
        self.next_goalPose = [0.0]*2
        self.noxtPoses = [0.0]*4
        self.dis_Angs = [0.0]*4
        self.direction = [0.0]*5
        self.windSpeed = 0.0
        self.windDirection = 0.0
        self.waveLevel = 0.0
        self.waveDirection = 0.0
        self.obsImg = np.zeros((self.render_size,self.render_size,3),dtype=np.uint8)
        self.reward = 0.0
        self.done = False
        self.info = []
        self.render_size = 800
        self.bool_obs = True
        self.actions = np.array([[0.0]*14]*4)
        self.act_index = 0
        self.stated = False
        self.state_checker = [0]*2

        '''
        集めるデータは以下の通り
        ・asvの位置(x,y)
        ・asvの船体角度
        ・asvの速度(x,y)
        ・asvの角速度
        ・目標地点の位置(x,y)
        ・次の目標地点の位置(x,y)
        ・エピソードの終了判定
        ・波の大きさ
        ・波の向き
        ・風の大きさ
        ・風の向き

        集めたデータを、0.1秒ごとに
        [
            [obs[],action[],rewards,info],
            ...
            ...
        ]
        の形式で並べ、保存する
        同時に、expertDataメッセージとしてpublishする
        '''
        #データを集める配列を宣言
        self.act = []
        self.obs = []
        self.rews = []
        self.info = []
        self.next_obs = []
        self.done = []
        #タイマーコールバック関数を宣言
        self.timer = self.create_timer(1.0, self.timer_callback)

    #コールバック関数
    def cmd_vel_callback(self, msg):
        self.myVel = msg.linear.x
        self.myAngle = msg.angular.z
        self.myAmgVel = msg.angular.x

        #記録を開始していいかチェック
        if(self.state_checker[0]==0):
            self.state_checker[0] = 1
            if(self.state_checker[1]==1):
                self.stated = True
           

    def waypoints_callback(self, msg):
        self.prePose = self.myPose
        self.myPose = msg.poses[0].x, msg.poses[0].y
        self.goalPose = msg.poses[1].x, msg.poses[1].y
        self.next_goalPose = msg.poses[2].x, msg.poses[2].y

        #記録を開始していいかチェック
        if(self.state_checker[1]==0):
            self.state_checker[1] = 1
            if(self.state_checker[0]==1):
                self.stated = True
    
    def _point_render(self, myPos, myAng, target_point, img, r,g,b,radius=1.0):
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

    def timer_callback(self):
        if(self.stated):
            return
        #action, observation, reward, info, next_observation, done を作成
        if(self.prePose!=None):
            cullent_action = self.culculate_action(self.myPose, self.prePose)
            for i in range(4):
                self.actions[(self.act_index+i)%4][2+3*i] = cullent_action[0]
                self.actions[(self.act_index+i)%4][3+3*i] = cullent_action[1]
                self.actions[(self.act_index+i)%4][4+3*i] = self.myAngle
            self.actions[self.act_index][0] = self.myVel
            self.actions[self.act_index][1] = self.myAmgVel
            action = self.actions[(self.act_index+3)%4]
            self.act_index -= 1
            self.act_index %= 4
        else :
            action = [False]*2
        observation_1 = [
            self.windSpeed,
            self.windDirection,
            self.waveLevel,
            self.waveDirection,
        ]
        obsImg = np.zeros((self.render_size,self.render_size,3),dtype=np.uint8)
        #中心に自己位置を描画
        #自分の位置を表す円を中心に描画
        cv2.circle(obsImg, (int(self.render_size/2),int(self.render_size/2)), 5, (255,255,255), -1)
        obsImg = self._point_render(self.myPose, self.myAngle, self.goalPose, self.obsImg, 0,1,0)
        obsImg = self._point_render(self.myPose, self.myAngle, self.next_goalPose, self.obsImg, 0,1,0)
        observation_2 = [
            obsImg 
        ]
        observation = [observation_1, observation_2]
        reward = self.reward
        done = self.done
        info = self.info

        self.save_data(action, observation, observation, reward, info, done)

    def culculate_action(self, cullentPos, prePos):
        dis = [0.0]*2
        dis[0] = cullentPos[0]-prePos[0]
        dis[1] = cullentPos[1]-prePos[1]
        distanse = np.linalg.norm(dis)
        dis_Ang = np.arctan2(dis[0],dis[1])
        return distanse, dis_Ang


    def save_data(self, action, observation, next_observation, reward, info, done):
        if(self.bool_obs):
            #最初の一回目はnext_observationがないので、appnedしない
            self.bool_obs = False
            self.act.append(action)
            self.obs.append(observation)
            self.rews.append(reward)
            self.info.append(info)
            self.done.append(done)
        if(action[0] != None):
            self.act.append(action)
        self.obs.append(observation)
        self.obs.append(next_observation)
        self.rews.append(reward)
        self.info.append(info)
        self.done.append(done)
        