import gym
import cameleon_gym_env
import time

print(gym.envs.registry.all())
env = gym.make('Cameleon-v0')

#環境を初期化
env.reset()

#アクションを指定回数実行
for _ in range(200):
    action = env.action_space.sample() #ランダムなアクションを取得
    observation, reward, done, info = env.step(action) #アクションを実行
    if done:
        print("Episode finished after {} timesteps".format(_+1))
        env.reset() #環境を初期化
        break
    #1秒待機
    time.sleep(1)