import numpy as np
def check_open_threes(chessboard, move):
    H, W = chessboard.shape
    i, j = move
    assert(chessboard[i,j]==1)
    l = []
    # 1. left-right
    if j>=1 and j< W-1:
        for k in range(3):
            j1 = j-k-1
            j2 = j+3-k
            if j1 < 0 or j2 >= W:
                continue
            if (j1 == 0 and chessboard[i,j2+1] == 2) or (j2+1==W and chessboard[i,j1-1]==2) or (j1 - 1>=0 and j2+1<W and chessboard[i, j1-1] == 2 and chessboard[i,j2+1]==2):
                continue
            if chessboard[i,j1]==0 and chessboard[i,j2]==0 and chessboard[i, j1+1] == 1 and chessboard[i, j1+2] == 1 and chessboard[i, j1+3] == 1:
                if (j1>= 1 and chessboard[i,j1-1] == 1) or (j2<W-1 and chessboard[i,j2+1] ==1):
                    continue
                l.append([(i,j1+1),(i,j1+2), (i,j1+3)])
        
        for k in range(4):
            j1 = j-k-1
            j2 = j+4-k
            if j1 < 0 or j2 >= W:
                continue
            if chessboard[i,j1]==0 and chessboard[i,j2]==0 and chessboard[i,j1+1] == 1 and chessboard[i,j2-1]==1 and \
            ((chessboard[i,j1+2] == 1 and chessboard[i,j1+3] == 0) or (chessboard[i,j1+2] == 0 and chessboard[i,j1+3] == 1)):
                point = (i,j1+2) if chessboard[i,j1+2] == 1 else (i,j1+3)
                l.append([(i,j1+1),point, (i,j2-1)])


    # 2. up-down
    if i>=1 and i< H-1:
        for k in range(3):
            i1 = i-k-1
            i2 = i+3-k
            if i1 < 0 or i2 >= H:
                continue
            if (i1 == 0 and chessboard[i2+1,j] == 2) or (i2+1==H and chessboard[i1-1,j]==2) or (i1 - 1>=0 and i2+1<H and chessboard[i1-1, j] == 2 and chessboard[i2+1,j]==2):
                continue
            if chessboard[i1,j]==0 and chessboard[i2,j]==0 and chessboard[i1+1, j] == 1 and chessboard[i1+2, j] == 1 and chessboard[i1+3, j] == 1:
                if (i1>= 1 and chessboard[i1-1,j] == 1) or (i2<H-1 and chessboard[i2+1,j] ==1):
                    continue
                l.append([(i1+1,j),(i1+2,j), (i1+3,j)])
        
        for k in range(4):
            i1 = i-k-1
            i2 = i+4-k
            if i1 < 0 or i2 >= H:
                continue
            if chessboard[i1,j]==0 and chessboard[i2,j]==0 and chessboard[i1+1,j] == 1 and chessboard[i2-1,j]==1 and \
            ((chessboard[i1+2,j] == 1 and chessboard[i1+3,j] == 0) or (chessboard[i1+2,j] == 0 and chessboard[i1+3,j] == 1)):
                point = (i1+2,j) if chessboard[i1+2,j] == 1 else (i1+3,j)
                l.append([(i1+1,j),point, (i2-1,j)])


    # 3. left_down - right_up
    if 1<=i<H-1 and 1<=j<W-1:
        for k in range(3):
            i1 = i+1+k
            i2 = i-3+k
            j1 = j-1-k
            j2 = j+3-k
            if i1 >= H or i2 < 0 or j1 < 0 or j2 >= W:
                continue
            
            if (i1 == H-1 and j2==W-1) or (i2 ==0 and j1 == 0) or (i1==H-1 and chessboard[i2-1,j2+1]!=0) or (j2 == W-1 and chessboard[i1+1,j1-1]!=0) or \
            (i2 == 0 and chessboard[i1+1,j1-1]!=0) or (j1==0 and chessboard[i2-1,j2+1]!=0):
                continue
            if i1+1 < H and j1-1>=0 and i2-1>=0 and j2+1 < W and ((chessboard[i1+1,j1-1]==2 and chessboard[i2-1,j2+1] == 2) or chessboard[i1+1,j1-1]==1 or chessboard[i2-1,j2+1] == 1):
                continue
            
            if chessboard[i1, j1] == 0 and chessboard[i1-1,j1+1] == 1 and chessboard[i1-2,j1+2] == 1 and chessboard[i1-3,j1+3] == 1 and chessboard[i1-4,j1+4] == 0:
                l.append([(i1-1,j1+1), (i1-2,j1+2), (i1-3,j1+3)])

        for k in range(4):
            i1 = i+1+k
            i2 = i-4+k
            j1 = j-1-k
            j2 = j+4-k
            if i1 >= H or i2 < 0 or j1 < 0 or j2 >= W:
                continue
            if chessboard[i1,j1] == 0 and chessboard[i2, j2]==0 and chessboard[i1-1,j1+1] == 1 and chessboard[i2+1, j2-1] == 1 and \
                ((chessboard[i1-2,j1+2] == 1 and chessboard[i1-3,j1+3] == 0) or (chessboard[i1-2,j1+2] == 0 and chessboard[i1-3,j1+3] == 1)):

                point = (i1-2,j1+2) if chessboard[i1-2,j1+2] == 1 else (i1-3,j1+3)
                l.append([(i1-1,j1+1), point, (i2+1,j2-1)])

     # 4. left_up-right_down
    if 1<=i<H-1 and 1<=j<W-1:
        for k in range(3):
            i1 = i-k-1
            i2 = i+3-k
            j1 = j-k-1
            j2 = j+3-k
            if i1 < 0 or i2 >= H or j1 < 0 or j2 >= W:
                continue
            if (j1 == 0 and i2+1 <H and chessboard[i2+1,j2+1] == 2) or (i1==0 and j2+1< W and chessboard[i2+1,j2+1] == 2 ) or (j2==W-1 and i1-1 >= 0 and chessboard[i1-1,j1-1]==2) or (i2==H-1 and j1-1>=0 and chessboard[i1-1,j1-1]==2) or (j1 - 1>=0 and i1-1>=0 and j2+1<W and i2+1<H and chessboard[i1-1, j1-1] == 2 and chessboard[i2+1,j2+1]==2):
                continue
            if chessboard[i1,j1] == 0 and chessboard[i1+1,j1+1] == 1 and chessboard[i1+2,j1+2] == 1 and chessboard[i1+3,j1+3] == 1 and chessboard[i1+4,j1+4] == 0:
                if (j1>= 1 and i1>=1 and chessboard[i1-1,j1-1] == 1) or (j2<W-1 and i2<H-1 and chessboard[i2+1,j2+1] ==1):
                    continue
                l.append([(i1+1,j1+1),(i1+2,j1+2),(i1+3,j1+3)])

        for k in range(4):
            i1 = i-k-1
            i2 = i+4-k
            j1 = j-k-1
            j2 = j+4-k
            if i2 >= H or i1 < 0 or j1 < 0 or j2 >= W:
                continue
            if chessboard[i1,j1]==0 and chessboard[i2,j2]==0 and chessboard[i1+1,j1+1] == 1 and chessboard[i2-1,j2-1]==1 and \
            ((chessboard[i1+2,j1+2] == 1 and chessboard[i1+3,j1+3] == 0) or (chessboard[i1+2,j1+2] == 0 and chessboard[i1+3,j1+3] == 1)):
                point = (i1+2,j1+2) if chessboard[i1+2,j1+2] == 1 else (i1+3,j1+3)
                l.append([(i1+1,j1+1), point, (i2-1,j2-1)])
    return l
        
            
def check_fours(chessboard, move):
    H, W = chessboard.shape
    i, j = move
    l = []
    assert(chessboard[i,j]==1)

    # 1. left-right
    if j>=0 and j<= W-1:
        # oooo
        for k in range(4):
            j1 = j-k-1
            j2 = j-k+4
            if j1 < -1 or j2 > W:
                continue
            if j1 == -1 and chessboard[i,j2] !=0:
                continue
            if j2 == W and  chessboard[i,j1] !=0:
                continue
            if chessboard[i,j1+1] == 1 and chessboard[i,j1+2] == 1 and chessboard[i,j1+3] == 1 and chessboard[i,j1+4] == 1:
                if j1>=0 and j2 < W  and ((chessboard[i,j1]==2 and chessboard[i,j2]==2) or chessboard[i,j1]==1 or chessboard[i,j2] == 1):
                    continue
                l.append([(i,j1+1),(i,j1+2),(i,j1+3),(i,j1+4)])
        # oxooo
        # ooxoo
        # oooxo
        for k in range(5):
            j1 = j-k-1
            j2 = j-k+5
            if j1 < -1 or j2 > W:
                continue
            if j1 == -1 and chessboard[i,j2] ==1:
                continue
            if j2 == W and chessboard[i,j1] == 1:
                continue
            if j1>=0 and j2<W and (chessboard[i,j1]==1 or chessboard[i,j2]==1):
                continue

            if chessboard[i,j1+1] == 1 and chessboard[i,j2-1]==1: 
                if chessboard[i,j1+2]==0 and chessboard[i,j1+3]==1 and chessboard[i,j1+4]==1:
                    l.append([(i,j1+1),(i,j1+3),(i,j1+4),(i,j2-1)])
                elif chessboard[i,j1+2]==1 and chessboard[i,j1+3]==0 and chessboard[i,j1+4]==1:
                    l.append([(i,j1+1),(i,j1+2),(i,j1+4),(i,j2-1)])
                elif chessboard[i,j1+2]==1 and chessboard[i,j1+3]==1 and chessboard[i,j1+4]==0:
                    l.append([(i,j1+1),(i,j1+2),(i,j1+3),(i,j2-1)])


    # 2. up-down
    if i>=0 and i<= H-1:
        for k in range(4):
            i1 = i-k-1
            i2 = i-k+4
            if i1 < -1 or i2 > H:
                continue
            if i1 == -1 and chessboard[i2,j] !=0:
                continue
            if i2 == H and  chessboard[i1,j] !=0:
                continue

            if chessboard[i1+1,j] == 1 and chessboard[i1+2,j] == 1 and chessboard[i1+3,j] == 1 and chessboard[i1+4,j] == 1:
                if i1>=0 and i2 < H  and ((chessboard[i1,j]==2 and chessboard[i2,j]==2) or chessboard[i1,j]==1 or chessboard[i2,j] == 1):
                    continue
                l.append([(i1+1,j),(i1+2,j),(i1+3,j),(i1+4,j)])
        # oxooo
        # ooxoo
        # oooxo
        for k in range(5):
            i1 = i-k-1
            i2 = i-k+5
            if i1 < -1 or i2 > H:
                continue
            if i1 == -1 and chessboard[i2,j] ==1:
                continue
            if i2 == H and chessboard[i1,j] == 1:
                continue
            if i1>=0 and i2<H and (chessboard[i1,j]==1 or chessboard[i2,j]==1):
                continue

            if chessboard[i1+1,j] == 1 and chessboard[i2-1,j]==1: 
                if chessboard[i1+2,j]==0 and chessboard[i1+3,j]==1 and chessboard[i1+4,j]==1:
                    l.append([(i1+1,j),(i1+3,j),(i1+4,j),(i2-1,j)])
                elif chessboard[i1+2,j]==1 and chessboard[i1+3,j]==0 and chessboard[i1+4,j]==1:
                    l.append([(i1+1,j),(i1+2,j),(i1+4,j),(i2-1,j)])
                elif chessboard[i1+2,j]==1 and chessboard[i1+3,j]==1 and chessboard[i1+4,j]==0:
                    l.append([(i1+1,j),(i1+2,j),(i1+3,j),(i2-1,j)])
    # 3. left_down - right_up
    if 0<=i<H and 0<=j<W:
        for k in range(4):
            i1 = i+1+k
            i2 = i-4+k
            j1 = j-1-k
            j2 = j+4-k
            if i1 > H or i2 <-1 or j1 <-1 or j2 >W:
                continue
            if i1 == H and j2 < W and chessboard[i2,j2] != 0:
                continue
            if i2 == -1 and j1 >= 0 and  chessboard[i1,j1] != 0:
                continue
            if j1 == -1 and i2 >= 0 and chessboard[i2,j2] != 0:
                continue
            if j2 == W and i1 < H and chessboard[i1,j1] != 0:
                continue
            if chessboard[i1-1,j1+1] == 1 and  chessboard[i1-2,j1+2] == 1 and chessboard[i1-3,j1+3] == 1 and chessboard[i1-4,j1+4] == 1:
                if i1< H and j2 < W and j1 >=0 and i2>=0 and ((chessboard[i1,j1]==2 and chessboard[i2,j2]==2) or chessboard[i1,j1] == 1 or chessboard[i2,j2]==1):
                    continue
                l.append([(i1-1,j1+1),(i1-2,j1+2),(i1-3,j1+3),(i1-4,j1+4)])

        for k in range(5):
            i1 = i+1+k
            i2 = i-5+k
            j1 = j-1-k
            j2 = j+5-k
            if i1 > H or i2 <-1 or j1 <-1 or j2 >W:
                continue
            if i1 == H and j2 < W and chessboard[i2,j2] == 1:
                continue
            if i2 == -1 and j1 >= 0 and  chessboard[i1,j1] == 1:
                continue
            if j1 == -1 and i2 >= 0 and chessboard[i2,j2] == 1:
                continue
            if j2 == W and i1 < H and chessboard[i1,j1] == 1:
                continue
            
            if i1 < H and j2 < W and j1>=0 and i2>=0 and (chessboard[i1,j1]==1 or chessboard[i2,j2]==1):
                continue
            if chessboard[i1-1,j1+1] == 1 and chessboard[i2+1,j2-1] == 1:
                if chessboard[i1-2,j1+2] == 1 and chessboard[i1-3,j1+3] == 1 and chessboard[i1-4,j1+4] == 0:
                    l.append([(i1-1,j1+1),(i1-2,j1+2),(i1-3,j1+3), (i2+1,j2-1)])
                elif chessboard[i1-2,j1+2] == 1 and chessboard[i1-3,j1+3] == 0 and chessboard[i1-4,j1+4] == 1:
                    l.append([(i1-1,j1+1),(i1-2,j1+2),(i1-4,j1+4), (i2+1,j2-1)])
                elif chessboard[i1-2,j1+2] == 0 and chessboard[i1-3,j1+3] == 1 and chessboard[i1-4,j1+4] == 1:
                    l.append([(i1-1,j1+1),(i1-3,j1+3),(i1-4,j1+4), (i2+1,j2-1)])

            

    # 4. left_up - right_down
    if 0<=i<H and 0<=j<W:
        for k in range(4):
            i1 = i-1-k
            i2 = i+4-k
            j1 = j-1-k
            j2 = j+4-k
            if i1 <-1  or i2 >H or j1 <-1 or j2 >W:
                continue
            if i1 == -1 and j2 < W and chessboard[i2,j2] != 0:
                continue
            if i2 == H and j1 >= 0 and  chessboard[i1,j1] != 0:
                continue
            if j1 == -1 and i2 < H and chessboard[i2,j2] != 0:
                continue
            if j2 == W and i1 > 0 and chessboard[i1,j1] != 0:
                continue
            if chessboard[i1+1,j1+1] == 1 and  chessboard[i1+2,j1+2] == 1 and chessboard[i1+3,j1+3] == 1 and chessboard[i1+4,j1+4] == 1:
                if i2< H and j2 < W and j1 >=0 and i1>=0 and ((chessboard[i1,j1]==2 and chessboard[i2,j2]==2) or chessboard[i1,j1] == 1 or chessboard[i2,j2]==1):
                    continue
                l.append([(i1+1,j1+1),(i1+2,j1+2),(i1+3,j1+3),(i1+4,j1+4)])

        for k in range(5):
            i1 = i-1-k
            i2 = i+5-k
            j1 = j-1-k
            j2 = j+5-k
            if i1 <-1  or i2 >H or j1 <-1 or j2 >W:
                continue
            if i1 == -1 and j2 < W and chessboard[i2,j2] == 1:
                continue
            if i2 == H and j1 >= 0 and  chessboard[i1,j1] == 1:
                continue
            if j1 == -1 and i2 < H and chessboard[i2,j2] == 1:
                continue
            if j2 == W and i1 > 0 and chessboard[i1,j1] == 1:
                continue
            
            if i2 < H and j2 < W and j1>=0 and i1>=0 and (chessboard[i1,j1]==1 or chessboard[i2,j2]==1):
                continue
            if chessboard[i1+1,j1+1] == 1 and chessboard[i2-1,j2-1] == 1:
                if chessboard[i1+2,j1+2] == 1 and chessboard[i1+3,j1+3] == 1 and chessboard[i1+4,j1+4] == 0:
                    l.append([(i1+1,j1+1),(i1+2,j1+2),(i1+3,j1+3), (i2-1,j2-1)])
                elif chessboard[i1+2,j1+2] == 1 and chessboard[i1+3,j1+3] == 0 and chessboard[i1+4,j1+4] == 1:
                    l.append([(i1+1,j1+1),(i1+2,j1+2),(i1+4,j1+4), (i2-1,j2-1)])
                elif chessboard[i1+2,j1+2] == 0 and chessboard[i1+3,j1+3] == 1 and chessboard[i1+4,j1+4] == 1:
                    l.append([(i1+1,j1+1),(i1+3,j1+3),(i1+4,j1+4), (i2-1,j2-1)])

    return l

def check_six(chessboard, move):
    H, W = chessboard.shape
    i, j = move
    assert(chessboard[i,j]==1)

    for k in range(6):
        j1 = max(j-k,0)
        j2 = min(j+6-k,W)
        if j2-j1 == 6 and np.sum(chessboard[i,j1:j2]==1)==6:
            return 1

        # 2. up down
    for k in range(6):
        i1 = max(i-k,0)
        i2 = min(i+6-k,H)
        if i2-i1 == 6 and np.sum(chessboard[i1:i2,j]==1)==6:
            return 1

        # 3. leftdown rightup
    for k in range(6):
        i1 = min(i+k, H - 1)
        i2 = max(i-6+k, -1)
        j1 = max(j-k, 0)
        j2 = min(j+6-k, W)
        if i1-i2 == 6 and j2-j1 == 6 and np.sum(chessboard[range(i1,i2,-1),range(j1,j2)]==1)==6:
            return 1

        # 4. leftup rightdown
    for k in range(6):
        i1 = max(i-k, 0)
        i2 = min(i+6-k, H)
        j1 = max(j-k, 0)
        j2 = min(j+6-k, W)
        if i2-i1 == 6 and j2-j1 == 6 and np.sum(chessboard[range(i1,i2),range(j1,j2)]==1)==6:
            return 1
    return 0

def forbidden_rule(chessboard, move):
    "Return 1 if this move is forbidden else return 0"
    six = check_six(chessboard, move)
    if six ==  1:
        return 1
    two_fours = check_fours(chessboard, move)
    if len(two_fours) >= 2:
        return 1
    elif len(two_fours) == 1:
        for i in two_fours[0]:
             if len(check_fours(chessboard, i)) == 2:
                 return 1
    
    open_threes = check_open_threes(chessboard, move)
    if len(open_threes) >= 2:
        return 1
    elif len(open_threes) == 1:
        for i in open_threes[0]:
             if len(check_open_threes(chessboard, i)) == 2:
                 return 1
    return 0

    


class GomokuBoard:

    def __init__(self, size = (8,8)):
        self.chessboard = np.zeros((size[0], size[1]), dtype = int)
        self.H = size[0] # the height of chessboard
        self.W = size[1] # the weight of chessboard
       # self.player1 = 0
       # self.player2 = 0
        self.turn = 1  # the current player
        self.availables = [(i,j) for i in range(self.H) for j in range(self.W)] # available positions for current player
        self.last_move = None
    
    def reset(self):
        self.chessboard = np.zeros((self.H, self.W), dtype = int)
        self.turn = 1
        self.availables = [(i,j) for i in range(self.H) for j in range(self.W)]
    def state(self):
        '''
        return the state for current player
        '''
        player = self.turn
        state = np.zeros((4,self.H, self.W))
        state[0][self.chessboard == self.turn] = 1
        state[1][self.chessboard == (self.turn % 2 + 1)] = 1
        if self.last_move:
            state[2][self.last_move] = 1
        if self.turn == 1: # initial player
            state[3] = 1
        return state

    def do_move(self, move):
        # take a move
        i,j = move
        player = self.turn
        
        try: 
            if self.chessboard[i,j] == 0:
                self.chessboard[i,j] = player
                self.availables.remove((i,j))
                self.last_move = (i,j)
                self._exchange_player()
                return 1
            else: 
                raise
        except:
            print("This position has been occupied or is beyond boundary, please try another position~!")
            return 0

    def get_result(self, forbidden = True):
        """ Get the result of the game according to the last move, return 
        result  O: continue, 1:player 1 (black) win, 2:player 2 (white) win, 3: draw"""
        if self.last_move == None:
            return 0
        i,j = self.last_move
        player = (self.turn % 2) + 1        # last player
            
        if forbidden and player == 1: # require forbidden and current player is black
            if forbidden_rule(self.chessboard, (i,j)):
                return 2
        
        # 1. left right
        for k in range(5):
            j1 = max(j-k,0)
            j2 = min(j+5-k,self.W)
            if j2-j1 == 5 and np.sum(self.chessboard[i,j1:j2]==player)==5:
                return player

        # 2. up down
        for k in range(5):
            i1 = max(i-k,0)
            i2 = min(i+5-k,self.H)
            if i2-i1 == 5 and np.sum(self.chessboard[i1:i2,j]==player)==5:
                return player

        # 3. leftdown rightup
        for k in range(5):
            i1 = min(i+k, self.H - 1)
            i2 = max(i-5+k, -1)
            j1 = max(j-k, 0)
            j2 = min(j+5-k, self.W)
            if i1-i2 == 5 and j2-j1 == 5 and np.sum(self.chessboard[range(i1,i2,-1),range(j1,j2)]==player)==5:
                return player

        # 4. leftup rightdown
        for k in range(5):
            i1 = max(i-k, 0)
            i2 = min(i+5-k, self.H)
            j1 = max(j-k, 0)
            j2 = min(j+5-k, self.W)
            if i2-i1 == 5 and j2-j1 == 5 and np.sum(self.chessboard[range(i1,i2),range(j1,j2)]==player)==5:
                return player
 
        if self.availables == []:
            return 3
        return 0
    
    def _exchange_player(self):
        self.turn = 1 if self.turn == 2 else 2
        
class GomokuGame:
    def __init__(self, board, is_self_play = True):
        self.board = board
        self.is_self_play = is_self_play

    def start_self_play(self, player, temp=1e-3):
        ''' start a self-play game using a MCTS player, reuse the search tree,
        and store the self-play data: (state, mcts_probs, z) for training '''
        self.board.reset()
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board,
                                                 temp=temp,
                                                 return_prob=1)
            # store the data
            states.append(self.board.state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.turn)
            # perform a move
            self.board.do_move(move)
            result = self.board.get_result()
            z = np.zeros(len(current_players))
            if result == 3:
                return result, zip(states, mcts_probs, z)
            elif result == 0:
                continue
            else:
                z[np.array(current_players) == result] = 1.0
                z[np.array(current_players) != result] = -1.0

                return result, zip(states, mcts_probs, z)
            
        
        

