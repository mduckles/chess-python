from enum import Enum
import curses
import math
from pystockfish import *
# set engine depth 
deep = Engine(depth=10)

#letters for the board
letters = ['a','b','c','d','e','f','g','h']

#round a number like in normal math and physics rounding
def round_half_up(n):
    return int(n+0.25)


class Game:
    '''Game class storing all game data with game methods'''
    def __init__(self,player1,player2):
        '''takes to players as input along with self and setting up board colors mousemasks for the game'''
        #moves that have been played 
        self.moves = []
        #the board being played on
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
        '''Game loop '''
        #out puts board with pieces on it
        self.pieces_to_board()
        self.board_out()
        # what piece was clicked 
        is_piece_clicked = False
        piece_clicked = self.player1.pieces[0]       
        # to check for win conditions
        count =0
        player1_won = False
        player2_won = False
        while not self.gameover:
            #player1's turn
            if self.player1.is_turn:
                #if a piece has not been selected
                if not is_piece_clicked:
                    #mouse clicks and q input for quiting
                    event = self.window.getch()
                    (bx,by) = self.inputs(event)
                    for piece in self.player1.pieces:
                        #highliht piece clicked if a piece was clicked
                        if (bx,by) == (piece.position[0],piece.position[1]):
                            #showing highlight of possible moves a piece can make
                            possible_moves = piece.possible_moves(self.board) 
                            highlight = possible_moves+[[bx,by]]
                            self.board_out(highlight)
                            self.window.refresh()
                            is_piece_clicked = True
                            piece_clicked = piece
                #if a piece has been selected
                if is_piece_clicked:
                    possible_moves = piece_clicked.possible_moves(self.board) 
                    #get a second click
                    event2 = self.window.getch()
                    (x,y) = self.inputs(event)
                    #if the click is a possible move
                    if [x,y] in possible_moves:
                        if (x,y) != (-1,-1):
                            #delet piece if a piece is caputured
                            for (i,piece2) in enumerate(self.player2.pieces):
                                if [piece2.position[0],piece2.position[1]] == [int(x),int(y)]:
                                    self.player2.pieces.pop(i)
                                    break
                            #move piece and switch turn
                            self.move_piece(piece_clicked,(x,y))
                            self.board_out()
                            self.window.refresh()
                            is_piece_clicked = False
                            self.player1.is_turn =False
                            self.player2.is_turn = True
                        else:
                            #clear highlight's 
                            self.board_out()
                            self.window.refresh()
                            is_piece_clicked = False
                            continue
                    #changes turn 
                    piece_clicked = 0
                    is_piece_clicked = False
            #player 2's turn
            elif self.player2.is_turn:
                #sets position for stockfish
                deep.setposition(self.moves)
                #if there are no legal moves for stockfish you win(you will only win if you cheat)
                try:
                    move = deep.bestmove()["move"]
                except:
                    player1_won = True
                    self.gameover = True
                #spilt letter number notation to number number notation
                xi = str([i for (i,l) in enumerate(letters) if l == move[0]])[1]
                yi = str(8-int(move[1]))
                xf = str([i for (i,l) in enumerate(letters) if l == move[2]])[1]
                yf = str(8-int(move[3]))
                #castle for stockfish
                if move == "e8g8":
                    for piece in self.player2.pieces:
                        if piece.position == [7,0]:
                            self.move_piece(piece,[5,0],True)
                        if piece.position == [4,0]:
                            self.move_piece(piece,[int(xf),int(yf)])
                        self.board_out()
                        self.window.refresh()
                        self.player1.is_turn =True
                        self.player2.is_turn =False 
                #other castle for stocfish 
                elif move == "e8c8":
                    for piece in self.player2.pieces:
                        if piece.position == [0,0]:
                            self.move_piece(piece,[3,0],True)
                        if piece.position == [4,0]:
                            self.move_piece(piece,[int(xf),int(yf)])
                        self.board_out()
                        self.window.refresh()
                        self.player1.is_turn =True
                        self.player2.is_turn =False 
                #other move's
                else:
                    for piece in self.player2.pieces:
                        if [piece.position[0],piece.position[1]] == [int(xi),int(yi)]:
                            #delete captured pieces
                            for (i,piece2) in enumerate(self.player1.pieces):
                                if [piece2.position[0],piece2.position[1]] == [int(xf),int(yf)]:
                                    self.player1.pieces.pop(i)
                                    break
                            #move pieces
                            self.move_piece(piece,[int(xf),int(yf)])
                            self.board_out()
                            self.window.refresh()
                            self.player1.is_turn =True
                            self.player2.is_turn =False 
                count+=1
                #player 1 has no legal moves or made a iligal move and the king was captured
                if count >= 1000:
                    player2_won = True
                    self.gameover = True

            #just incase it isn't anybodys turn for some reason doesn't get stuck in infinite loop
            else:
                break
                    
        #clears window
        curses.endwin()
        #win and lose messages
        if player2_won:
            print("You lost your bad at the game(if you made an illigel move the abitor is a bit angry so you lose)")
        if player1_won:
            print("You won which meant you cheated. I know where you live in a non creepy way")

    def move_piece(self,piece,cords,*castle):
        '''moves pieces'''
        if not castle:
            #adds to the board position
            self.moves.append(f'{letters[piece.position[0]]}{8-piece.position[1]}{letters[cords[0]]}{8-cords[1]}')
        #moves peice
        self.board[cords[0]][cords[1]] = piece.piece_output
        self.board[piece.position[0]][piece.position[1]] = [" ",""]
        piece.position = [cords[0],cords[1]]

    def pieces_to_board(self):
        '''put's pieces on the board'''
        for piece in self.player1.pieces+self.player2.pieces:
            self.board[piece.position[0]][piece.position[1]] = piece.piece_output

    def inputs(self,event):
        '''gets inputs from mouse and q'''
        if event == ord("q"):
            self.gameover = True
        if event == curses.KEY_MOUSE:
            mouse = curses.getmouse()
            #if mouse is in  the board
            if (mouse[2] >=round_half_up(self.height/2)-4 and mouse[2] <=round_half_up(self.height/2)+4) and (mouse[1]>=round_half_up(self.width/2)-8 and mouse[1] <=round_half_up(self.width/2)+8):
                #returns chess cords 
                return (int(int(mouse[1]-self.width/2+8)/2),mouse[2]-int(self.height/2)+4)
        return(-1,-1)

    def board_out(self,*highlight):
        '''outputs the board'''
        for (i,row) in enumerate(self.board):
            for (j,square) in enumerate(row):
                #light squares
                if (j+i)%2==0:
                    self.square_out(square,4,6,j,i)
                    if len(highlight) != 0:
                        if [i,j] in highlight[0]:
                            self.square_out(square,2,1,j,i)
                #dark squares
                elif (j+i)%2!=0:
                    self.square_out(square,5,7,j,i)
                    if len(highlight) != 0:
                        if [i,j] in highlight[0]:
                            self.square_out(square,2,1,j,i)
                self.window.refresh()

    def square_out(self,square,pair1,pair2,j,i):
        '''output's squares with colores'''
        #light squares
        if square[1] == "white":
            self.window.attron(curses.color_pair(pair1))
            self.window.addch(j,2*i,square[0])
            self.window.addch(j,2*i+1," ")
            self.window.attroff(curses.color_pair(pair1))
        #dark squares
        elif square[1] == "black" or square[1]=="":
            self.window.attron(curses.color_pair(pair2))
            self.window.addch(j,2*i,square[0])
            self.window.addch(j,2*i+1," ")
            self.window.attroff(curses.color_pair(pair2))


class Piece:
    def __init__(self,piece,color:str,x:int,y:int):
        '''takes the piece color and poistion'''
        self.piece_type = piece 
        self.piece_output = [" ",color]   
        #assigns charaters to pieces
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
        '''runs the correct function for the right piece for possilbe moves'''
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
        '''possible moves for pawns'''
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
        '''possible moves for knights'''
        possible_moves = []
        #all eight squares
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
        '''possible bishops moves'''
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
        '''possilble rooks moves'''
        possible_moves = []
        for i in range(1,7):
            try:
                if board[self.position[0]+i][self.position[1]][1] == "":
                    possible_moves.append([self.position[0]+i,self.position[1]])
                    
                if board[self.position[0]+i][self.position[1]][1] == "black":
                    possible_moves.append([self.position[0]+i,self.position[1]])
                    break
                if board[self.position[0]+i][self.position[1]][1] == "white":
                    break
            except:
                pass
        for i in range(1,7):
            try:
                if board[self.position[0]-i][self.position[1]][1] == "":
                    possible_moves.append([self.position[0]-i,self.position[1]])
                    
                if board[self.position[0]-i][self.position[1]][1] == "black":
                    possible_moves.append([self.position[0]-i,self.position[1]])
                    break
                if board[self.position[0]-i][self.position[1]][1] == "white":
                    break
            except:
                pass
        for i in range(1,7):
            try:
                if board[self.position[0]][self.position[1]-i][1] == "":
                    possible_moves.append([self.position[0],self.position[1]-i])
                    
                if board[self.position[0]][self.position[1]-i][1] == "black":
                    possible_moves.append([self.position[0],self.position[1]-i])
                    break
                if board[self.position[0]][self.position[1]-i][1] == "white":
                    break
            except:
                pass
        for i in range(1,7):
            try:
                if board[self.position[0]][self.position[1]+i][1] == "":
                    possible_moves.append([self.position[0],self.position[1]+i])
                   
                if board[self.position[0]][self.position[1]+i][1] == "black":
                    possible_moves.append([self.position[0],self.position[1]+i])
                    break
                if board[self.position[0]][self.position[1]+i][1] == "white":
                    break
            except:
                pass
        return possible_moves

    def queen_moves(self,board):
        '''possible queen moves'''
        # juse both rook and bishop moves
        possible_moves = self.rook_moves(board) + self.bishop_moves(board)
        return possible_moves

    def king_moves(self,board):
        '''possilbe king moves'''
        possible_moves = []
        try:
            if board[self.position[0]][self.position[1]-1][1] != "white":
                possible_moves.append([self.position[0],self.position[1]-1])
        except:
            pass
        try:
            if board[self.position[0]-1][self.position[1]-1][1] != "white":
                possible_moves.append([self.position[0]-1,self.position[1]-1])
        except:
            pass
        
        try:
            if board[self.position[0]+1][self.position[1]-1][1] != "white":
                possible_moves.append([self.position[0]+1,self.position[1]-1])
        except:
            pass
        try:
            if board[self.position[0]+1][self.position[1]][1] != "white":
                possible_moves.append([self.position[0]+1,self.position[1]])
        except:
            pass
        try:
            if board[self.position[0]-1][self.position[1]][1] != "white":
                possible_moves.append([self.position[0]-1,self.position[1]])
        except:
            pass
        try:
            if board[self.position[0]][self.position[1]+1][1] != "white":
                possible_moves.append([self.position[0],self.position[1]+1])
        except:
            pass
        try:
            if board[self.position[0]-1][self.position[1]+1][1] != "white":
                possible_moves.append([self.position[0]-1,self.position[1]+1])
        except:
            pass
        try:
            if board[self.position[0]+1][self.position[1]+1][1] != "white":
                possible_moves.append([self.position[0]+1,self.position[1]+1])
        except:
            pass
        return possible_moves

class Player:
    def __init__(self,turn:bool,pieces):
        '''given it's turn and it pieces'''
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
    '''main function for set up'''
    #player 1's peices
    player1_peices = [
                      Piece(PieceType.Rook,"white",0,7),
                      Piece(PieceType.Knight,"white",1,7),
                      Piece(PieceType.Bishop,"white",2,7),
                      Piece(PieceType.King,"white",4,7),
                      Piece(PieceType.Queen,"white",3,7),
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

    #player 2's peices
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

    #set up both players
    player1 = Player(True,player1_peices)
    player2 = Player(False,player2_peices)
    #set up game
    game = Game(player1,player2)
    #runs game
    game.gameloop()
    

if __name__ == "__main__":
    main()
