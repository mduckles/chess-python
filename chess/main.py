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
    def __init__(self,piece,color,x,y):
        self.piece_type = piece
        self.color = color
        self.popsition = [x,y]

    

class Player:
    def __init__(self):
        self.gamestate = Gamestate.InProgress


    
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
