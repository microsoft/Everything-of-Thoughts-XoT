# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
import pandas as pd
import numpy as np
import logging
import coloredlogs
import argparse
import timeit
from collections import deque
from heapq import heappush, heappop, heapify
import itertools
import numpy as np

from .solver import *

log = logging.getLogger(__name__)

"""
Game class implementation for NPuzzle.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Chaoyun Zhang
Date: Sep 28, 2023.
"""

ACTION_SIZE = 4
action_list = ['Left', 'Down', 'Right', 'Up']


class NPuzzle(Game):
    def __init__(self, train_dir='', test_dir=''):

        self.train_size = 0
        self.test_size = 0
        self.total_test = 0
        self.action_size = ACTION_SIZE
        self.steps = 9


        if train_dir:
            log.info("Loading Training Environment...")
            self.train_data = pd.read_csv(train_dir)
            self.train_size = len(self.train_data)
        if test_dir:
            log.info("Loading Test Environment...")
            self.test_data = pd.read_csv(test_dir)
            self.test_size = len(self.test_data)
        
    def getInitBoard(self):
        # return initial board (numpy board)

        state_index = ['state_%s'%i for i in range(1, 10)]
        if self.train_size > 0:
            choose = self.train_data[state_index].sample(n=1).values[0]
            b = np.array(choose)
        else:
            b = np.array([3, 1, 2, 0, 6, 5, 7, 4, 8])   
        return b

    def getTestBoard(self):
        # return initial board (numpy board)
        state_index = ['state_%s'%i for i in range(1, 10)]
        if self.test_size > 0:
            i = self.total_test % self.test_size
            choose = self.test_data[state_index].iloc[i]
            b = np.array(choose)
            self.total_test += 1
            return b
        return self.getInitBoard()

    
    def getOneTestBoard(self, idx):
        # return initial board (numpy board)
        state_index = ['state_%s'%i for i in range(1, 10)]
        choose = self.test_data[state_index].iloc[idx]
        b = np.array(choose)
        return b

    
    def TestReset(self):
        self.total_test = 0

    def getBoardSize(self):
        # (a,b) tuple
        return 9

    def getActionSize(self):
        # return number of actions
        return self.action_size
    

    def getNextState(self, board, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move

        direction = action_list[action]
        next_state = move(board.tolist(), direction)

        return np.array(next_state), direction
        

    def getValidMoves(self, board):
        # return a fixed size binary vector

        valids = np.array([1] * self.getActionSize())

        for action in range(self.getActionSize()):
            direction = action_list[action]
            if move(board.tolist(), direction) == None:
                valids[action] = 0

        return valids


    def getGameEnded(self, board):
         
        minmumStep = len(solve(board.tolist())['path_to_goal'])

        if minmumStep == 0:
            reward = 1
        else:
            reward = minmumStep * (-0.01)

        return reward
    

    def isTerminate(self, board, step):

        return len(solve(board.tolist())['path_to_goal']) == 0 or step >= self.steps
    

    def isFinishing(self, board, moves):
        board = board.tolist()
        s_current, _ = self.get_current_state(board, moves)
        return len(solve(s_current)['path_to_goal']) == 0

    def get_current_state(self, s0, moves):
        legal = True
        for m in moves:
            # print('m', m)
            s1 = move(s0, m)
            # print('s1', s1)
            if s1 == None:
                s1 = s0
                legal = False
                break
            s0 = s1
        return s1, legal
   
      

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        """Board is not symmetric"""
        return [(board, pi)]

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tobytes()
