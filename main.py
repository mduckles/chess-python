from enum import Enum
import curses


class Game:
    def __init__(self,player1,player2):
        self.board = [[["  ","black"]for i in range(8)] for i in range(8)] 
        self.player1 = player1
        self.player2 = player2
        self.gameover = False
        self.window = curses.initscr()
        self.window.keypad(1)
        curses.curs_set(0)
        curses.mousemask(1)
        self.width = curses.COLS
        self.height = curses.LINES
        curses.start_color()
        curses.init_color(1,770,450,90)
        curses.init_color(2,530,230,30)
        curses.init_color(3,1,1,1)
        curses.init_pair(1,1,2)
        curses.init_pair(2,2,1)
        curses.init_pair(3,3,3)
        self.window.attrset(curses.color_pair(3))

    def gameloop(self):
        self.board_out()
        while not self.gameover:
            event = self.window.getch()
            self.inputs(event)
        curses.endwin()

    def inputs(self,event):
        if event == ord("q"):
            self.gameover = True
        if event == curses.KEY_MOUSE:
            mouse = curses.getmouse()
            if (mouse[2] >=round(self.height/2)-4 and mouse[2] <=round(self.height/2)+4) and (mouse[1]>=round(self.width/2)-8 and mouse[1] <=round(self.width/2)+8):
                self.gameover = True
                



    def board_out(self):
        for (i,row) in enumerate(self.board):
            for (j,square) in enumerate(row):
                if (j+i)%2!=0:
                    self.window.attron(curses.color_pair(1))
                    self.window.addstr(j+round(self.height/2)-4,2*i+round(self.width/2)-8,square[0])
                    self.window.attroff(curses.color_pair(1))
                elif (j+i)%2==0:
                    self.window.attron(curses.color_pair(2))
                    self.window.addstr(j+round(self.height/2)-4,2*i+round(self.width/2)-8,square[0])
                    self.window.attroff(curses.color_pair(2))
                self.window.refresh()

class Piece:
    def __init__(self,piece,color:str,x:int,y:int):
        self.piece_type = piece 
        self.color = color
        self.popsition = [x,y]
                

class Player:
    def __init__(self,turn:bool):
        self.gamestate = Gamestate.InProgress
        self.is_turn=turn

class PieceType(Enum):
    Pawn=1 
    Knight=2 
    Bishop=3 
    Rook=4
    Queen=5
    King=6
    
class Gamestate(Enum):
    Win =1
    Loss=2
    Draw=3
    InProgress=4


def main():
    player1 = Player(True)
    player2 = Player(False)
    game = Game(player1,player2)
    game.gameloop()
    

if __name__ == "__main__":
    main()
