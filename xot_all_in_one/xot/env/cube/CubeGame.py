# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
import pandas as pd
import numpy as np
from . import py222
from .solver import *
from itertools import permutations

import logging
import coloredlogs

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

"""
Game class implementation for the game of 24.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Chaoyun Zhang
Date: Sep 28, 2023.
"""

ACTION_SIZE = 9
action_list = ["U", "U'", "U2", "R", "R'", "R2", "F", "F'", "F2"]


class Cube(Game):
    def __init__(self, train_dir='', test_dir=''):
        self.action_size = ACTION_SIZE


        self.train_size = 0
        self.test_size = 0
        self.total_test = 0
        self.total_game_step = 4

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

        state_index = ['state_%s'%i for i in range(1, 25)]
        if self.train_size > 0:
            choose = self.train_data[state_index].sample(n=1).values[0]
            b = np.array(choose)
        else:
            b = np.array([4, 5, 4, 4, 5, 1, 5, 0, 0, 0, 2, 0, 1, 1, 3, 2, 2, 2, 4, 3, 3, 3, 1, 5])   
        return b

    def getTestBoard(self):
        # return initial board (numpy board)
        state_index = ['state_%s'%i for i in range(1, 25)]
        if self.test_size > 0:
            i = self.total_test % self.test_size
            choose = self.test_data[state_index].iloc[i]
            b = np.array(choose)
            self.total_test += 1
            return b
        return self.getInitBoard()
    
    def getOneTestBoard(self, idx):
        # return initial board (numpy board)
        state_index = ['state_%s'%i for i in range(1, 25)]
        choose = self.test_data[state_index].iloc[idx]
        b = np.array(choose)
        return b

    def TestReset(self):
        self.total_test = 0

    def getBoardSize(self):
        # (a,b) tuple
        return 24

    def getActionSize(self):
        # return number of actions
        return self.action_size

    def getNextState(self, board, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move

        next_state = py222.doAlgStr(board, action_list[action])

        return np.array(next_state), action_list[action]
        
        
    def getValidMoves(self, board):
        # return a fixed size binary vector

        valids = np.array([1] * self.getActionSize())

        return valids


    def getGameEnded(self, board):
        _, minmumStep = solveCube(np.array(board))

        if minmumStep == 0:
            reward = 1
        else:
            reward = minmumStep * (-0.05)
        return reward
    

    def isFinishing(self, x, moves):
        s1 = py222.doAlgStr(np.array(x), moves)
        answer = int(py222.isSolved(np.array(s1)))
        
        return True if answer == 1 else False
   

    def isTerminate(self, board, step):

        return py222.isSolved(board) or step >=self.total_game_step
      

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        """Board is not symmetric"""

        Symboard = []
        positions = {}

        for color in range(6):
            positions[color] = np.where(board==color)

        for order in permutations(range(6)):
            new_s = board.copy()
            for pcolor, ncolor in enumerate(order):
                new_s[positions[pcolor]] = ncolor
            Symboard.append((new_s, pi))

        return Symboard

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tobytes()