from PyQt5.QtWidgets import QApplication
from window import GomokuWindow
from gomoku import *
import sys
from gomoku import *
from human_player import HumanPlayer
from policy_value_net import *
from mcts import *
from mcts_pure import *

mode = 1 # 0: human vs human; 1: human vs AI
H = 8
W = 8
temp = 0.1
#player1 = HumanPlayer()  # human player
print("Loading model size=",(H,W))
f_theta = PolicyValueNet(H,W,model_file='./model/model88.model').policy_value_fn
print("Finished loading.")
player2 = MCTSPlayer(f_theta,c_puct=5, n_playout=1000)   # MCTSPlayer
player1 = MCTSPlayer(f_theta,c_puct=5, n_playout=1000)   
app = QApplication(sys.argv)
# set mode = 0: human vs human, mode = 1: huamn vs AI.
ex = GomokuWindow((H,W),player1=player1, player2 = player2, mode = mode)
ex.show()
sys.exit(app.exec_())