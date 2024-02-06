import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import time
import pygame
import cv2
from typing import Optional, Tuple, Union

class CameleonEnv2(gym.Env):

    def __init__(self, render_mode='hum'):
        self.window_size = 1000 #人間に見せる画像のサイズ
        self.render_size = 600 #環境の画像のサイズ
        self.myPos = [0.0]*2 #自分の位置
        self.prePose = [0.0]*2 #一つ前の自分の位置
        self.myAngle = 0.0 #自分の角度
        self.max_vel = 3.0 #asvの最大速度
        self.max_distance = 50.0 
        self.max_Angvel = np.pi #asvの最大角速度
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
        self.max_episode_steps = 29
        self.episode_step = 0
        
        #通過地点の座標
        self.passing_point = np.zeros((self.passing_point_num, 2))
        #目指す通過地点のインデックス
        self.nextPointIndex = 0
        preAng = np.degrees(self.myAngle)
        #通過地点の生成
        for i in range(self.passing_point_num):
            #一つ前の通過地点からの距離を8~10の範囲でランダムに決定
            distance = np.random.rand()*2.0+8.0
            #一つ前の通過地点からの角度を-90~90の範囲でランダムに決定
            angle = preAng + np.random.rand()*180.0-90.0
            preAng = angle
            #ポイントの中身を更新(i=0の時は原点からの距離を代入)
            if(i==0):
                self.passing_point[i][0] = self.myPos[0] + distance*np.cos(self.myAngle)
                self.passing_point[i][1] = self.myPos[1] + distance*np.sin(self.myAngle)
                preAng = np.degrees(self.myAngle)
                preAng = 90.0 - preAng
            else:
                self.passing_point[i][0] = self.passing_point[i-1][0] + distance*np.sin(np.radians(angle))
                self.passing_point[i][1] = self.passing_point[i-1][1] + distance*np.cos(np.radians(angle))

        self.distance = [0.0]*2
        self.distance[0] = abs(self.myPos[0]-self.passing_point[self.nextPointIndex][0])
        self.distance[1] = abs(self.myPos[1]-self.passing_point[self.nextPointIndex][1])

        higher = np.array(
            [
                self.max_vel, #asvの最大速度
                self.max_Angvel, #方向

            ]
        )
        lower = np.array(
            [
                0.0, #asvの最大速度
                -self.max_Angvel, #方向
            ]
        )
        self.action_space = gym.spaces.Box(low= lower, high = higher, dtype=np.float32)

        higher_list = []
        higher_list.append(self.max_distance) #目的距離
        higher_list.append(np.pi) #目的方向
        higher_list.append(self.max_distance) #目的目的距離
        higher_list.append(np.pi) #目的目的方向
        higher_list.append(np.pi) #風向
        higher_list.append(np.finfo(np.float32).max) #風速
        higher_list.append(np.pi) #波向
        higher_list.append(np.finfo(np.float32).max) #波高
        higher_list_np = np.array(higher_list, np.float32) 

        low_list = []
        low_list.append(0.0) #目的距離
        low_list.append(-np.pi) #目的方向
        low_list.append(0.0) #目的目的距離
        low_list.append(-np.pi) #目的目的方向
        low_list.append(-np.pi) #風向
        low_list.append(0.0) #風速
        low_list.append(-np.pi) #波向
        low_list.append(0.0) #波高
        low_list_np = np.array(low_list, np.float32)

        self.observation_space = gym.spaces.Box(low=low_list_np, high=higher_list_np, dtype=np.float32)

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

        self.prePose = self.myPos.copy()
        #actionを実行をもとに現在地を更新
        self.myVel = action[0]
        self.myAngVel = action[1]
        self.myAngle += action[1]
        self.myPos[0] += action[0]*np.sin(self.myAngle)
        self.myPos[1] += action[0]*np.sin(self.myAngle)

        #報酬を計算
        reward = self._get_reward()

        #episodeの終了判定
        done = self._is_done()

        #状態を更新
        nextnextPointIndex = self.nextPointIndex+1
        #coment out
        #self.state = self._next_state(self.myPos, self.myAngle, self.passing_point[self.nextPointIndex], self.passing_point[nextnextPointIndex])

        self.state = self._next_state_vector(self.myPos, self.myAngle, self.passing_point[self.nextPointIndex], self.passing_point[nextnextPointIndex])



        #episodeの情報
        info = {}

        #人間に画像を見せる
        if(self.render_mode=='human'):
            img = np.zeros((self.window_size,self.window_size,3),dtype=np.uint8)
            img = self.render(img, self.myPos, self.prePose, self.passing_point)
            pygame.display.set_caption("Cameleon")
            image_surface = pygame.surfarray.make_surface(img)
            self.screen.blit(image_surface, (0,0))
            pygame.display.flip()


        return self.state, reward, done, False, info
    
    def render(self, img, myPos, prePose, wayPoints):
        img = np.zeros((self.window_size,self.window_size,3),dtype=np.uint8)
        #add way point
        for i in range(self.passing_point_num):
            point = wayPoints[i]
            point = [int(point[0]*10+500), int(point[1]*10+500)]
            cv2.circle(img, (point[0], point[1]), 5, (0,0,255), -1)
        #add my position
        cv2.circle(img, (int(myPos[0]*10+500), int(myPos[1]*10+500)), 5, (255,255,255), -1)
        #add my pre position
        cv2.circle(img, (int(prePose[0]*10+500), int(prePose[1]*10+500)), 5, (255,0,0), -1)

        return img

    def reset(
            self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
        render_mode: str = 'hum',
    ):
        self.render_mode = render_mode
        if(self.render_mode=='human'):
            pygame.init() #pygameの初期化
            self.screen = pygame.display.set_mode((self.window_size,self.window_size)) #pygameの画面を設定
        self.episode_step = 0
        self.myPos = [0.0]*2
        self.prePose = [0.0]*2
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
        preAng = np.degrees(self.myAngle)
        #通過地点の生成
        for i in range(self.passing_point_num):
            #一つ前の通過地点からの距離を8~10の範囲でランダムに決定
            distance = np.random.rand()*2.0+8.0
            #一つ前の通過地点からの角度を-90~90の範囲でランダムに決定
            angle = preAng + np.random.rand()*180.0-90.0
            preAng = angle
            #ポイントの中身を更新(i=0の時は船の現在地からの距離を代入)
            if(i==0):
                self.passing_point[i][0] = self.myPos[0] + distance*np.cos(self.myAngle)
                self.passing_point[i][1] = self.myPos[1] + distance*np.sin(self.myAngle)
                preAng = np.degrees(self.myAngle)
                #y方向角度からx方向角度に変更
                preAng = 90.0 - preAng
                
            else:
                self.passing_point[i][0] = self.passing_point[i-1][0] + distance*np.sin(np.radians(angle))
                self.passing_point[i][1] = self.passing_point[i-1][1] + distance*np.cos(np.radians(angle))
        self.distance = [0.0]*2
        self.distance[0] = abs(self.myPos[0]-self.passing_point[self.nextPointIndex][0])
        self.distance[1] = abs(self.myPos[1]-self.passing_point[self.nextPointIndex][1])

        '''
        self.state = self._next_state(self.myPos, self.myAngle, self.passing_point[self.nextPointIndex], self.passing_point[self.nextPointIndex+1])
        '''
        self.state = self._next_state_vector(self.myPos, self.myAngle, self.passing_point[self.nextPointIndex], self.passing_point[self.nextPointIndex+1])

        return self.state, {}
    
    def _next_state_vector(self, myPos, myAng, target_point, nextnextPoint_):
        #状態を生成
        #target_pointのmyPosからの相対位置を計算
        nextPoint = [0.0]*2
        nextPoint[0] = target_point[0]-myPos[0]
        nextPoint[1] = target_point[1]-myPos[1]
        #target_pointのmyPosからの相対距離を計算
        nextPointDistance = np.linalg.norm(nextPoint)
        #myAngからの相対角度を計算
        nextPointAngle = np.arctan2(nextPoint[1],nextPoint[0])-myAng

        nextnextPoint = [0.0]*2
        nextnextPoint[0] = nextnextPoint_[0]-myPos[0]
        nextnextPoint[1] = nextnextPoint_[1]-myPos[1]
        #target_pointのmyPosからの相対距離を計算
        nextnextPointDistance = np.linalg.norm(nextnextPoint)
        #myAngからの相対角度を計算
        nextnextPointAngle = np.arctan2(nextnextPoint[1],nextnextPoint[0])-myAng

        states = np.array([nextPointDistance, nextPointAngle, nextnextPointDistance, nextnextPointAngle, self.wind_direction, self.wind_speed, self.wave_direction, self.wave_level], dtype=np.float32)
        return states
    
    def _next_state(self, myPos, myAng, nextPoint_, nextnextPoint_):
        #画像を生成
        #img = self._render_mono(myPos, myAng, nextPoint_, nextnextPoint_)
        img = self._render(myPos, myAng, nextPoint_, nextnextPoint_,)

        #state1 = np.array([self.myVel, self.myAngVel, self.wind_direction, self.wind_speed, self.wave_direction, self.wave_level], dtype=np.float32)
        state1 = self._state1_mono(self.myVel, self.myAngVel, self.wind_direction, self.wind_speed, self.wave_direction, self.wave_level)
        state2 = img
        states = state2

        #状態を生成
        state = states

        return state
    
    def _state1_mono(self, myVel, myAngVel, wind_direction, wind_speed, wave_direction, wave_level):
        #状態を生成
        state = []
        for i in range(60):
            state.append(wind_direction)
        for i in range(60):
            state.append(wind_speed)
        for i in range(60):
            state.append(wave_direction)
        for i in range(60):
            state.append(wave_level)
        state = np.array(state, dtype=np.float32)
        return state
    
    def _render_mono(self, myPos, myAng, nextPoint_, nextnextPoint_):
        #画像を生成
        img = np.zeros((self.render_size,self.render_size),dtype=np.float32)
        #自分の位置を表す円を中心に描画
        cv2.circle(img, (int(self.render_size/2),int(self.render_size/2)), 1, 255, -1)
        for i in range(self.passing_point_num):
            img = self._point_render_mono(myPos, myAng, self.passing_point[i], img, 20, 1)
        img = self._point_render_mono(myPos, myAng, nextPoint_, img, 155, 1)
        img = self._point_render_mono(myPos, myAng, nextnextPoint_, img, 55, 1)
        #画像を返す
        return img
    
    def _render(self, myPos, myAng, nextPoint_, nextnextPoint_):
        #画像を生成
        img = np.zeros((self.render_size,self.render_size,3),dtype=np.uint8)
        #自分の位置を表す円を中心に描画
        cv2.circle(img, (int(self.render_size/2),int(self.render_size/2)), 5, (255,255,255), -1)

        for i in range(self.passing_point_num):
            img = self._point_render(myPos, myAng, self.passing_point[i], img, 0,1,1, 1)
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
        PointDistance = np.linalg.norm(Point)
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
        reward = 0.0
        radian = np.arctan2(distance[0]-self.myPos[0], distance[1]-self.myPos[1])
        if(abs(radian)<30):
            reward += 10.0
        else:
            reward -= 10.0
        '''
        distance_change_rate = np.linalg.norm(distance)-np.linalg.norm(self.distance)
        self.distance = distance
        if(distance_change_rate<-1.0):
            reward += 10.0
        else:
            reward -= distance_change_rate
        '''
        if(np.linalg.norm(distance)<3.0):
            #次の通過点のインデックスを更新
            self.nextPointIndex += 1
            reward += 100.0
        else:
            reward -= np.linalg.norm(distance)
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
