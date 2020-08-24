import numpy as np
import copy
import warnings
warnings.filterwarnings("ignore")
class MCTSNode:
    def __init__(self, parent, prior):
        self._parent = parent
        self._children = {} # a map from action to MCTSNode
        self._Q = 0.0
        self._N = 0.0
        self._U = 0.0
        self._P = prior # the probability of choosing this node from its parent

    def select(self, c_puct):
        return max(self._children.items(), key=lambda node: node[1].get_value(c_puct))

    def expand(self, action_probs):
        for action, probs in action_probs:
            if action not in self._children:
                self._children[action] = MCTSNode(self, probs)

    def backup(self, value):
        if self._parent:
            self._parent.backup(-value)
        self.update(value)

    def update(self, value):
        self._N += 1.0
        self._Q += (value - self._Q)/self._N
        
    def get_value(self, c_puct):
        self._U = (c_puct * self._P * np.sqrt(self._parent._N) / (1 + self._N))
        return self._Q + self._U

    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None
    


class MCTS:
    def __init__(self, f_theta, c_puct=5, n_playout=10000):
        self._root = MCTSNode(None, 1.0)
        self._f = f_theta # (p, v) = f_theta(s)
        self._c_puct = c_puct
        self._n_playout = n_playout

    def _playout(self, state):
        '''run single playout '''
        node = self._root
        action = None
        while True:
            if node.is_leaf():
                break
            action, node = node.select(self._c_puct)
            state.do_move(action)
        
        action_probs, leaf_value = self._f(state)
        if action != None:
            result = state.get_result()
        if action == None or result == 0: # contiuous
            node.expand(action_probs)
        else:
            if result == 3:
                leaf_value = 0.0
            else:
                leaf_value = 1.0 if result == state.turn else -1.0 # At the current's view, if the game is end, then the player is lose.

        node.backup(-leaf_value)

    def simulation(self, state, temp):
        for _ in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
        action_N = [(action, node._N) for action, node in self._root._children.items()]
        actions, N  = zip(*action_N)
        N_temp = np.array(N)**(1/temp)
        sum_N_temp = np.sum(N_temp)+1e-10
        act_probs = N_temp/sum_N_temp
        
        return actions, act_probs
    
    def update_tree(self, action):
        if action in self._root._children:
            self._root = self._root._children[action]
            self._root._parent = None
        else:
            self._root = MCTSNode(None, 1.0)


class MCTSPlayer(object):
    """Player based on MCTS"""

    def __init__(self, policy_value_function, c_puct=5, n_playout=2000, is_selfplay=0):
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self._is_selfplay = is_selfplay

    def set_player(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_tree(-1)

    def get_action(self, board, temp=0.1, return_prob = 0):
        sensible_moves = board.availables
        #move_probs = np.zeros(board.W*board.H)
        if len(sensible_moves) > 0:
            acts, probs = self.mcts.simulation(board, temp)
            #move_probs[list(acts)] = probs
            if self._is_selfplay:
                choice = np.random.choice(
                    len(acts),
                    p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )
                move = acts[choice]
                self.mcts.update_tree(move)
            else:
                choice = np.random.choice(len(acts), p=probs)
                move = acts[choice] 
                # reset the root node
                self.mcts.update_tree(-1)

            if return_prob:
                move_probs = np.zeros((board.W,board.H))
                for a,p in zip(acts,probs):
                    move_probs[a] = p

                return move, move_probs
            else:
                return move
        else:
            print("WARNING: the board is full")