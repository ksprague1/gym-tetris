from gym.envs.registration import register

#woot
register(
    id='Tetris-v0',
    entry_point='Games.Tetris:TetrisEnv',
    max_episode_steps = 1000,
)

