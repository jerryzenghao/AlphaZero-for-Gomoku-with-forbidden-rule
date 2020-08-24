import numpy as np
import copy
from operator import itemgetter

def rollout_policy_fn(board):
    """a coarse, fast version of policy_fn used in the rollout phase."""
    # rollout randomly
    action_probs = np.random.rand(len(board.availables))
    return zip(board.availables, action_probs)


def policy_value_fn(board):
    """a function that takes in a state and outputs a list of (action, probability)
    tuples and a score for the state"""
    # return uniform probabilities and 0 score for pure MCTS
    action_probs = np.ones(len(board.availables))/len(board.availables)
    return zip(board.availables, action_probs), 0

class PureMCTSNode:
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
                self._children[action] = PureMCTSNode(self, probs)

    def backup(self, value):
        if self._parent:
            self._parent.backup(-value)
        self.update(value)

    def update(self, value):
        self._N += 1.0
        self._Q += (value - self._Q)/self._N
        
    def get_value(self, c_puct):
        self._U = (c_puct * self._P * np.sqrt(self._parent._N) / (1 + self._N))
        return self._Q + self._U+np.random.rand()*0.01

    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None
    


class PureMCTS:
    def __init__(self, f_theta, c_puct=5, n_playout=10000):
        self._root = PureMCTSNode(None, 1.0)
        self._f = f_theta # (p, v) = f_theta(s)
        self._c_puct = c_puct
        self._n_playout = n_playout
    
    def _evaluate_rollout(self, state, limit=1000):
        """Use the rollout policy to play until the end of the game,
        returning +1 if the current player wins, -1 if the opponent wins,
        and 0 if it is a tie.
        """
        player = state.turn
        for _ in range(limit):
            result = state.get_result()
            if result:
                break
            action_probs = rollout_policy_fn(state)
            max_action = max(action_probs, key=itemgetter(1))[0]
            state.do_move(max_action)
        if result == 0:  # tie
            return 0
        else:
            return 1 if result == player else -1

    def _playout(self, state):
        '''run single playout '''
        node = self._root
        action = None
        while True:
            if node.is_leaf():
                break
            action, node = node.select(self._c_puct)
            state.do_move(action)
        
        action_probs, _ = self._f(state)
        if action != None:
            result = state.get_result()
        if action == None or result == 0: # contiuous
            node.expand(action_probs)
        leaf_value = self._evaluate_rollout(state)
        
        node.backup(-leaf_value)

    def simulation(self, state, temp):
        for _ in range(self._n_playout):
        #for _ in range(1):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
        return max(self._root._children.items(), key=lambda act_node: act_node[1]._N)[0]
    
    def update_tree(self, action):
        if action in self._root._children:
            self._root = self._root._children[action]
            self._root._parent = None
        else:
            self._root = PureMCTSNode(None, 1.0)


class PureMCTSPlayer(object):
    """Player based on MCTS"""

    def __init__(self, policy_value_function = policy_value_fn, c_puct=5, n_playout=2000):
        self.mcts = PureMCTS(policy_value_function, c_puct, n_playout)

    def set_player(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_tree(-1)

    def get_action(self, board, temp=0.1, return_prob = 0):
        sensible_moves = board.availables
        #move_probs = np.zeros(board.W*board.H)
        if len(sensible_moves) > 0:
            move = self.mcts.simulation(board, temp)
            # reset the root node
            self.mcts.update_tree(-1)
            return move
        else:
            print("WARNING: the board is full")