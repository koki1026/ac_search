from gymnasium.envs.registration import register

register(
    id='CameleonBC-v0',
    entry_point='cameleon_gym_env_bc.envs:CameleonEnvBC',
)