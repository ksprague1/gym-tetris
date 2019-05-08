import numpy as np
import gym
import gym.spaces
from engine import Engine

def segments(p):
    return zip(p, p[1:] + [p[0]])

class TetrisEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        self.engine = Engine()
        self.action_space = gym.spaces.Discrete(4)
        self.steps = []
        

    def reset(self):
        self.engine.reset() 
        state = self.get_state()
        self.steps.append(list(state))
        return np.array(state)

    def step(self,action):
        score = engine.score
        curr_state = self.engine.get_state()
        self.engine.update(action)
        next_state = self.engine.get_state()
        reward = engine.score-score
        return next_state, reward, engine.done, {}

    def get_state(self):
        return self.engine.get_state()


    def render(self, mode ='human'):
       return 0 
