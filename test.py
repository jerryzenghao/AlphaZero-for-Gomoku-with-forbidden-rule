from gomoku import *
from human_player import HumanPlayer
from policy_value_net import *
from mcts import *
from mcts_pure import *
if __name__ == "__main__":
    
    H = 10
    W = 10
    temp = 0.1
    board = GomokuBoard((H,W))
    #player1 = HumanPlayer()  # human player
    print("Loading model size=",(H,W))
    f_theta = PolicyValueNet(H,W,model_file='./model/model1010.model').policy_value_fn
    print("Finished loading.")
   # player2 = MCTSPlayer(f_theta,c_puct=5, n_playout=800)   # MCTSPlayer
    player1 = MCTSPlayer(f_theta,c_puct=5, n_playout=400)
    player2 = PureMCTSPlayer(c_puct=5, n_playout=2000)  # PureMCTSPlayer
   # player2 = PureMCTSPlayer(c_puct=5, n_playout=800)
    turn = player1
    
    print("Start play")
    result = 0
    while True:
        move = turn.get_action(board,temp)
        board.do_move(move)
        print(board.chessboard)
        result= board.get_result()
        if result == 0:
            turn = player2 if turn == player1 else player1
        else:
            break
    
    print("The winner is player",result)
        