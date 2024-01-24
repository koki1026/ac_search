import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from imitation.data.types import MaybeWrapDict

class make_expertData(Node):
    #ノード名を宣言
    def __init__(self):
        super().__init__('make_expertData')
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        #変数を宣言
        self.myVel = 0.0
        self.myAngle = 0.0
        self.distance = [0.0]*5
        self.dis_Ang = [0.0]*5
        self.direction = [0.0]*5
        self.windSpeed = 0.0
        self.windDirection = 0.0
        self.waveLevel = 0.0
        self.waveDirection = 0.0
        self.obsImg = np.zeros((self.render_size,self.render_size,3),dtype=np.uint8)
        self.reward = 0.0
        self.done = False
        self.info = []

        #データを集めるための変数を宣言
        self.current_pose

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
    def listener_callback(self, msg):
        self.vel = msg
        self.count += 1
        if(self.count==10):
            self.count = 0
            #データを集める
            #データを保存する
            #データをpublishする
            self.get_logger().info('I heard: "%s"' % self.vel.linear.x)

    def timer_callback(self):
        #action, observation, reward, info, next_observation, done を作成
        action = [
            self.myVel, 
            self.myAngle, 
            self.distance[0], 
            self.dis_Ang[0], 
            self.direction[0], 
            self.distance[1], 
            self.dis_Ang[1], 
            self.direction[1], 
            self.distance[2], 
            self.dis_Ang[2], 
            self.direction[2],
            self.distance[3],
            self.dis_Ang[3],
            self.direction[3],
            self.distance[4],
            self.dis_Ang[4],
            self.direction[4],
        ]
        observation_1 = [
            self.windSpeed,
            self.windDirection,
            self.waveLevel,
            self.waveDirection,
        ]
        observation_2 = [
            self.obsImg,
        ]
        observation = [observation_1, observation_2]
        reward = self.reward
        done = self.done
        info = self.info

        self.seve_data(action, observation, reward, info, done)

    def save_data(self, action, observation, reward, info, done):
        self.act.append(action)
        self.obs.append(observation)
        self.rews.append(reward)
        self.info.append(info)
        self.done.append(done)
        