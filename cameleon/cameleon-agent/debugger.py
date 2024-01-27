import gymnasium as gym
import cameleon_gym_env
import time

env = gym.make('Cameleon-v0')

#環境を初期化
env.reset()

#アクションを指定回数実行
for _ in range(200):
    action = env.action_space.sample() #ランダムなアクションを取得
    observation, reward, done, info = env.step(action) #アクションを実行
    print("observation:", observation)
    if done:
        print("Episode finished after {} timesteps".format(_+1))
        env.reset() #環境を初期化
    #1秒待機
    time.sleep(3)