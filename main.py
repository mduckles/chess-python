from enum import Enum
import curses


class Game:
    def __init__(self,player1,player2):
        self.board = [[["  ","black"]for i in range(8)] for i in range(8)] 
        self.player1 = player1
        self.player2 = player2
        self.gameover = False
        #initialise window
        self.window = curses.initscr()
        #set up keystrokes and mouse inputes
        self.window.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        curses.mousemask(1)
        #dimensions of window
        self.width = curses.COLS
        self.height = curses.LINES
        #starts colors 
        curses.start_color()
        # dark brown 
        curses.init_color(1,770,450,90)
        # light brown
        curses.init_color(2,530,230,30)
        #black
        curses.init_color(3,0,0,0)
        #white
        curses.init_color(4,1000,1000,1000)
        #black
        curses.init_color(3,1,1,1)
        
        curses.init_pair(1,1,2)
        curses.init_pair(2,2,1)
        curses.init_pair(3,3,3)

        #white dark brown
        curses.init_pair(4,4,1)
        #white light brown
        curses.init_pair(5,4,2)
        #black dark brown
        curses.init_pair(6,3,1)
        #black light brown
        curses.init_pair(7,3,2)
        self.window.attrset(curses.color_pair(3))

    def gameloop(self):
        self.pieces_to_board()
        self.board_out()
        while not self.gameover:
            event = self.window.getch()
            (bx,by) = self.inputs(event)
            for piece in self.player1.pieces + self.player2.pieces:
                with open ("output.txt","a") as f:
                    f.write(f"({bx},{by})({piece.position[0]},{piece.position[1]})")
                f.close
                if (bx,by) == (piece.position[0],piece.position[1]):
                    self.gameover = True
                    
        curses.endwin()

    def pieces_to_board(self):
        for piece in self.player1.pieces+self.player2.pieces:
            self.board[piece.position[0]][piece.position[1]] = piece.piece_output

    def inputs(self,event):
        if event == ord("q"):
            self.gameover = True
        if event == curses.KEY_MOUSE:
            mouse = curses.getmouse()
            if (mouse[2] >=round(self.height/2)-4 and mouse[2] <=round(self.height/2)+4) and (mouse[1]>=round(self.width/2)-8 and mouse[1] <=round(self.width/2)+8):
                #returns chess cords 
                return (round((mouse[1]-round(self.width/2)+8)/2),mouse[2]-round(self.height/2)+4)
        return(-1,-1)

    def board_out(self):
        for (i,row) in enumerate(self.board):
            for (j,square) in enumerate(row):
                if (j+i)%2!=0:
                    if square[1]== "white":
                        self.window.attron(curses.color_pair(4))
                        self.window.addstr(j+round(self.height/2)-4,2*i+round(self.width/2)-8,square[0])
                        self.window.attroff(curses.color_pair(4))
                    elif square[1] == "black":
                        self.window.attron(curses.color_pair(6))
                        self.window.addstr(j+round(self.height/2)-4,2*i+round(self.width/2)-8,square[0])
                        self.window.attroff(curses.color_pair(6))
                elif (j+i)%2==0:
                    if square[1] == "white":
                        self.window.attron(curses.color_pair(5))
                        self.window.addstr(j+round(self.height/2)-4,2*i+round(self.width/2)-8,square[0])
                        self.window.attroff(curses.color_pair(5))
                    elif square[1] == "black":
                        self.window.attron(curses.color_pair(7))
                        self.window.addstr(j+round(self.height/2)-4,2*i+round(self.width/2)-8,square[0])
                        self.window.attroff(curses.color_pair(7))
                self.window.refresh()

class Piece:
    def __init__(self,piece,color:str,x:int,y:int):
        self.piece_type = piece 
        self.piece_output = ["  ",color]   
        if  self.piece_type.value==1: 
            self.piece_output = ["♟ ",color]
        if self.piece_type.value ==2: 
            self.piece_output = ["♞ ",color]
        if self.piece_type.value==3:
            self.piece_output = ["♝ ",color]
        if self.piece_type.value==4:
            self.piece_output = ["♜ ",color]
        if self.piece_type.value==5:
            self.piece_output = ["♛ ",color]
        if self.piece_type.value==6:
            self.piece_output = ["♚ ",color]
        self.color = color
        self.position = [x,y]
                

class Player:
    def __init__(self,turn:bool,pieces):
        self.gamestate = Gamestate.InProgress
        self.is_turn=turn
        self.pieces = pieces

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
    with open("output.txt","w") as f:
        f.write("")
    f.close()
    player1_peices = [
                      Piece(PieceType.Rook,"white",0,7),
                      Piece(PieceType.Knight,"white",1,7),
                      Piece(PieceType.Bishop,"white",2,7),
                      Piece(PieceType.King,"white",3,7),
                      Piece(PieceType.Queen,"white",4,7),
                      Piece(PieceType.Bishop,"white",5,7),
                      Piece(PieceType.Knight,"white",6,7),
                      Piece(PieceType.Rook,"white",7,7),
                      Piece(PieceType.Pawn,"white",0,6),
                      Piece(PieceType.Pawn,"white",1,6),
                      Piece(PieceType.Pawn,"white",2,6),
                      Piece(PieceType.Pawn,"white",3,6), 
                      Piece(PieceType.Pawn,"white",4,6), 
                      Piece(PieceType.Pawn,"white",5,6), 
                      Piece(PieceType.Pawn,"white",6,6), 
                      Piece(PieceType.Pawn,"white",7,6), 
                          ]

    player2_peices = [
                      Piece(PieceType.Rook,"black",0,0),
                      Piece(PieceType.Knight,"black",1,0),
                      Piece(PieceType.Bishop,"black",2,0),
                      Piece(PieceType.Queen,"black",3,0),
                      Piece(PieceType.King,"black",4,0),
                      Piece(PieceType.Bishop,"black",5,0),
                      Piece(PieceType.Knight,"black",6,0),
                      Piece(PieceType.Rook,"black",7,0),
                      Piece(PieceType.Pawn,"black",0,1),
                      Piece(PieceType.Pawn,"black",1,1),
                      Piece(PieceType.Pawn,"black",2,1),
                      Piece(PieceType.Pawn,"black",3,1), 
                      Piece(PieceType.Pawn,"black",4,1), 
                      Piece(PieceType.Pawn,"black",5,1), 
                      Piece(PieceType.Pawn,"black",6,1), 
                      Piece(PieceType.Pawn,"black",7,1), 
            ]

    player1 = Player(True,player1_peices)
    player2 = Player(False,player2_peices)
    game = Game(player1,player2)
    game.gameloop()
    

if __name__ == "__main__":
    main()
