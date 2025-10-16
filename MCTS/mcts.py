import math
import random
class gameState:
    def __init__(self,board=None,player=1):
        self.board=board
        if(self.board==None):
            self.board=[[0 for j in range(3)]for i in range(3)]
        self.player=player
    def legal_moves(self):
        b=self.board
        lm=[[0 for j in range(3)]for i in range(3)]
        for i in range(3):
            for j in range(3):
                if b[i][j]==0:
                    lm[i][j]=1
        return lm 
    def clone(self):
        return gameState([row[:] for row in self.board],self.player)           
    def playMove(self,x,y):
        if self.board[x][y]==0:
            self.board[x][y]=self.player
            if self.player==1:
                self.player=2
            else:
                self.player=1
            return True
        return False
    def nextState(self,x,y):
        cur_state=gameState([row[:] for row in self.board],self.player)
        lm=cur_state.legal_moves()
        if lm[x][y]==1:
            cur_state.board[x][y]=self.player
            if cur_state.player==1:
                cur_state.player=2
            else:
                cur_state.player=1
            return cur_state
        return False
    def check_terminated(self):
        b=self.board
        if b[0][0]==b[1][1] and b[1][1]==b[2][2] and b[1][1]!=0:
           return b[0][0]
        if b[2][0]==b[1][1] and b[1][1]==b[0][2] and b[1][1]!=0:
           return b[1][1]
        for i in range(3):
            is_sameX=True
            is_sameY=True
            X=b[i][0]
            Y=b[0][i]
            for j in range(3):
               if(b[i][j]!=X or b[i][j]==0):
                   is_sameX=False
               if(b[j][i]!=Y or b[j][i]==0):
                   is_sameY=False
            if(is_sameX):
                return X
            elif(is_sameY):
                return Y
        for i in range(3):
            for j in range(3):
                if(b[i][j]==0):
                    return None  
        return 0 
    def print_board(self):
        b=self.board
        for i in range(3):
            r=list()
            for j in range(3):
                if(b[i][j]==1):
                    r.append("O")
                elif(b[i][j]==2):
                    r.append("X")
                else:
                    r.append("-")
            print(r)

class node:
    def __init__(self,state,parent=None,prev_move=None):
        self.state=state
        self.parent=parent
        self.prev_move=prev_move
        self.children=[]
        lm=self.state.legal_moves()
        vm=list()
        for i in range(3):
            for j in range(3):
                if lm[i][j]==1:
                    vm.append((i,j))
        self.next_moves=vm
        self.W=0.0
        self.N=0
    def getBestChild(self,c):
        maxucb=-float('inf')
        maxchild=None
        for ch in self.children:
            N=ch.N
            W=ch.W
            ucb=float(W/(N+1))+c*float((float(math.log(self.N+1) /(N+1)))**(1/2))
            if ucb>maxucb:
                maxucb=ucb
                maxchild=ch
        return maxchild           

    def expand(self):
        if len(self.next_moves)==0:
            return None
        nxtmv=self.next_moves.pop()
        newstate=(self.state.clone()).nextState(nxtmv[0],nxtmv[1])
        
        parent=self
        chnode=node(newstate,parent,nxtmv)
        self.children.append(chnode)
        return chnode
    
    def isFullyExpanded(self):
        return len(self.next_moves)==0
    
    def update(self,result):
        self.N+=1
        if result==0:
            self.W+=0.5
        elif result==3-self.state.player:
            self.W+=1
        else:
            self.W+=0
        if self.parent is not None:
            self.parent.update(result)            
class MCTS:
    def __init__(self,c=1.2,loops=1000):
        self.c=c
        self.loops=loops
    def rollout(self,state):
        tempstate=state.clone()
        while True:
            lm=tempstate.legal_moves()
            vm=list()
            for i in range(3):
                for j in range(3):
                    if lm[i][j]==1:
                        vm.append((i,j))
            if tempstate.check_terminated() is not None:
                return tempstate.check_terminated()            
            pm=random.choice(vm)            
            tempstate.playMove(pm[0],pm[1])            


    def  search(self,start_state):
        root=node(start_state,None,None)
        for i in range(self.loops):
            cur_node=root
            #selection
            while len(cur_node.children)!=0 and cur_node.isFullyExpanded():
                tnode=cur_node.getBestChild(self.c)
                if tnode is None:
                    break
                cur_node=tnode
                if cur_node.state.check_terminated() is not None:
                    break

            # expansion
            if cur_node.isFullyExpanded()==False and cur_node.state.check_terminated() is None:
                ch=cur_node.expand()
                cur_node=ch
                
            # roll
            result=self.rollout(cur_node.state)
            # backprop (update) 
            cur_node.update(result)
        best_child=max(root.children,key=lambda x:x.N)
        return best_child.prev_move

def GamePlay():
    game=gameState()
    human=1
    ai=2
    mcst_ai=MCTS(c=1.2,loops=1000)
    while True:
        if game.check_terminated() is not None:
            win=game.check_terminated()
            if win==human:
                print("Hooman wins!")
            elif win==ai:
                print("bot rekt you lol...git good bro...L Noob!")
            else:
                print("Draw...no shit...its tic tac toe")
            break
        if game.player==human:
            print(">> play hooman: ")
            while(True):
              print("enter x: ")
              x=int(input())
              print("enter y: ")
              y=int(input())
              if game.playMove(x,y):  
                  break
              else:
                  print("stoopid hooman play again...noob ass move!")
        else:
            print("hmmmmm.....")
            move=mcst_ai.search(game)
            print("I play: ",move)
            game.playMove(move[0],move[1])
        game.print_board()
GamePlay()        




        