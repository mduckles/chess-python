from enum import Enum


class Game:
    def __init__(self):
        self.board = [["  "for i in range(8)] for i in range(8)] 
        self.gameover = False

    def gameloop(self):
        while not self.gameover:
            pass

    def board_out(self):
        print("\033[J")
        print("\033[38;5;9")
        for (i,row) in enumerate(self.board):
            for (j,square) in enumerate(row):
                if (j+i)%2 !=0:
                    print(f"\033[48;5;232m {square}",end='\033[0m')
                if (j+i)%2 ==0:
                    print(f"\033[48;5;130m {square}",end='\033[0m')
            print("")

        
    

class Piece:
    def __init__(self,piece:PieceType,color:str,x:int,y:int):
        self.piece_type = piece 
        self.color = color
        self.popsition = [x,y]
    def piece_out(self):
        black = "\033[38;5;237m]"
        white = "\033[38;5;15m]"
        output = ""
        if color == "black":
            match self.piece_type.value:
                case 1:
                    output = black + "♟"
                case 2:
                    output = black + "♞"
                case 3:
                    output = black + "♝"
                case 4:
                    output = black + "♜"
                case 5:
                    output = black + "♛"
                case 6:
                    output = black + "♚"

        elif color == "white":
            match self.piece_type.value:
                case 1:
                    output= white + "♙"
                case 2:
                    output = white + "♘"
                case 3:
                    output = white + "♗"
                case 4:
                    output = white + "♖"
                case 5:
                    output = white + "♕"
                case 6:
                    output = white + "♔"
        return output
                


    

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
    game = Game()
    game.board_out()
    

if __name__ == "__main__":
    main()
