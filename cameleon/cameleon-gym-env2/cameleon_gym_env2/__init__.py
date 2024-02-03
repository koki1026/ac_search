from gymnasium.envs.registration import register

register(
    id='Cameleon2-v0',
    entry_point='cameleon_gym_env2.envs:CameleonEnv2',
)