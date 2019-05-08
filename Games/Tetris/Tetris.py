def keypress(event):
    #Here inputs are all stored in a dictionary called pressed
    #Keeping track of keypresses (adds the key)
    global pressed
    pressed[str(event.keysym)] = str(event.char)
def keyrelease(event):
    #Keeps track of key releases (removes the key)
    if str(event.keysym) in pressed:
        del pressed[str(event.keysym)]    
def handleroat():
    #This actually handles all the inputs
    global pressed,on_
    if 'a' in pressed:
        on_.move([0,-1])
        del pressed['a']
    if 'd' in pressed:
        on_.move([0,1])
        del pressed['d']
    if 's' in pressed:
        on_.move([1,0])
        #del pressed['s']
    if 'q' in pressed:
        on_.rotate(-1)
        del pressed['q']
    if 'e' in pressed:
        on_.rotate()
        del pressed['e']
def callback(event):
    c.focus_set()
def callback2(event):
    c.focus_set()
class tetramino():
    def __init__(self,shape,offset,c=0,d=0):
        #pts is a set of coordinates representing the piece
        self.pts = shape
        #offset is solely for rotation, it's where the piece pivots from
        self.off = offset
        #pos is where the center of the piece is relative to the board
        self.pos = [-1,3]
        #pos+pts[x] gives the board position of the specific square
        #c is the colour number
        self.c = c
        #d=1 if the tetramino only has 2 rotate states
        self.d = d
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
            create_square(p,self.c)
    def commit(self):
        global game_board,prefabs,on_,score,lines
        if self.overlap():
            game_board = [[2]*10 for x in range(24)] #10x24
            score = 0
            lines = 0
            on_ = random.choice(prefabs).copy()
            return
        for pos in self.pts:
            p = (pos[0]+self.pos[0],pos[1]+self.pos[1])
            game_board[p[0]][p[1]] = self.c
        #TODO: check if any lines are complete
        legend = [0,40,100,300,1200]
        for row in range(len(game_board)):
            if [a for a in game_board[row] if a==2] == []:
                del game_board[row]
                del legend[0]
                lines +=1
                game_board = [[2]*10]+ game_board
        on_ = random.choice(prefabs).copy()
        score += legend[0]*(level+1)
    def copy(self):
        return tetramino([a+[] for a in self.pts],self.off,self.c,self.d)
    def overlap(self,new_pts = None,new_pos = None):
        global game_board
        #new pts is testing for a rotation and new pos is testing for a translation
        new_pts = self.pts if new_pts == None else new_pts
        new_pos = self.pos if new_pos == None else new_pos
        for pt in new_pts:
            pt = [pt[0]+new_pos[0],pt[1]+new_pos[1]]
            #checks if out of bounds
            if pt[0] > 23 or pt[0] < 0 or pt[1] > 9 or pt[1] < 0:
                return True
            #checks if board already has a piece (2 is the empty value of the board)
            if game_board[pt[0]][pt[1]] != 2:
                return True
        return False
def rend():
    global game_board,on_, swap
    c.create_text(300,400,text = "Lines %d"%lines,fill="white",tag = 'tes')
    c.create_text(300,300,text = "Score %d"%score,fill="white",tag = 'tes')
    c.create_text(300,500,text = "Level %d"%level,fill="white",tag = 'tes')
    for col in range(len(game_board)):
        for row in range(len(game_board[0])):
            if game_board[col][row] != -1:
                create_square((col,row),game_board[col][row])
    #here the tetramino the player controls is rendered independantly from the
    #board
    on_.render()
def create_square(coords,palate):
    center = [300,400]
    scale = 10
    #can change the colour palate since the colours are numbered
    colours = ["orange","red","grey","green","blue","magenta","purple","yellow"]
    x1 = coords[1]*scale+center[1]
    x2 = x1+ scale
    y1 = coords[0]*scale+center[0]
    y2 = y1 + scale
    drend = c.create_rectangle(x1,y1,x2,y2,tag="tes",fill=colours[palate])

from tkinter import *
import random,time
print ("Move: WASD, Change Colour: Space/Mouse Click")
#controls = {"w":[1,-2],"s":[1,2],"a":[0,-2],"d":[0,2]}
pressed = {}
root = Tk()
c = Canvas(root, width=1000, height=800)
c.bind("<KeyPress>", keypress)
c.bind("<KeyRelease>", keyrelease)
c.bind("<Button-1>", callback)
c.bind("<Button-3>", callback2)
c.configure(background='black')
c.pack()
game_board = [[2]*10 for x in range(24)] #10x24

T = [[1, 1], [1, 2], [1, 3], [2, 2]]
LR = [[1, 1], [1, 2], [1, 3], [2, 3]]
ZL = [[1, 1], [1, 2], [2, 2], [2, 3]] #binary
SQ = [[1,1],[1,2],[2,1],[2,2]]# None
ZR = [[2, 1], [2, 2], [1, 2], [1, 3]] #bibary
LL = [[2, 1], [1, 1], [1, 2], [1, 3]]
LONG = [[1, 3], [1, 2], [1, 1], [1, 0]] # binary
prefabs = [
    tetramino(T,[1,2],c=4),
    tetramino(LR,[1,2],c=3),
    tetramino(ZL,[1,2],c=1,d=1),
    tetramino(SQ,None,c=7),
    tetramino(ZR,[1,2],c=3,d=1),
    tetramino(LL,[1,2],c=1),
    tetramino(LONG,[1.5,1.5],c=4,d=1)]
on_ = random.choice(prefabs).copy()
for a in prefabs:
    print (a, end = "")
def frames(x):
    nonstandard = [(29,1),(19,2),(16,3),(13,4),(10,5),(9,6)]
    if x < 9:
        return 48-x*5
    else:
        for a in nonstandard:
            if x >= a[0]:
                print(a,x)
                return a[1]
i = -40
last = time.time()-0.1
c.focus_set()
score = 0
level = 9
tick = 1/60*frames(level)
lines = 0
while True:
    i=time.time()
    if i-last>=tick:
        last=i
        on_.move([1,0])
    c.delete("tes")
    time.sleep(0.005)
    handleroat()
    rend()
    c.update()
root.geometry('%sx%s+%s+%s' %(1024, 768, 100, 100))
root.resizable(0, 0)
root.mainloop()
