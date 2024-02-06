import cv2
from git import Optional
import gymnasium as gym
import numpy as np
import pygame

class CameleonEnvFinal(gym.Env):
    def __init__(self, render_mode='hum'):
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
        self.observation_space = gym.spaces.Box(low, high, dtype=np.float32)

        # Define the goal
        self.waypoint_num = 30
        self.waypoints = np.zeros((self.waypoint_num, 2), dtype=np.float32)
        for i in range(self.waypoint_num):
            self.waypoints[i][0] = 0
            self.waypoints[i][1] = i

        # Define the state
        self.myPos = [0.0, 0.0]
        self.myVel = 0.0
        self.myAngVel = 0.0
        self.myAngle = 0.0

        # make tools for updating the environment
        self.target_index = 0
        self.judge_distance = 3.0
        self.episode_length = 0

        # Define the rendering parameters
        self.render_size = 1000
        self.render_scale = 10
        self.render_mode = render_mode
        if(self.render_mode=='human'):
            pygame.init()
            self.screen = pygame.display.set_mode((self.render_size,self.render_size))
            #画像を見せるpygameにて実装
            self.render(self.render_mode)

    # Define the step function
    def step(self, action):
        # update the episode length
        self.episode_length += 1
        # update the state
        self.myVel, self.myAngVel,self.myAngle, self.myPos  =self.updateState(action, self.myPos, self.myAngle)
        # Calculate the goalPos
        goal_state = self.goalState()
        # make the observation
        obs = self.makeObservation(goal_state)
        # Calculate the reward
        reward = self.reward(goal_state)
        # Check if the episode is done
        done = self.isDone()
        # render the environment
        self.render(self.render_mode)
        return obs, reward, done, False,{}
    
    # Define updateState function
    def updateState(self, action, myPos, myAngle):
        # update the state
        myVel = action[0]
        myAngVel = action[1]
        myAngle = myAngle + myAngVel
        # make sure the angle is in the range of [-pi, pi]
        if myAngle > np.pi:
            myAngle -= 2*np.pi
        elif myAngle < -np.pi:
            myAngle += 2*np.pi
        # update the position
        # myAngle is yaw
        myPos[0] += myVel*np.sin(myAngle)
        myPos[1] += myVel*np.cos(myAngle)
        return myVel, myAngVel, myAngle, myPos
    
    # Define goalState function
    def goalState(self):
        # calculate the goal state
        goalPos = self.waypoints[self.target_index]
        distance = [goalPos[0] - self.myPos[0], goalPos[1] - self.myPos[1]]
        #culculate the angle to the goal (yaw)
        angle = np.arctan2(distance[0], distance[1]) - self.myAngle
        # make sure the angle is in the range of [-pi, pi]
        if angle > np.pi:
            angle -= 2*np.pi
        elif angle < -np.pi:
            angle += 2*np.pi
        return [np.linalg.norm(distance), angle]
    
    # Define makeObservation function
    def makeObservation(self, goal_state):
        # make the observation
        obs = np.zeros(2, dtype=np.float32)
        obs[0] = goal_state[0]
        obs[1] = goal_state[1]
        return obs
    
    # Define reward function
    def reward(self, goal_state):
        # calculate the reward
        if goal_state[0] < self.judge_distance:
            self.target_index += 1
            return 100.0
        else:
            return -goal_state[0]

    # Define isDone function
    def isDone(self):
        # check if the episode is done
        if self.episode_length > 30:
            return True
        else:
            return False
        
    # Define reset function
    def reset(    self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
        render_mode: str = 'hum',
        ):
        # reset the rendering mode
        self.render_mode = render_mode
        if(self.render_mode=='human'):
            pygame.init()
            self.screen = pygame.display.set_mode((self.render_size,self.render_size))
            #画像を見せるpygameにて実装
            pygame.display.set_caption("Cameleon")
            self.render(self.render_mode)
        # reset the environment
        self.myPos = [0.0, 0.0]
        self.myVel = 0.0
        self.myAngVel = 0.0
        self.myAngle = 0.0
        self.target_index = 0
        self.episode_length = 0

        #reset the goal
        for i in range(self.waypoint_num):
            self.waypoints[i][0] = 0
            self.waypoints[i][1] = i
        goal_state = self.goalState()
        return self.makeObservation(goal_state)
    
    # Define render function
    def render(self, mode):
        # render the environment
        img = np.zeros((self.render_size, self.render_size, 3), dtype=np.uint8)
        #senter position of the image is (0,0)
        center = [self.render_size/2, self.render_size/2]
        #draw the waypoints
        for i in range(self.waypoint_num):
            x = int(self.waypoints[i][0]*self.render_scale + center[0])
            y = int(self.waypoints[i][1]*self.render_scale + center[1])
            cv2.circle(img, (x, y), self.render_scale/2, (0, 0, 255), -1)
        #draw the goal
        goalPos = self.waypoints[self.target_index]
        x = int(goalPos[0]*self.render_scale + center[0])
        y = int(goalPos[1]*self.render_scale + center[1])
        cv2.circle(img, (x, y), self.render_scale/2, (0, 255, 0), -1)
        #draw the agent
        x = int(self.myPos[0]*self.render_scale + center[0])
        y = int(self.myPos[1]*self.render_scale + center[1])
        cv2.circle(img, (x, y), self.render_scale/2, (255, 0, 0), -1)

        #show the image by pygame
        if mode == 'human':
            pygame.display.set_caption("Cameleon")
            image_surface = pygame.surfarray.make_surface(img)
            self.screen.blit(image_surface, (0,0))
            pygame.display.flip()
