import numpy as np
import gym
import gym.spaces
from tkinter import *
try:
    from engine import Engine
    import Config
except:
    from Games.Polymino.engine import Engine
    from Games.Polymino import Config

#Generalized tetris environment
class TetrisEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self,cfg):
        self.engine = Engine(cfg)
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=-1, high=1,shape=[cfg.height+1,cfg.width])
        self.steps = []
        self.c = None
        self.num_envs = 1
        #for visualizing the game only
        self.niceView = cfg.niceView
    def reset(self):
        #engine.reset() resets the game
        self.engine.reset() 
        state = self.get_state()
        self.steps.append(list(state))
        return np.array(state)

    def step(self,action):
        score = self.engine.score
        curr_state = self.engine.get_state()
        self.engine.update(action)
        next_state = self.engine.get_state()
        reward = self.engine.score-score
        return next_state, reward, self.engine.done, {}

    def get_state(self):
        return self.engine.get_state()
    def seed(self,seed):
        self.engine.seed(seed)
    def render(self, mode ='human'):
        if self.c == None:
            root = Tk()
            self.c = Canvas(root, width=1000, height=800)
            self.c.configure(background='black')
            self.c.pack()
        if self.niceView:
            #rendering nicely
            self.rend(self.engine.get_state_render(),self.c)
        else:
            #rendering what the learning agent sees
            self.rend(self.engine.get_state()[1:],self.c)
    def rend(self,game_board,c):
        #tkinter is required
        c.delete("tes")
        for pt in self.engine.next_.pts:
            self.create_square([pt[0]+10,pt[1]+15],self.engine.next_.c,self.c)
        lines,score,level = self.engine.lines,self.engine.score, 10-self.engine.frames
        c.create_text(300,400,text = "Lines %d"%lines,fill="white",tag = 'tes')
        c.create_text(300,300,text = "Score %.2f"%score,fill="white",tag = 'tes')
        c.create_text(300,500,text = "Level %d"%level,fill="white",tag = 'tes')
        for col in range(len(game_board)):
            for row in range(len(game_board[0])):
                if game_board[col][row] != -1:
                    self.create_square((col,row),game_board[col][row],c)
        #here the tetramino the player controls is rendered independantly from the
        #board
        c.update()
    def create_square(self,coords,palate,c):
        center = [300,400]
        scale = 10
        #can change the colour palate since the colours are numbered
        colours = ["orange","red","grey","green","blue","magenta","purple","yellow"]
        x1 = coords[1]*scale+center[1]
        x2 = x1+ scale
        y1 = coords[0]*scale+center[0]
        y2 = y1 + scale
        drend = c.create_rectangle(x1,y1,x2,y2,tag="tes",fill=colours[palate])

#Specific gamemodes based on the general model
class Tetris(TetrisEnv):
    def __init__(self):
        super().__init__(Config.Config())
class Monominos(TetrisEnv):
    def __init__(self):
        kwargs = {"rfunc":Config.lreward([0,1]),
                  "height":24,
                  "prefabs":Config.Polyminos.Monominos}
        super().__init__(Config.Config(**kwargs))
class Dominosv2(TetrisEnv):
    def __init__(self):
        kwargs = {"prefabs":Config.Polyminos.Dominos,
                  "rfunc":Config.breward([0,1,3]),
                  "frames":1}
        super().__init__(Config.Config(**kwargs))
class Dominosv1(TetrisEnv):
    def __init__(self):
        kwargs = {"prefabs":Config.Polyminos.Dominos,
		  "width":6,"height":16,
		  "startpos":[-1,1],
                  "rfunc":Config.lreward([0,1,3])}
        super().__init__(Config.Config(**kwargs))
class Dominosv0(TetrisEnv):
    def __init__(self):
        kwargs = {"prefabs":Config.Polyminos.Dominos,
                  "rfunc":Config.lreward([0,1,3])}
        super().__init__(Config.Config(**kwargs))
class Triminos(TetrisEnv):
    def __init__(self):
        kwargs = {"prefabs":Config.Polyminos.Triminos,
                  "rfunc":Config.lreward([0,1,3,9])}
        super().__init__(Config.Config(**kwargs))

