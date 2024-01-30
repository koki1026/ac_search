# GAILを用いて、cameleon-gymの環境で学習する

import gymnasium as gym
import cameleon_gym_env
import time
import numpy as np
from imitation.policies.serialize import load_policy
from imitation.util.util import make_vec_env
from imitation.data.wrappers import RolloutInfoWrapper
from imitation.data import rollout
from imitation.algorithms.adversarial.gail import GAIL
from imitation.rewards.reward_nets import BasicRewardNet
from imitation.util.networks import RunningNorm
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.evaluation import evaluate_policy
import pickle
import cv2


SEED = 42

env = make_vec_env(
    "Cameleon-v0",
    rng=np.random.default_rng(SEED),
    n_envs=8,
    post_wrappers=[
        lambda env, _: RolloutInfoWrapper(env)
    ],  # needed for computing rollouts later
)
env_file_path = env.__module__
print(env_file_path)

path_file = "/media/gaia-22/ESD-ISO/auto_cosmos/cameleon/data/pkl/rollout02.pkl"
rollouts = pickle.load(open(path_file, 'rb'))

print("type: "+ str(type(rollouts)))
 
learner = PPO(
    env=env,
    policy=MlpPolicy,
    batch_size=64,
    ent_coef=0.0,
    learning_rate=0.0004,
    gamma=0.95,
    n_epochs=5,
    seed=SEED,
)
reward_net = BasicRewardNet(
    observation_space=env.observation_space,
    action_space=env.action_space,
    normalize_input_layer=RunningNorm,
)
gail_trainer = GAIL(
    demonstrations=rollouts,
    demo_batch_size=64,
    gen_replay_buffer_capacity=512,
    n_disc_updates_per_round=8,
    venv=env,
    gen_algo=learner,
    reward_net=reward_net,
)

learner_rewards_before_training, _ = evaluate_policy(
    learner, env, 100, return_episode_rewards=True
)
gail_trainer.train(200_000)

learner_rewards_after_training, _ = evaluate_policy(
    learner, env, 100, return_episode_rewards=True
)

print(
    "Rewards before training:",
    np.mean(learner_rewards_before_training),
    "+/-",
    np.std(learner_rewards_before_training),
)
print(
    "Rewards after training:",
    np.mean(learner_rewards_after_training),
    "+/-",
    np.std(learner_rewards_after_training),
)
