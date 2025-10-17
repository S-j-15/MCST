import math
import random
import tkinter as tk
from tkinter import messagebox
class gameState:
    def __init__(self,board=None,player=1):
        self.board=board
        if self.board is None:
            self.board=[[[0 for i in range(6)],0]for stacks in range(7)]
        self.player=player
    #legalmoves
    def legal_moves(self):
        b=self.board
        lm=list()
        for i in range(7):
            if b[i][1]<6:
                lm.append(i)
        return lm
            
    # clone
    def clone(self):
        return gameState([[[self.board[stacks][0][i] for i in range(6)],self.board[stacks][1]]for stacks in range(7)],self.player)
    # playmove
    def playMove(self,i):
        lm=set(self.legal_moves())
        if i in lm:
            self.board[i][0][self.board[i][1]]=self.player
            self.board[i][1]+=1
            self.player=3-self.player
            return True
        return False            
    # nextstate
    def nextState(self,i):
        cur_state=self.clone()
        lm=set(cur_state.legal_moves())
        if i in lm:
            cur_state.board[i][0][cur_state.board[i][1]]=cur_state.player
            cur_state.board[i][1]+=1
            cur_state.player=3-cur_state.player
            return cur_state
        return None
    # chk terminated
    def check_terminated(self):
        b=self.board
        for col in range(7):
            count_1=0
            count_2=0
            for row in range(6):
                cell=b[col][0][row]
                if cell==1:
                    count_1+=1
                    count_2=0
                elif cell==2:
                    count_2+=1
                    count_1=0
                else:
                    count_1=0
                    count_2=0
                if count_1>=4:
                    return 1
                if count_2>=4:
                    return 2
        for row in range(6):
            count_1=0
            count_2=0
            for col in range(7):
                cell = b[col][0][row]
                if cell==1:
                    count_1+=1
                    count_2=0
                elif cell==2:
                    count_2+=1
                    count_1=0
                else:
                    count_1=0
                    count_2=0
                if count_1>=4:
                    return 1
                if count_2>=4:
                    return 2
        for col in range(0,4):
            for row in range(0,3):
                a=b[col][0][row]
                if a != 0:
                    if b[col+1][0][row+1]==a and b[col+2][0][row+2]==a and b[col+3][0][row+3]==a:
                        return a
        for col in range(3,7):
            for row in range(0,3):
                a = b[col][0][row]
                if a != 0:
                    if b[col-1][0][row+1]==a and b[col-2][0][row+2]==a and b[col-3][0][row+3]==a:
                        return a
        if all(self.board[c][1]>=6 for c in range(7)):
            return 0
        return None
class node:
    #init
    def __init__(self,state,parent=None,prev_move=None):
        self.state=state
        self.parent=parent
        self.children=[]
        self.prev_move=prev_move
        self.next_moves=self.state.legal_moves()
        self.N=0
        self.W=0.0
    # getBestChild
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
    # expand
    def expand(self):
        if len(self.next_moves)==0:
            return None
        nxtmv=self.next_moves.pop()
        newstate=(self.state.clone()).nextState(nxtmv)
        
        parent=self
        chnode=node(newstate,parent,nxtmv)
        self.children.append(chnode)
        return chnode
    # isfullyexpanded
    def isFullyExpanded(self):
        return len(self.next_moves)==0
    # update
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
    #init
    def __init__(self,c=1.2,loops=1000):
        self.c=c
        self.loops=loops
    # rollout
    def rollout(self,state):
        tempstate=state.clone()
        while True:
            lm=tempstate.legal_moves()
            if tempstate.check_terminated() is not None:
                return tempstate.check_terminated()            
            pm=random.choice(lm)            
            tempstate.playMove(pm)
    # search 
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

CELL_SIZE = 80
ROWS = 6
COLS = 7
HUMAN = 1
AI = 2

class Connect4GUI:
    def __init__(self, master):
        self.master = master
        master.title("Connect-4 MCTS")
        
        self.state = gameState()
        self.mcts_ai = MCTS(c=1.2, loops=2000)  # adjust loops for speed
        
        self.canvas = tk.Canvas(master, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg='blue')
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.human_click)
        self.draw_board()
        self.human_turn = True

    def draw_board(self):
        self.canvas.delete("all")
        for c in range(COLS):
            for r in range(ROWS):
                x0 = c*CELL_SIZE
                y0 = (ROWS-r-1)*CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill='blue', outline='black')
                
                token = self.state.board[c][0][r]
                if token == HUMAN:
                    color = 'red'
                elif token == AI:
                    color = 'yellow'
                else:
                    color = 'white'
                self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=color)
        self.master.update()

    def human_click(self, event):
        if not self.human_turn:
            return
        col = event.x // CELL_SIZE
        if col not in self.state.legal_moves():
            return
        self.state.playMove(col)
        self.draw_board()
        winner = self.state.check_terminated()
        if winner:
            self.game_over(winner)
            return
        self.human_turn = False
        self.master.after(300, self.ai_move)

    def ai_move(self):
        move = self.mcts_ai.search(self.state)
        if move is not None:
            self.state.playMove(move)
            self.draw_board()
        winner = self.state.check_terminated()
        if winner:
            self.game_over(winner)
            return
        self.human_turn = True

    def game_over(self, winner):
        if winner == HUMAN:
            messagebox.showinfo("Game Over", "You Win!")
        elif winner == AI:
            messagebox.showinfo("Game Over", "AI Wins!")
        else:
            messagebox.showinfo("Game Over", "Draw!")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = Connect4GUI(root)
    root.mainloop()       