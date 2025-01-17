import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import time
import pygame
import cv2
from typing import Optional, Tuple, Union

class CameleonEnv(gym.Env):

    def __init__(self, render_mode='hum'):
        self.window_size = 600 #人間に見せる画像のサイズ
        self.render_size = 600 #環境の画像のサイズ
        self.myPos = [0.0]*2 #自分の位置
        self.myAngle = 0.0 #自分の角度
        self.max_vel = 10.0 #asvの最大速度
        self.max_Angvel = np.pi/4.0 #asvの最大角速度
        self.render_mode = render_mode #人間に見せる画像のモード
        self.myVel = 0.0 #asvの速度
        self.myAngVel = 0.0 #asvの角速度
        if(self.render_mode=='human'):
            pygame.init() #pygameの初期化
            self.screen = pygame.display.set_mode((self.window_size,self.window_size)) #pygameの画面を設定
        #風向と風速をランダムに決定
        self.wind_direction = np.random.rand()*2.0*np.pi-np.pi
        self.wind_speed = np.random.rand()*10.0
        #波向と波高をランダムに決定
        self.wave_direction = np.random.rand()*2.0*np.pi-np.pi
        #波のレベルは1.0,2.0,3.0のいずれか
        self.wave_level = float(np.random.randint(1,4))
        #通過地点の数
        self.passing_point_num = 50 #用意する通過地点の数
        self.episode_point_num = self.passing_point_num-10 #エピソードの通過地点の数

        # エピソードの長さを60で切る
        self.max_episode_steps = 60
        self.episode_step = 0
        
        #通過地点の座標
        self.passing_point = np.zeros((self.passing_point_num, 2))
        #目指す通過地点のインデックス
        self.nextPointIndex = 0
        #通過地点の生成
        for i in range(self.passing_point_num):
            #一つ前の通過地点からの距離を8~10の範囲でランダムに決定
            distance = np.random.rand()*2.0+8.0
            #一つ前の通過地点からの角度を-90~90の範囲でランダムに決定
            angle = np.random.rand()*180.0-90.0
            #ポイントの中身を更新(i=0の時は原点からの距離を代入)
            if(i==0):
                self.passing_point[i][0] = abs(self.myPos[0] + distance*np.cos(angle))
                self.passing_point[i][1] = abs(self.myPos[1] + distance*np.sin(angle))
            else:
                self.passing_point[i][0] = abs(self.passing_point[i-1][0] + distance*np.cos(angle))
                self.passing_point[i][1] = abs(self.passing_point[i-1][1] + distance*np.sin(angle))
                                                                                        
        higher = np.array(
            [
                self.max_vel, #asvの次の瞬間の最大速度
                self.max_Angvel, #asvの次の瞬間の最大角速度
                self.max_vel, #asvの最大速度
                np.pi, #方向
                np.pi,  #角度
                self.max_vel, #asvの最大速度
                np.pi, #方向
                np.pi,  #角度
                self.max_vel, #asvの最大速度
                np.pi, #方向
                np.pi,  #角度
                self.max_vel, #asvの最大速度
                np.pi, #方向
                np.pi,  #角度
            ]
        )
        lower = np.array(
            [
                0.0, #asvの次の瞬間の最低速度
                -self.max_Angvel, #asvの次の瞬間の最低角速度
                0.0, #asvの最大速度
                -np.pi, #方向
                -np.pi,  #角度
                0.0, #asvの最大速度
                -np.pi, #方向
                -np.pi,  #角度
                0.0, #asvの最大速度
                -np.pi, #方向
                -np.pi,  #角度
                0.0, #asvの最大速度
                -np.pi, #方向
                -np.pi,  #角度
            ]
        )
        self.action_space = gym.spaces.Box(low= lower, high = higher, dtype=np.float32)

        higher_list = []
        for i in range(40):
            higher_list.append(self.max_vel)
        for i in range(40):
            higher_list.append(self.max_Angvel)
        for i in range(40):
            higher_list.append(np.pi)
        for i in range(40):
            higher_list.append(np.finfo(np.float32).max)
        for i in range(40):
            higher_list.append(np.pi)
        for i in range(40):
            higher_list.append(np.finfo(np.float32).max)
        higher_list_np = np.array(higher_list, np.float32)

        low_list = []
        for i in range(40):
            low_list.append(0.0)
        for i in range(40):
            low_list.append(-self.max_Angvel)
        for i in range(40):
            low_list.append(-np.pi)
        for i in range(40):
            low_list.append(0.0)
        for i in range(40):
            low_list.append(-np.pi)
        for i in range(40):
            low_list.append(0.0)
        low_list_np = np.array(low_list, np.float32)

        zero_image = np.zeros((self.render_size, self.render_size), np.float32)
        zero_image240 = cv2.resize(zero_image, (240, 240))
        high_image = np.full((self.render_size, self.render_size), 255.0, np.float32)
        high_image240 = cv2.resize(high_image, (240, 240))

        observation_high_list_np = np.vstack([high_image240, higher_list_np])
        observation_low_list_np = np.vstack([zero_image240, low_list_np])

        

        self.observation_space = gym.spaces.Box(low=observation_low_list_np, high=observation_high_list_np, dtype=np.float32)

        '''
        higher = np.array([
            self.max_vel, #速度
            self.max_Angvel, #角速度
            np.pi, #風向
            np.finfo(np.float32).max, #風速
            np.pi, #波向
            np.finfo(np.float32).max, #波高
            ]
            ,np.float32
        )
        lower = np.array([
            0.0, #速度
            -self.max_Angvel, #角速度
            -np.pi, #風向
            0.0, #風速
            -np.pi, #波向
            0.0, #波高
            ]
            ,np.float32
        )
        box_space1 = gym.spaces.Box(low = lower, high=higher, dtype=np.float32)
        box_space2 = gym.spaces.Box(low=0, high=255, shape=(self.render_size, self.render_size, 3), dtype=np.uint8)
        spase = ()

        self.observation_space = gym.spaces.Tuple(
            (box_space1, box_space2)
        )
        '''
        

    def step(self, action):
        self.episode_step += 1
        #エラー処理
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg

        #actionを実行をもとに現在の速度を更新
        self.myVel = action[0]
        #actionを実行をもとに現在の角速度を更新
        self.myAngVel = action[1]
        #actionを実行をもとに現在地を更新
        self.myPos[0] += action[2]*np.cos(action[3])
        self.myPos[1] += action[2]*np.sin(action[3])
        #actionを実行をもとに現在の角度を更新
        self.myAngle = action[4]

        #報酬を計算
        reward = self._get_reward()

        #episodeの終了判定
        done = self._is_done()

        #状態を更新
        nextnextPointIndex = self.nextPointIndex+1
        self.state = self._next_state(self.myPos, self.myAngle, self.passing_point[self.nextPointIndex], self.passing_point[nextnextPointIndex])



        #episodeの情報
        info = {}

        #人間に画像を見せる
        if(self.render_mode=='human'):
            self.render(self.state[1],action)

        return self.state, reward, done, False, info
    
    def render(self, img, action):
        #imgにactionの5~16を描画(白)
        waypoint = np.zeros((4, 3)) #ポイントが4つ、x座標、y座標、向き
        waypoint[0][0] = self.myPos[0] + action[5]*np.cos(action[6])
        waypoint[0][1] = self.myPos[1] + action[5]*np.sin(action[6])
        waypoint[0][2] = action[7]
        waypoint[1][0] = waypoint[0][0] + action[8]*np.cos(action[9])
        waypoint[1][1] = waypoint[0][1] + action[8]*np.sin(action[9])
        waypoint[1][2] = action[10]
        waypoint[2][0] = waypoint[1][0] + action[11]*np.cos(action[12])
        waypoint[2][1] = waypoint[1][1] + action[11]*np.sin(action[12])
        waypoint[2][2] = action[13]
        waypoint[3][0] = waypoint[2][0] + action[14]*np.cos(action[15])
        waypoint[3][1] = waypoint[2][1] + action[14]*np.sin(action[15])
        waypoint[3][2] = action[16]

        for i in range(4):
            img = self._point_render(self.myPos, self.myAngle, waypoint[i], img,0,1,1,4-i)

        #画像を見せるpygameにて実装
        pygame.display.set_caption("Cameleon")
        image_surface = pygame.surfarray.make_surface(img)
        self.screen.blit(image_surface, (0,0))
        pygame.display.flip()

    def reset(
            self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        self.episode_step = 0
        self.myPos = [0.0]*2
        self.myVel = 0.0
        self.myAngle = 0.0
        #風向と風速をランダムに決定
        self.wind_direction = np.random.rand()*2.0*np.pi-np.pi
        self.wind_speed = np.random.rand()*10.0
        #波向と波高をランダムに決定
        self.wave_direction = np.random.rand()*2.0*np.pi-np.pi
        #波のレベルは1.0,2.0,3.0のいずれか
        self.wave_level = float(np.random.randint(1,4))
        self.nextPointIndex = 0
        #通過地点の生成
        for i in range(self.passing_point_num):
            #一つ前の通過地点からの距離を8~10の範囲でランダムに決定
            distance = np.random.rand()*2.0+8.0
            #一つ前の通過地点からの角度を-90~90の範囲でランダムに決定
            angle = np.random.rand()*180.0-90.0
            #ポイントの中身を更新(i=0の時は原点からの距離を代入)
            if(i==0):
                self.passing_point[i][0] = self.myPos[0] + distance*np.sin(np.radians(angle))
                self.passing_point[i][1] = self.myPos[1] + distance*np.cos(np.radians(angle))

            else:
                self.passing_point[i][0] = abs(self.passing_point[i-1][0] + distance*np.cos(angle))
                self.passing_point[i][1] = abs(self.passing_point[i-1][1] + distance*np.sin(angle))

        self.state = self._next_state(self.myPos, self.myAngle, self.passing_point[self.nextPointIndex], self.passing_point[self.nextPointIndex+1])

        return self.state, {}
    
    def _next_state(self, myPos, myAng, nextPoint_, nextnextPoint_):
        #画像を生成
        img = self._render_mono(myPos, myAng, nextPoint_, nextnextPoint_)
        #img = self._render(myPos, myAng, nextPoint_, nextnextPoint_,)
        img240 = cv2.resize(img, (240,240))

        #state1 = np.array([self.myVel, self.myAngVel, self.wind_direction, self.wind_speed, self.wave_direction, self.wave_level], dtype=np.float32)
        state1 = self._state1_mono(self.myVel, self.myAngVel, self.wind_direction, self.wind_speed, self.wave_direction, self.wave_level)
        state2 = img240
        states = np.vstack([state2, state1])

        #状態を生成
        state = states

        return state
    
    def _state1_mono(self, myVel, myAngVel, wind_direction, wind_speed, wave_direction, wave_level):
        #状態を生成
        state = []
        for i in range(40):
            state.append(myVel)
        for i in range(40):   
            state.append(myAngVel) 
        for i in range(40):
            state.append(wind_direction)
        for i in range(40):
            state.append(wind_speed)
        for i in range(40):
            state.append(wave_direction)
        for i in range(40):
            state.append(wave_level)
        state = np.array(state, dtype=np.float32)
        return state
    
    def _render_mono(self, myPos, myAng, nextPoint_, nextnextPoint_):
        #画像を生成
        img = np.zeros((self.render_size,self.render_size),dtype=np.float32)
        #自分の位置を表す円を中心に描画
        cv2.circle(img, (int(self.render_size/2),int(self.render_size/2)), 5, 255, -1)
        img = self._point_render_mono(myPos, myAng, nextPoint_, img, 155, 5)
        img = self._point_render_mono(myPos, myAng, nextnextPoint_, img, 55, 5)
        #画像を返す
        return img
    
    def _render(self, myPos, myAng, nextPoint_, nextnextPoint_):
        #画像を生成
        img = np.zeros((self.render_size,self.render_size,3),dtype=np.uint8)
        #自分の位置を表す円を中心に描画
        cv2.circle(img, (int(self.render_size/2),int(self.render_size/2)), 5, (255,255,255), -1)
        img = self._point_render(myPos, myAng, nextPoint_, img, 1,0,0, 5)
        img = self._point_render(myPos, myAng, nextnextPoint_, img, 0,1,0, 5)
        #画像を返す
        return img
    
    def _point_render_mono(self, myPos, myAng, target_point, img, gray, radius=1):
        #target_pointのmyPosからの相対位置を計算
        Point = [0.0]*2
        Point[0] = target_point[0]-myPos[0]
        Point[1] = target_point[1]-myPos[1]
        #target_pointのmyPosからの相対距離を計算
        PointDistance = np.linalg.norm(Point)*10
        #myAngからの相対角度を計算
        PointAngle = np.arctan2(Point[1],Point[0])-myAng
        #target_pointを表す円を描画
        cv2.circle(img, (int(self.render_size/2+PointDistance*np.cos(PointAngle)),int(self.render_size/2+PointDistance*np.sin(PointAngle))), radius, gray, -1)
        #画像を返す
        return img
    
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
    
    def _get_reward(self):
        #自分の位置が次の通過点の半径1.0以内なら報酬を与える
        distance = [0.0]*2
        distance[0] = self.myPos[0]-self.passing_point[self.nextPointIndex][0]
        distance[1] = self.myPos[1]-self.passing_point[self.nextPointIndex][1]
        if(np.linalg.norm(distance)<3.0):
            #次の通過点のインデックスを更新
            self.nextPointIndex += 1
            reward = 1.0
        else:
            reward = 0.0
        return reward
    
    def _is_done(self):
        '''
        #次の通過点のインデックスが通過点の数-3を超えたら終了
        if(self.nextPointIndex>self.episode_point_num):
            done = True
        else:
            done = False
        '''
        done = False
        #現在地が次の通過点の半径20.0以上なら終了
        distance = [0.0]*2
        distance[0] = self.myPos[0]-self.passing_point[self.nextPointIndex][0]
        distance[1] = self.myPos[1]-self.passing_point[self.nextPointIndex][1]
        '''
        if(np.linalg.norm(distance)>20.0):
            done = True
        '''
        
        #エピソードの長さが60を超えたら終了
        if(self.episode_step>=self.max_episode_steps):
            done = True

        return done

'''
env = CameleonEnv()

env.reset()

for _ in range(200):
    action = env.action_space.sample() #ランダムなアクションを取得
    observation, reward, done, info = env.step(action) #アクションを実行
    if done:
        print("Episode finished after {} timesteps".format(_+1))
        env.reset() #環境を初期化
    #1秒待機
    time.sleep(1)
'''
