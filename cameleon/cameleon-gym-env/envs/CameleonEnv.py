import gym
import numpy as np
import matplotlib.pyplot as plt

class CameleonEnv(gym.Env):

    def __init__(self, render_mode='human'):
        self.window_size = 200.0
        self.render_size = 50.0
        self.myPos = [0.0]*2
        self.myVel = 0.0
        self.myAngle = 0.0
        self.render_mode = render_mode
        #風向と風速をランダムに決定
        self.wind_direction = np.random.rand()*2.0*np.pi-np.pi
        self.wind_speed = np.random.rand()*10.0
        #波向と波高をランダムに決定
        self.wave_direction = np.random.rand()*2.0*np.pi-np.pi
        #波のレベルは1.0,2.0,3.0のいずれか
        self.wave_level = float(np.random.randint(1,4))
        #通過地点の数
        self.passing_point_num = 40
        #通過地点の座標
        self.passing_point = [[0.0]*2]*self.passing_point_num
        #通過地点の生成
        for i in range(self.passing_point_num):
            #一つ前の通過地点からの距離を8~10の範囲でランダムに決定
            distance = np.random.rand()*2.0+8.0
            #一つ前の通過地点からの角度を-90~90の範囲でランダムに決定
            angle = np.random.rand()*180.0-90.0
            #ポイントの中身を更新(i=0の時は原点からの距離を代入)
            if(i==0):
                self.passing_point[i][0] = distance*np.cos(angle)
                self.passing_point[i][1] = distance*np.sin(angle)
            else:
                self.passing_point[i][0] = self.passing_point[i-1][0] + distance*np.cos(angle)
                self.passing_point[i][1] = self.passing_point[i-1][1] + distance*np.sin(angle)

        high = np.array(
            [
                self.window_size, #横方向位置
                self.window_size, #縦方向位置
                np.finfo(np.float32).max, #前進速度
                np.finfo(np.float32).max, #角速度
                self.window_size, #横方向位置
                self.window_size, #縦方向位置
                np.finfo(np.float32).max, #前進速度
                np.finfo(np.float32).max, #角速度
                self.window_size, #横方向位置
                self.window_size, #縦方向位置
                np.finfo(np.float32).max, #前進速度
                np.finfo(np.float32).max, #角速度
                self.window_size, #横方向位置
                self.window_size, #縦方向位置
                np.finfo(np.float32).max, #前進速度
                np.finfo(np.float32).max, #角速度
                self.window_size, #横方向位置
                self.window_size, #縦方向位置
                np.finfo(np.float32).max, #前進速度
                np.finfo(np.float32).max, #角速度
            ],
            dtype=np.float32,
        )
        low = np.array(
            [
                0.0, #横方向位置
                0.0, #縦方向位置
                0.0, #前進速度
                -np.finfo(np.float32).max, #角速度
                0.0, #横方向位置
                0.0, #縦方向位置
                0.0, #前進速度
                -np.finfo(np.float32).max, #角速度
                0.0, #横方向位置
                0.0, #縦方向位置
                0.0, #前進速度
                -np.finfo(np.float32).max, #角速度
                0.0, #横方向位置
                0.0, #縦方向位置
                0.0, #前進速度
                -np.finfo(np.float32).max, #角速度
                0.0, #横方向位置
                0.0, #縦方向位置
                0.0, #前進速度
                -np.finfo(np.float32).max, #角速度
            ],
            dtype=np.float32,
        )
        self.action_space = gym.spaces.Box(low, high, dtype=np.float32)

        high = [
            np.finfo(np.float32).max, #現在速度
            np.finfo(np.float32).max, #現在角速度
            1.0, #風向
            np.finfo(np.float32).max, #風速
            1.0, #波向
            np.finfo(np.float32).max, #波高
        ]
        low = [
            0.0, #現在速度
            -np.finfo(np.float32).max, #現在角速度
            -1.0, #風向
            0.0, #風速
            -1.0, #波向
            0.0, #波高
        ]

        self.observation_space = gym.spaces.Tuple(gym.spaces.Box(low, high, dtype=np.float32),gym.spaces.Box(low=0, high=255, shape=(self.render_size,self.render_size,3), dtype=np.float32))

    def step(self, action):
        #エラー処理
        err_msg = f"{action!r} ({type(action)}) invalid"
        assert self.action_space.contains(action), err_msg

        #現在の状態を保存
        myVel = self.myVel
        myAngle = self.myAngle

        #行動を実行
        self.myPos[0] = action[0]
        self.myVel[1] = action[1]
        self.myVel = action[2]
        self.myAngle = action[3]

        #状態を更新
        self.state = self._next_state(self, self.myPos)

        #報酬を計算
        reward = self._get_reward()

        #episodeの終了判定
        done = self._is_done()

        #episodeの情報
        info = {}

        #人間に画像を見せる
        if(self.render_mode=='human'):
            self.render()

        return self.state, reward, done, info
    
    def render(self):
        #人間に見せる画像を生成
        img = self._render(self, self.myPos)
        #画像を見せる
        plt.imshow(img)

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
        for i in range(self.passing_point_num):
            #一つ前の通過地点からの距離を8~10の範囲でランダムに決定
            distance = np.random.rand()*2.0+8.0
            #一つ前の通過地点からの角度を-90~90の範囲でランダムに決定
            angle = np.random.rand()*180.0-90.0
            #ポイントの中身を更新(i=0の時は原点からの距離を代入)
            if(i==0):
                self.passing_point[i][0] = distance*np.cos(angle)
                self.passing_point[i][1] = distance*np.sin(angle)
            else:
                self.passing_point[i][0] = self.passing_point[i-1][0] + distance*np.cos(angle)
                self.passing_point[i][1] = self.passing_point[i-1][1] + distance*np.sin(angle)



        self.state = self._next_state(self, self.myPos)

        return self.state
    
    def _next_state(self, myPos):
        #画像を生成
        img = self._render(self, myPos)

        #状態を生成
        state = (self.myVel, self.myAngle, self.wind_direction, self.wind_speed, self.wave_direction, self.wave_level), img

        return state
    
    def _render(self, myPos, myAng, nextPointIndex):
        #画像を生成
        img = np.zeros((self.render_size,self.render_size,3),dtype=np.float32)
        #自分の位置を表す円を中心に描画
        img[int(self.render_size/2),int(self.render_size/2),0] = 255.0
        #次の通過地点のmyPosからの相対位置を計算
        nextPoint = self.passing_point[nextPointIndex]-myPos
        nextnextPoint = self.passing_point[nextPointIndex+1]-myPos
        #次の通過地点のmyPosからの相対距離を計算
        nextPointDistance = np.linalg.norm(nextPoint)
        nextnextPointDistance = np.linalg.norm(nextnextPoint)
        #myAngからの相対角度を計算
        nextPointAngle = np.arctan2(nextPoint[1],nextPoint[0])-myAng
        nextnextPointAngle = np.arctan2(nextnextPoint[1],nextnextPoint[0])-myAng
        #次の通過地点を表す円を描画
        img[int(self.render_size/2+nextPointDistance*np.cos(nextPointAngle)),int(self.render_size/2+nextPointDistance*np.sin(nextPointAngle)),1] = 255.0
        #次の次の通過地点を表す円を描画
        img[int(self.render_size/2+nextnextPointDistance*np.cos(nextnextPointAngle)),int(self.render_size/2+nextnextPointDistance*np.sin(nextnextPointAngle)),2] = 255.0

        #画像を返す
        return img
    
    def _get_reward(self):
        #自分の位置が次の通過点の半径1.0以内なら報酬を与える
        if(np.linalg.norm(self.myPos-self.passing_point[self.nextPointIndex])<1.0):
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
        if(np.linalg.norm(self.myPos-self.passing_point[self.nextPointIndex])>20.0):
            done = True

        return done

