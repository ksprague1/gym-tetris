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
        if self.overlap():
            self.env.done = True
            return
        old_board = np.copy(self.env.game_board)
        for pos in self.pts:
            p = (pos[0]+self.pos[0],pos[1]+self.pos[1])
            self.env.game_board[p[0]][p[1]] = self.c
        #TODO: check if any lines are complete
        cleared = 0
        for row in range(len(self.env.game_board)):
            if [a for a in self.env.game_board[row] if a==2] == []:
                del self.env.game_board[row]
                cleared+=1
                self.env.lines +=1
                #Add in a new empty line
                self.env.game_board = [[2]*self.env.cfg.width]+ self.env.game_board
        self.env.on_ = self.env.next_
        self.env.next_ = random.choice(self.env.prefabs).copy(self.env)
        #the score is updated in accordance with the reward function in fonfig
        self.env.score += self.env.cfg.rfunc(old_board,self.env.game_board,cleared)
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
        #prefabs are all the polyminos the game is allowed to use
        self.prefabs = cfg.prefabs
        #The polymino is decided by picking a random one from prefabs
        self.on_ = random.choice(self.prefabs).copy(self)
        self.next_ = random.choice(self.prefabs).copy(self)
        #board is represented by a heightxwidth grid of integers
        #[0][0] is top left and [width-1][height-1] is bottom right
        self.game_board = [[2]*cfg.width for x in range(cfg.height)]
        self.i = 0
        self.score = 0
        self.lines = 0
        self.done = False
        self.frames = cfg.frames
    def reset(self):
        self.i=0
        self.score=0
        self.lines=0
        self.game_board = [[2]*self.cfg.width for x in range(self.cfg.height)] #10x24
        self.on_ = random.choice(self.prefabs).copy(self)
        self.next_ = random.choice(self.prefabs).copy(self)
        self.done = False
    def update(self,action):
        """Updates the board based on an action given"""
        #This actually handles all the inputs
        self.i+=1
        if action==0:
            self.on_.move([0,-1])
        if action == 1:
            self.on_.move([0,1])
        if action == 2:
            self.on_.rotate()
        if self.i>=self.frames:
            self.on_.move([1,0])
            self.i=0
            #updates score in accordance to config
            #this score is just for moving a piece down
            self.score+= self.cfg.downpts

    def get_state(self):
        """Getter for environment state"""
        #5 empty slots for the header :(
        header = [self.on_.pos[0],self.on_.pos[1],self.on_.orientation
                  ,self.on_.id_,self.next_.id_]+[0]*(self.cfg.width-5)
        #if the width is less then 5 the last entries are dropped
        header = [header[:self.cfg.width]]
        # all board positions are now 0 if occupied or 1 if empty
        board2 = [[[1,0][a==2] for a in x]for x in self.game_board]
        for pos in self.on_.pts:
                p = (pos[0]+self.on_.pos[0],pos[1]+self.on_.pos[1])
                #boards with the controlled polymino are set to a special
                #value in accordance to the config (default is 1)
                board2[p[0]][p[1]] = self.cfg.dynamicint
        return np.array(header+board2)
    def get_state_render(self):
        """Special Getter for visulaizing the environment state"""
        #the board is by default colour coated to look nicer with the integer
        #at a specific board position representing the colour of that tile
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
