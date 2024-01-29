import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import time
import pygame
import cv2

class CameleonEnv(gym.Env):

    def __init__(self, render_mode='human'):
        self.window_size = 800 #人間に見せる画像のサイズ
        self.render_size = 800 #環境の画像のサイズ
        self.myPos = [0.0]*2 #自分の位置
        self.myAngle = 0.0 #自分の角度
        self.max_vel = 10.0 #asvの最大速度
        self.max_Angvel = np.pi/4.0 #asvの最大角速度
        self.render_mode = render_mode #人間に見せる画像のモード
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
                self.passing_point[i][0] = abs(distance*np.cos(angle))
                self.passing_point[i][1] = abs(distance*np.sin(angle))
                #通過地点をデバッグ
                print("passing_point: "+str(self.passing_point[i][0])+","+str(self.passing_point[i][1]))
            else:
                self.passing_point[i][0] = abs(self.passing_point[i-1][0] + distance*np.cos(angle))
                self.passing_point[i][1] = abs(self.passing_point[i-1][1] + distance*np.sin(angle))
                #通過地点をデバッグ
                print("passing_point: "+str(self.passing_point[i][0])+","+str(self.passing_point[i][1]))
                                                                                        
        high = np.array(
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
                self.max_vel, #asvの最大速度
                np.pi, #方向
                np.pi,  #角度
            ],
            dtype=np.float32,
        )
        low = np.array(
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
                0.0, #asvの最大速度
                -np.pi, #方向
                -np.pi,  #角度
            ],
            dtype=np.float32,
        )
        self.action_space = gym.spaces.Box(low, high, dtype=np.float32)

        high = np.array([
            self.max_vel, #速度
            self.max_Angvel, #角速度
            1.0, #風向
            np.finfo(np.float32).max, #風速
            1.0, #波向
            np.finfo(np.float32).max, #波高
        ])
        low = np.array([
            0.0, #速度
            -self.max_Angvel, #角速度
            -1.0, #風向
            0.0, #風速
            -1.0, #波向
            0.0, #波高
        ])

        box_space1 = gym.spaces.Box(low, high, dtype=np.float32)
        box_space2 = gym.spaces.Box(low=0, high=255, shape=(self.render_size, self.render_size, 3), dtype=np.uint8)

        self.observation_space = gym.spaces.Tuple(
            (box_space1, box_space2)
        )

    def step(self, action):
        #エラー処理
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg

        #actionを実行をもとに現在の速度を更新
        self.myVel = action[0]
        #actionを実行をもとに現在の角速度を更新
        self.myAng = action[1]
        #actionを実行をもとに現在地を更新
        self.myPos[0] += action[2]*np.cos(action[3])
        self.myPos[1] += action[2]*np.sin(action[3])
        #actionを実行をもとに現在の角度を更新
        self.myAngle += action[4]


        #状態を更新
        nextnextPointIndex = self.nextPointIndex+1
        self.state = self._next_state(self.myPos, self.myAngle, self.passing_point[self.nextPointIndex], self.passing_point[nextnextPointIndex])

        #報酬を計算
        reward = self._get_reward()

        #episodeの終了判定
        done = self._is_done()

        #episodeの情報
        info = {}

        #人間に画像を見せる
        if(self.render_mode=='human'):
            self.render(self.state[1],action)

        return self.state, reward, done, info
    
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

    def reset(self):
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
                self.passing_point[i][0] = abs(distance*np.cos(angle))
                self.passing_point[i][1] = abs(distance*np.sin(angle))

            else:
                self.passing_point[i][0] = abs(self.passing_point[i-1][0] + distance*np.cos(angle))
                self.passing_point[i][1] = abs(self.passing_point[i-1][1] + distance*np.sin(angle))

        self.state = self._next_state(self.myPos, self.myAngle, self.passing_point[self.nextPointIndex], self.passing_point[self.nextPointIndex+1])

    
    def _next_state(self, myPos, myAng, nextPoint_, nextnextPoint_):
        #画像を生成
        img = self._render(myPos, myAng, nextPoint_, nextnextPoint_,)

        #状態を生成
        state = (self.myVel, self.myAngle, self.wind_direction, self.wind_speed, self.wave_direction, self.wave_level), img

        return state
    
    def _render(self, myPos, myAng, nextPoint_, nextnextPoint_):
        #画像を生成
        img = np.zeros((self.render_size,self.render_size,3),dtype=np.uint8)
        #自分の位置を表す円を中心に描画
        cv2.circle(img, (int(self.render_size/2),int(self.render_size/2)), 5, (255,255,255), -1)
        img = self._point_render(myPos, myAng, nextPoint_, img, 0,1,0, 5)
        img = self._point_render(myPos, myAng, nextnextPoint_, img, 0,1,0, 5)
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
        if(np.linalg.norm(distance)<1.0):
            #次の通過点のインデックスを更新
            self.nextPointIndex += 1
            reward = 1.0
        else:
            reward = 0.0
        return reward
    
    def _is_done(self):
        #次の通過点のインデックスが通過点の数-3を超えたら終了
        if(self.nextPointIndex>self.passing_point_num-3):
            done = True
        else:
            done = False

        #現在地が次の通過点の半径20.0以上なら終了
        distance = [0.0]*2
        distance[0] = self.myPos[0]-self.passing_point[self.nextPointIndex][0]
        distance[1] = self.myPos[1]-self.passing_point[self.nextPointIndex][1]
        if(np.linalg.norm(distance)>20.0):
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
