from gymnasium.envs.registration import register

register(
    id='CameleonPath-v0',
    entry_point='cameleon_gym_env_path.envs:CameleonEnvPath',
)