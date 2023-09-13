from enum import Enum


class Game:
    def __init__(self):
        self.board = [[" t "for i in range(8)] for i in range(8)] 
        self.gameover = False

    def gameloop(self):
        while not self.gameover:
            pass

    def board_out(self):
        for row in self.board:
            for square in row:
                print(square,end='')
            print("\n")

        
    

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
