try:
    from engine import tetramino
except:
    from Games.Polymino.engine import tetramino
class Polyminos():
    #polyminos are mainly just a list of points
    T = [[1, 1], [1, 2], [1, 3], [2, 2]]
    LR = [[1, 1], [1, 2], [1, 3], [2, 3]]
    ZL = [[1, 1], [1, 2], [2, 2], [2, 3]] #binary
    SQ = [[1,1],[1,2],[2,1],[2,2]]# None
    ZR = [[2, 1], [2, 2], [1, 2], [1, 3]] #bibary
    LL = [[2, 1], [1, 1], [1, 2], [1, 3]]
    LONG = [[1, 3], [1, 2], [1, 1], [1, 0]] # binary
    Tetraminos = [
    tetramino(T,[1,2],c=4),
    tetramino(LR,[1,2],c=3),
    tetramino(ZL,[1,2],c=1,d=1),
    tetramino(SQ,None,c=7),
    tetramino(ZR,[1,2],c=3,d=1),
    tetramino(LL,[1,2],c=1),
    tetramino(LONG,[1.5,1.5],c=4,d=1)]

    TSQ = [[1,1],[1,2],[2,1]]# None
    TT = [[1, 1], [1, 2], [1, 3]]
    Triminos = [
    tetramino(TT,[1,2],c=4,id_=0),
    tetramino(TSQ,[1.5,1.5],c=3,id_=1)]

    DLONG = [[1, 2], [1, 1]] # binary
    Dominos = [tetramino(DLONG,[1.5,1.5],c=4,d=1,id_=0)]

    Monominos = [tetramino([[1,1]],None,c=3,d=1,id_=0)]
def lreward(legend):
    def func(old_board,new_board,cleared):
        return legend[cleared]
    return func
def breward(legend,pheight=0.5,phole=0.36):
    def height(game_board):
        for y in range(len(game_board)):
            if [a for a in game_board[y] if a!=2] != []:
                return len(game_board)-y
        return 0
    def holes(game_board):
        holes=0
        for y in range(len(game_board)-1):
            for x in range(len(game_board[y])):
                if game_board[y][x]!=2:
                    holes+= (game_board[y+1][x]==2)
        return holes
    def func(old_board,new_board,cleared):
        reward =  legend[cleared]
        #print(height(new_board),height(old_board))
        reward += (height(old_board)-height(new_board))*pheight
        reward += (holes(old_board)-holes(new_board))*phole
        return reward
    return func
class Config():
    __default = {
        #The position the bottom left of a polymino starts in
	"startpos":[-1,3],
        #points awarded for line clears
        #         0  1  2   3   4   lines cleared
	"rfunc":lreward([0,40,100,300,1200]),
	"height":24,
	"width":10,
        #frames it takes to drop a piece
        "frames":3,
        #Polyminos available in the game
	"prefabs":Polyminos.Tetraminos,
        #Points awarded just for a piece moving down
	"downpts":0,
        #value of engine state for a point occupied by the controlled polymino
	"dynamicint":1,
        #True for a coloured render, false to see what the agent is given as input
        "niceView":True
	}
    def __init__(self,**kwargs):
        self.__dict__.update(Config.__default)
        self.__dict__.update(kwargs)


