# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import math

import numpy as np
from scipy.special import softmax
EPS = 1e-8

log = logging.getLogger(__name__)


class MCTS():
    """
    This class handles the MCTS tree.
    """

    def __init__(self, game, nnet, args, player=1):
        self.game = game
        self.player = player
        self.nnet = nnet
        self.args = args
        self.Qsa = {}  # stores Q values for s,a (as defined in the paper)
        self.Nsa = {}  # stores #times edge s,a was visited
        self.Ns = {}  # stores #times board s was visited
        self.Ps = {}  # stores initial policy (returned by neural net)

        self.Es = {}  # stores game.getGameEnded ended for board s
        self.Vs = {}  # stores game.getValidMoves for board s
        self.modelCall = 0

    def getActionProb(self, canonicalBoard, multi_sol=0, temp=1, step=0):
        """
        This function performs numMCTSSims simulations of MCTS starting from
        canonicalBoard.

        Returns:
            probs: a policy vector where the probability of the ith action is
                   proportional to Nsa[(s,a)]**(1./temp)
        """
        for i in range(self.args.numMCTSSims):
            if self.player == 2:
                self.search(canonicalBoard)
            elif self.player == 1:
                self.searchSinglePlayer(canonicalBoard, step=step)

        
        s = self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]

        if temp == 0:

            bestAs = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestA = np.random.choice(bestAs)
            probs = [0] * len(counts)
            probs[bestA] = 1

            return probs

        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [x / counts_sum for x in counts]

        return probs

    def searchSinglePlayer(self, canonicalBoard, step=0):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.

        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propagated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propagated up the search path. The values of Ns, Nsa, Qsa are
        updated.

        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.

        Returns:
            v: the negative of the value of the current canonicalBoard
        """
        
        s = self.game.stringRepresentation(canonicalBoard)

        terminate = self.game.isTerminate(canonicalBoard, step)

        if s not in self.Es:
            self.Es[s] = self.game.getGameEnded(canonicalBoard)
        if terminate:
            # terminal node
            return self.Es[s]

        if s not in self.Ps:
            # leaf node
            self.Ps[s], v = self.nnet.predict(canonicalBoard)
            self.modelCall += 1
            valids = self.game.getValidMoves(canonicalBoard)
            self.Ps[s] = self.Ps[s] * valids  # masking invalid moves
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s  # renormalize
            else:
                # if all valid moves were masked make all valid moves equally probable

                # NB! All valid moves may be masked if either your NNet architecture is insufficient or you've get overfitting or something else.
                # If you have got dozens or hundreds of these messages you should pay attention to your NNet and/or training process.   
                log.error("All valid moves were masked, doing a workaround.")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Ns[s] = 0
            return v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        # pick the action with the highest upper confidence bound
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
                            1 + self.Nsa[(s, a)])
                else:
                    u = self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)  # Q = 0 ?
                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        next_s, _ = self.game.getNextState(canonicalBoard, a)

        v = self.searchSinglePlayer(next_s, step+1)

        if (s, a) in self.Qsa:
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1

        else:
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1
        return v
    

    def inferSinglePlayer(self, canonicalBoard, step=0, seed=42):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.

        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propagated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propagated up the search path. The values of Ns, Nsa, Qsa are
        updated.

        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.

        Returns:
            v: the negative of the value of the current canonicalBoard
        """
        np.random.seed(seed)
        state = canonicalBoard
        selected_ac_seq = []
        for i in range(self.game.steps):
            terminate = self.game.isTerminate(state, i)
            if terminate:
                break

            s = self.game.stringRepresentation(state)
  
            ac_candidates = [action for (state, action) in self.Qsa.keys() if state == s]
            # pick the action with the highest upper confidence bound
            counts = []
       
            # for a in ac_candidates:
            for a in range(self.game.getActionSize()):
                try:
                    c_ = self.Nsa[(s, a)] 
                    counts.append(c_)
                except:
                    counts.append(0)

            counts_sum = float(sum(counts))
            if counts_sum == 0:
                probs, _ = self.nnet.predict(state)
                probs = probs.tolist()
              
            else:
                probs = [x / counts_sum for x in counts]
         
            # print('probs', probs)
            valid_moves = self.game.getValidMoves(state)
            masked_prob = valid_moves * probs
            counts_sum_masked = float(sum(masked_prob))
            probs = [x / counts_sum_masked for x in masked_prob]
       
            selected_ac = np.random.choice(len(probs), p=probs)
       
            state, action_in_text= self.game.getNextState(state, selected_ac)
            selected_ac_seq.append(action_in_text)

        res = self.game.getGameEnded(state)

        return selected_ac_seq, res

    
    def getModelCall(self):
        return self.modelCall
    
    def reset(self):
        self.Qsa = {}  # stores Q values for s,a (as defined in the paper)
        self.Nsa = {}  # stores #times edge s,a was visited
        self.Ns = {}  # stores #times board s was visited
        self.Ps = {}  # stores initial policy (returned by neural net)
        self.Es = {}  # stores game.getGameEnded ended for board s
        self.Vs = {}  # stores game.getValidMoves for board s