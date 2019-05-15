import numpy as np
from Games.Dominos.environment import TetrisEnv
def file_name(div):
    return "./tetris_data.hdf5"

# this function generates the training data. It takes an arguement which says
# how many groups of 100k samples should be done

#from Games.Tetris.environment import TetrisEnv

def keypress(event):
    #Here inputs are all stored in a dictionary called pressed
    #Keeping track of keypresses (adds the key)
    global pressed
    pressed[str(event.keysym)] = str(event.char)
def keyrelease(event):
    global pressed,Timer
    #Keeps track of key releases (removes the key)
    if str(event.keysym) in pressed:
        del pressed[str(event.keysym)]
    if not('Left' in pressed or "Right" in pressed):
        Timer = None
def handleroat():
    global pressed,Timer
    #This actually handles all the inputs
    if 'Left' in pressed or "Right" in pressed:
        if Timer == None:
            Timer = i
            return int("Right" in pressed)
        dt = (i-Timer);
        if(dt>0.20):
            Timer+=0.08
            return int("Right" in pressed)    
    if 'space' in pressed:    
        del pressed['space']
        return 2
    return 3
def callback(event):
    env.c.focus_set()
def callback2(event):
    env.c.focus_set()

import random,time
print ("Move: WASD, Change Colour: Space/Mouse Click")
#controls = {"w":[1,-2],"s":[1,2],"a":[0,-2],"d":[0,2]}
Timer = None
pressed = {}
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
last = time.time()+1
#env.c.focus_set()
level = 15
tick = 1/180*frames(level)
env = TetrisEnv()
env.render()
env.c.bind("<KeyPress>", keypress)
env.c.bind("<KeyRelease>", keyrelease)
env.c.bind("<Button-1>", callback)
env.c.bind("<Button-3>", callback2)
env.c.focus_set()
def stuff():
    global i,last
    while True:
        time.sleep(0.001)
        i=time.time()
        if i-last>=tick:
            last=i
            in_state = env.get_state()
            action = handleroat()
            state,reward,done,args = env.step(action)
            env.render()
            #yield (in_state,action)
        if env.engine.done:
            env.reset()
stuff()
