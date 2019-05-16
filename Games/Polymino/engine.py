import random
import numpy as np
class tetramino():
    def __init__(self,shape,offset,c=0,d=0,env = None, id_ = 0):
        self.env = env
        #pts is a set of coordinates representing the piece
        self.pts = shape
        #offset is solely for rotation, it's where the piece pivots from
        self.off = offset
        #pos is where the center of the piece is relative to the board
        if env!= None:
            self.pos = env.cfg.startpos.copy()
        else:
            self.pos = [-1,3]
        #pos+pts[x] gives the board position of the specific square
        #c is the colour number
        self.c = c
        #d=1 if the tetramino only has 2 rotate states
        self.d = d
        #orientation
        self.orientation = 0
        #what type of tetramino it is
        self.id_ = id_
    def rotate(self,d = 1):
        #d is the direction of rotation
        if self.off == None:
            return
        #goes to the other direction if there's only t rotate states
        #ex the I piece is only up or sideways
        if self.d !=0:
            d = self.d
            self.d *=-1
        new_pts = [a+[] for a in self.pts]
        for pos in new_pts:
            #find it relative to the pivot
            pos[0] -= self.off[0]
            pos[1] -= self.off[1]
            #rotate around
            pos[0],pos[1] = pos[1]*d,-pos[0]*d
            #move back based on the location of the pivot
            pos[0] = int(pos[0]+self.off[0])
            pos[1] = int(pos[1]+self.off[1])
        if not self.overlap(new_pts=new_pts):
            #only finalize if the rotation doesn't make it overlap with anything
            self.pts = new_pts
            self.orientation+=d
            self.orientation %=4
    def move(self,delta):
        new_pos = self.pos+[]
        new_pos[0]+= delta[0]
        new_pos[1] += delta[1]
        if not self.overlap(new_pos = new_pos):
            self.pos = new_pos
        elif delta == [1,0]:
            #if the new pos overlaps and was moving down,
            #the piece becomes a part of the board
            self.commit()
    def __str__(self):
        str_ = "    \n    \n    \n    \n"
        for pos in self.pts:
            str_ = str_[:5*pos[0]+pos[1]] + '@' + str_[5*pos[0]+pos[1]+1:]
        return str_
    def render(self):
        for pos in self.pts:
            p = (pos[0]+self.pos[0],pos[1]+self.pos[1])
            self.env.create_square(p,self.c)
    def commit(self):
        #THIS SHOULD TERMINATE WITH A NEGATIVE REWARD
        if self.overlap():
            self.env.done = True
            return
        for pos in self.pts:
            p = (pos[0]+self.pos[0],pos[1]+self.pos[1])
            self.env.game_board[p[0]][p[1]] = self.c
        #TODO: check if any lines are complete
        legend = self.env.cfg.legend.copy()
        for row in range(len(self.env.game_board)):
            if [a for a in self.env.game_board[row] if a==2] == []:
                del self.env.game_board[row]
                del legend[0]
                self.env.lines +=1
                self.env.game_board = [[2]*self.env.cfg.width]+ self.env.game_board
        self.env.on_ = self.env.next_
        self.env.next_ = random.choice(self.env.prefabs).copy(self.env)
        self.env.score += legend[0]*(self.env.level+1)
    def copy(self,env):
        return tetramino([a+[] for a in self.pts],self.off,self.c,self.d,env=env)
    def overlap(self,new_pts = None,new_pos = None):
        #new pts is testing for a rotation and new pos is testing for a translation
        new_pts = self.pts if new_pts == None else new_pts
        new_pos = self.pos if new_pos == None else new_pos
        for pt in new_pts:
            pt = [pt[0]+new_pos[0],pt[1]+new_pos[1]]
            #checks if out of bounds
            if pt[0] >= self.env.cfg.height or pt[0] < 0 or pt[1] >= self.env.cfg.width or pt[1] < 0:
                return True
            #checks if board already has a piece (2 is the empty value of the board)
            if self.env.game_board[pt[0]][pt[1]] != 2:
                return True
        return False

class Engine():
    
    def __init__(self,cfg):
        self.cfg = cfg
        self.prefabs = cfg.prefabs
        self.on_ = random.choice(self.prefabs).copy(self)
        self.next_ = random.choice(self.prefabs).copy(self)
        self.game_board = [[2]*cfg.width for x in range(cfg.height)]
        self.i = 0
        self.score = 0
        self.level = cfg.level
        self.lines = 0
        self.done = False
    def reset(self):
        self.i=0
        self.score=0
        self.lines=0
        self.game_board = [[2]*self.cfg.width for x in range(self.cfg.height)] #10x24
        self.on_ = random.choice(self.prefabs).copy(self)
        self.next_ = random.choice(self.prefabs).copy(self)
        self.done = False
    def update(self,action):
        #This actually handles all the inputs
        self.i+=1
        if action==0:
            self.on_.move([0,-1])
        if action == 1:
            self.on_.move([0,1])
        if action == 2:
            self.on_.rotate()
        if self.i>2:
            self.on_.move([1,0])
            self.i=0
            self.score+= self.cfg.downpts

    def get_state(self):
        #5 empty slots for the header :(
        header = [self.on_.pos[0],self.on_.pos[1],self.on_.orientation
                  ,self.on_.id_,self.next_.id_]+[0]*(self.cfg.width-5)
        header = [header[:self.cfg.width]]
        board2 = [[[1,0][a==2] for a in x]for x in self.game_board]
        for pos in self.on_.pts:
                p = (pos[0]+self.on_.pos[0],pos[1]+self.on_.pos[1])
                board2[p[0]][p[1]] = self.cfg.dynamicint
        return np.array(header+board2)
    def get_state_render(self):
        board2 = [[a for a in x]for x in self.game_board]
        for pos in self.on_.pts:
            p = (pos[0]+self.on_.pos[0],pos[1]+self.on_.pos[1])
            board2[p[0]][p[1]] = self.on_.c
        return np.array(board2)
    def seed(self,seed):
        random.seed(seed)
    def height(self):
        for y in range(len(self.game_board)):
            if [a for a in self.game_board[y] if a!=2] != []:
                return 24-y
        return 0
