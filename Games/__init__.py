from gym.envs.registration import register

#woot
register(
    id='Tetris-v0',
    entry_point='Games.Polymino.environment:Tetris',
)
register(
    id='Monominos-v0',
    entry_point='Games.Polymino.environment:Monominos',
    reward_threshold=1000.0
)
register(
    id='Dominos-v0',
    entry_point='Games.Polymino.environment:Dominosv0',
)
register(
    id='Dominos-v1',
    entry_point='Games.Polymino.environment:Dominosv1',
)
register(
    id='Dominos-v2',
    entry_point='Games.Polymino.environment:Dominosv2',
)
register(
    id='Triminos-v0',
    entry_point='Games.Polymino.environment:Triminos',
)
