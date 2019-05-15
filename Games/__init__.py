from gym.envs.registration import register

#woot
register(
    id='Tetris-v0',
    entry_point='Games.Tetris.environment:TetrisEnv',
)

register(
    id='Tetris-v1',
    entry_point='Games.Tetrisv1.environment:TetrisEnv',
)
register(
    id='Dominos-v0',
    entry_point='Games.Dominos.environment:TetrisEnv',
)
register(
    id='Dominos-v1',
    entry_point='Games.Dominosv1.environment:TetrisEnv',
)

register(
    id='Triminos-v0',
    entry_point='Games.Triminos.environment:TetrisEnv',
)
