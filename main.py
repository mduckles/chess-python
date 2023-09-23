from enum import Enum
import curses
import math
from stockfish import Stockfish

def round_half_up(n):
    return int(n+0.25)


class Game:
    def __init__(self,player1,player2):
        self.board = [[[" ",""]for i in range(8)] for i in range(8)] 
        self.player1 = player1
        self.player2 = player2
        self.gameover = False
        #init screen
        self.screen = curses.initscr()
        #dimensions of window
        if curses.COLS %2 ==0:
            self.width = curses.COLS
        else:
            self.width = curses.COLS-1
        self.height = curses.LINES
        #initialise window
        self.window = curses.newwin(8,17,round_half_up(self.height/2)-4,round_half_up(self.width/2)-8)
        #set up keystrokes and mouse inputes
        self.window.keypad(1)
        self.window.nodelay(False)
        curses.noecho()
        curses.curs_set(0)
        curses.mousemask(1)
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
        #highlight
        curses.init_color(5,921,921,360)
        
        curses.init_pair(3,3,3)
        curses.init_pair(1,3,5)
        curses.init_pair(2,4,5)

        #white dark brown
        curses.init_pair(4,4,1)
        #white light brown
        curses.init_pair(5,4,2)
        #black dark brown
        curses.init_pair(6,3,1)
        #black light brown
        curses.init_pair(7,3,2)
        self.window.attrset(curses.color_pair(3))
        self.screen.bkgdset(" ",curses.color_pair(3))

    def gameloop(self):
        self.pieces_to_board()
        self.board_out()
        while not self.gameover:
            if self.player1.is_turn:
                event = self.window.getch()
                (bx,by) = self.inputs(event)
                for piece in self.player1.pieces:
                    if (bx,by) == (piece.position[0],piece.position[1]) and self.player1.is_turn:
                        possible_moves = piece.possible_moves(self.board) 
                        highlight = possible_moves+[[bx,by]]
                        self.board_out(highlight)
                        self.window.refresh()
                        event2 = self.window.getch()
                        (x,y) = self.inputs(event)
                        if [x,y] in possible_moves:
                            if (x,y) != (-1,-1):
                                self.move_piece(piece,(x,y))
                                self.board_out()
                                self.window.refresh()
                            else:
                                self.board_out()
                                self.window.refresh()
                                continue
                        #changes turn 
                        # self.player1.is_turn =False
                        # self.player2.is_turn = True

            elif self.player2.is_turn:
                pass
            #just incase it isn't anybodys turn for some reason doesn't get stuck in infinite loop
            else:
                break
            
                    
                    
                    
        curses.endwin()

    def move_piece(self,piece,cords):
        self.board[cords[0]][cords[1]] = piece.piece_output
        self.board[piece.position[0]][piece.position[1]] = [" ",""]
        piece.position = [cords[0],cords[1]]

    def pieces_to_board(self):
        for piece in self.player1.pieces+self.player2.pieces:
            self.board[piece.position[0]][piece.position[1]] = piece.piece_output

    def inputs(self,event):
        if event == ord("q"):
            self.gameover = True
        if event == curses.KEY_MOUSE:
            mouse = curses.getmouse()
            if (mouse[2] >=round_half_up(self.height/2)-4 and mouse[2] <=round_half_up(self.height/2)+4) and (mouse[1]>=round_half_up(self.width/2)-8 and mouse[1] <=round_half_up(self.width/2)+8):
                #returns chess cords 
                return (int(int(mouse[1]-self.width/2+8)/2),mouse[2]-int(self.height/2)+4)
        return(-1,-1)

    def board_out(self,*highlight):
        with open("output.txt","a") as f:
            f.write(f"{highlight}\n")
        f.close()
        for (i,row) in enumerate(self.board):
            for (j,square) in enumerate(row):
                if (j+i)%2!=0:
                    self.square_out(square,4,6,j,i)
                    if len(highlight) != 0:
                        if [i,j] in highlight[0]:
                            self.square_out(square,2,1,j,i)
                elif (j+i)%2==0:
                    self.square_out(square,5,7,j,i)
                    if len(highlight) != 0:
                        if [i,j] in highlight[0]:
                            self.square_out(square,2,1,j,i)
                self.window.refresh()

    def square_out(self,square,pair1,pair2,j,i):
        if square[1] == "white":
            self.window.attron(curses.color_pair(pair1))
            self.window.addch(j,2*i,square[0])
            self.window.addch(j,2*i+1," ")
            self.window.attroff(curses.color_pair(pair1))
        elif square[1] == "black" or square[1]=="":
            self.window.attron(curses.color_pair(pair2))
            self.window.addch(j,2*i,square[0])
            self.window.addch(j,2*i+1," ")
            self.window.attroff(curses.color_pair(pair2))


class Piece:
    def __init__(self,piece,color:str,x:int,y:int):
        self.piece_type = piece 
        self.piece_output = [" ",color]   
        if  self.piece_type.value==1: 
            self.piece_output = ["♟",color]
        if self.piece_type.value ==2: 
            self.piece_output = ["♞",color]
        if self.piece_type.value==3:
            self.piece_output = ["♝",color]
        if self.piece_type.value==4:
            self.piece_output = ["♜",color]
        if self.piece_type.value==5:
            self.piece_output = ["♛",color]
        if self.piece_type.value==6:
            self.piece_output = ["♚",color]
        self.color = color
        self.position = [x,y]

    def possible_moves(self,board):
        if  self.piece_type.value==1: 
            return self.pawn_moves(board)
        if self.piece_type.value ==2: 
            return self.knight_moves(board)
        if self.piece_type.value==3:
            return self.bishop_moves(board)
        if self.piece_type.value==4:
            return self.rook_moves(board)
        if self.piece_type.value==5:
            return self.queen_moves(board)
        if self.piece_type.value==6:
            return self.king_moves(board)
        

    def pawn_moves(self,board):
        possible_moves = []
        #capturing
        if self.position[0]==0:
            if board[1][self.position[1]-1][0] != " " and board[1][self.position[1]-1][1] != "white":
                possible_moves.append([1,self.position[1]-1])
        elif self.position[0]==7:
            if board[6][self.position[1]-1][0] !=" " and board[6][self.position[1]-1][1] != "white":
                possible_moves.append([6,self.position[1]-1])
        else:
            if board[self.position[0]-1][self.position[1]-1][1] != "white" and board[self.position[0]-1][self.position[1]-1][0]!=" ":
                possible_moves.append([self.position[0]-1,self.position[1]-1])
            if board[self.position[0]+1][self.position[1]-1][1] != "white" and board[self.position[0]+1][self.position[1]-1][0] != " ":
                possible_moves.append([self.position[0]+1,self.position[1]-1])
        #double move
        if self.position[1] == 6 and board[self.position[0]][self.position[1]-1][0] == " " and board[self.position[0]][self.position[1]-2][0] == " ":
            possible_moves.append([self.position[0],self.position[1]-2])
        if board[self.position[0]][self.position[1]-1][0] == " ":
            possible_moves.append([self.position[0],self.position[1]-1])
        return possible_moves
                
                
    def knight_moves(self,board):
        possible_moves = []
        try:
            if board[self.position[0]-1][self.position[1]-2][1] != "white":
                possible_moves.append([self.position[0]-1,self.position[1]-2])
        except:
            pass
        try:
            if board[self.position[0]-1][self.position[1]+2][1] != "white":
                possible_moves.append([self.position[0]-1,self.position[1]+2])
        except:
            pass
        try:
            if board[self.position[0]+1][self.position[1]-2][1] != "white":
                possible_moves.append([self.position[0]+1,self.position[1]-2])
        except:
            pass
        try:
            if board[self.position[0]+1][self.position[1]+2][1] != "white":
                possible_moves.append([self.position[0]+1,self.position[1]+2])
        except:
            pass
        try:
            if board[self.position[0]-2][self.position[1]-1][1] != "white":
                possible_moves.append([self.position[0]-2,self.position[1]-1])
        except:
            pass
        try:
            if board[self.position[0]-2][self.position[1]+1][1] != "white":
                possible_moves.append([self.position[0]-2,self.position[1]+1])
        except:
            pass
        try:
            if board[self.position[0]+2][self.position[1]-1][1] != "white":
                possible_moves.append([self.position[0]+2,self.position[1]-1])
        except:
            pass
        try:
            if board[self.position[0]+2][self.position[1]+1][1] != "white":
                possible_moves.append([self.position[0]+2,self.position[1]+1])
        except:
            pass
        return possible_moves

    def bishop_moves(self,board):
        possible_moves = []
        #downward
        for i in range(1,7):
            try:
                if board[self.position[0]+i][self.position[1]+i][1] == "":
                    possible_moves.append([self.position[0]+i,self.position[1]+i])
                    
                if board[self.position[0]+i][self.position[1]+i][1] == "black":
                    possible_moves.append([self.position[0]+i,self.position[1]+i])
                    break
                if board[self.position[0]+i][self.position[1]+i][1] == "white":
                    break
            except:
                pass
        for i in range(1,7):
            try:
                if board[self.position[0]-i][self.position[1]+i][1] == "":
                    possible_moves.append([self.position[0]-i,self.position[1]+i])
                    
                if board[self.position[0]-i][self.position[1]+i][1] == "black":
                    possible_moves.append([self.position[0]-i,self.position[1]+i])
                    break
                if board[self.position[0]-i][self.position[1]+i][1] == "white":
                    break
            except:
                pass
        for i in range(1,7):
            try:
                if board[self.position[0]+i][self.position[1]-i][1] == "":
                    possible_moves.append([self.position[0]+i,self.position[1]-i])
                    
                if board[self.position[0]+i][self.position[1]-i][1] == "black":
                    possible_moves.append([self.position[0]+i,self.position[1]-i])
                    break
                if board[self.position[0]+i][self.position[1]-i][1] == "white":
                    break
            except:
                pass
        for i in range(1,7):
            try:
                if board[self.position[0]-i][self.position[1]-i][1] == "":
                    possible_moves.append([self.position[0]-i,self.position[1]-i])
                    
                if board[self.position[0]-i][self.position[1]-i][1] == "black":
                    possible_moves.append([self.position[0]-i,self.position[1]-i])
                    break
                if board[self.position[0]-i][self.position[1]-i][1] == "white":
                    break
            except:
                pass
                
        return possible_moves

    def rook_moves(self,board):
        possible_moves = []
        return possible_moves

    def queen_moves(self,board):
        possible_moves = []
        return possible_moves

    def king_moves(self,board):
        possible_moves = []
        return possible_moves

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
