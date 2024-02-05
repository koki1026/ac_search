import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import time
import pygame
import cv2
from typing import Optional, Tuple, Union

class CameleonEnvBC(gym.Env):

    def __init__(self, render_mode='hum'):
        self.action_space = gym.spaces.Box(low=0.0, high=1000.0, shape=(2,), dtype=np.float32)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(100, 100, 1), dtype=np.float32)
        self._action = np.zeros(2)
        
        

    def step(self, action):
        self._take_action(action)
        obs = self._get_obs()
        reward = self._get_reward()
        done = self._is_done()
        info = {}
        return obs, reward, done, False, info

    def _take_action(self, action):
        action = np.clip(action, self.action_space.low, self.action_space.high)
        self._action = action

    def _get_obs(self):
        return np.zeros((100, 100, 1), dtype=np.float32)
    
    def _get_reward(self):
        return 0.0
    
    def _is_done(self):
        return False
    
    def reset(   
            self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        state = self._get_obs()
        return state, {}
    