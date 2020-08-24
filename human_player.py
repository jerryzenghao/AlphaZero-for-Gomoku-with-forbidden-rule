# -*- coding: utf-8 -*-
class HumanPlayer(object):
    """
    human player
    """

    def __init__(self):
        self.player = None
        self.ui = 0 # 1 show 
        self.uimove = None

   # def set_player(self, p):
   #     self.player = p

    def get_action(self, board):
        availables = board.availables
        if self.ui==0:
            while True:
                try:
                    move = input("Human Player input move:")
                    move = eval(move)
                    if move not in availables:
                        print("You can't move here.")
                    else:
                        break
                except:
                    pass
        else:
            pass
        return move
        
