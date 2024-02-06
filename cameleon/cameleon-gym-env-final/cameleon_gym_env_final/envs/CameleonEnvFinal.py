import gymnasium as gym
import numpy as np

class CameleonEnvFinal(gym.Env):
    def __init__(self):
        # Initialize the environment

        #difine actionspace and observation space
        self.max_vel = 3.0
        self.max_angVel = np.pi/4.0
        low = np.zeros(2, dtype=np.float32)
        low[0] = 0.0 #linear velocity
        low[1] = -self.max_angVel #angular velocity
        high = np.zeros(2, dtype=np.float32)
        high[0] = self.max_vel
        high[1] = self.max_angVel
        self.action_space = gym.spaces.Box(low, high, dtype=np.float32)

        low = np.zeros(2, dtype=np.float32)
        low[0] = 0.0 #distance to goal
        low[1] = -np.pi #angle to goal
        high = np.zeros(2, dtype=np.float32)
        high[0] = np.inf
        high[1] = np.pi