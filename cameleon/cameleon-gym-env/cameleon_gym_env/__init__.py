from gymnasium.envs.registration import register

register(
    id='Cameleon-v0',
    entry_point='cameleon_gym_env.envs:CameleonEnv',
)