from gym.envs.registration import register

register(
    id='cameleon-v0',
    entry_point='cameleon_gym_env.envs:CameleonEnv',
)