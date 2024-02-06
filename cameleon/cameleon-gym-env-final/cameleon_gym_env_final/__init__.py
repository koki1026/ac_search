from gymnasium.envs.registration import register

register(
    id='CameleonFinal-v0',
    entry_point='cameleon_gym_env_final.envs:CameleonEnvFinal',
)