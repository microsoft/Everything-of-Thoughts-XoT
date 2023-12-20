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

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.


"""
Game class implementation for the game of 24.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Chaoyun Zhang
Date: Sep 28, 2023.
"""

ACTION_SIZE = 36
MASK_VALUE = 0.0001

action_ = ['+','-','in-','*','/','in/']
action_dic = {0: [0, '+', 1], 1: [0, '-', 1], 2: [1, '-', 0], 3: [0, '*', 1], 4: [0, '/', 1], 5: [1, '/', 0], 6: [0, '+', 2], 7: [0, '-', 2], 8: [2, '-', 0], 9: [0, '*', 2], 10: [0, '/', 2], 11: [2, '/', 0], 12: [0, '+', 3], 13: [0, '-', 3], 14: [3, '-', 0], 15: [0, '*', 3], 16: [0, '/', 3], 17: [3, '/', 0], 18: [1, '+', 2], 19: [1, '-', 2], 20: [2, '-', 1], 21: [1, '*', 2], 22: [1, '/', 2], 23: [2, '/', 1], 24: [1, '+', 3], 25: [1, '-', 3], 26: [3, '-', 1], 27: [1, '*', 3], 28: [1, '/', 3], 29: [3, '/', 1], 30: [2, '+', 3], 31: [2, '-', 3], 32: [3, '-', 2], 33: [2, '*', 3], 34: [2, '/', 3], 35: [3, '/', 2]}



class Game24(Game):
    def __init__(self, train_dir='', test_dir=''):
        self.action_size = ACTION_SIZE
        self.terminate = False
        self.target = 24
        self.init_board = [8, 8, 5, 5]
        self.train_size = 0
        self.test_size = 0
        self.total_test = 0
        self.n = 4
        self.total_game_step = 3

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
        if self.train_size > 0:
            choose = self.train_data['Puzzles'].sample(n=1).values
            b = np.array([int(i) for i in choose[0].split(' ')])
        else:
            b = self.init_board
        return np.array(b)

    def getTestBoard(self):
        # return initial board (numpy board)
        if self.test_size > 0:
            i = self.total_test % self.test_size
            choose = self.test_data['Puzzles'].iloc[i]
            b = np.array([int(i) for i in choose.split(' ')])
            self.total_test += 1
            return np.array(b)
        return self.getInitBoard()
    
    def getOneTestBoard(self, idx):
        # return initial board (numpy board)
        choose = self.test_data['Puzzles'].iloc[idx]
        b = np.array([int(i) for i in choose.split(' ')])
        return b
    
    def TestReset(self):
        
        self.total_test = 0

    def getBoardSize(self):

        return self.n

    def getActionSize(self):
        # return number of actions
        return self.action_size
    
    def getNextState(self, board, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        action_value = action_dic[action]
        num1, operator, num2 = action_value
        step = board.tolist().count(MASK_VALUE)
        step += 1
        expression = str(board[num1]) + str(operator) + str(board[num2]) 
        result = eval(expression)
        remaining = [x for i, x in enumerate(board) if i not in [num1, num2] and x != MASK_VALUE]

        n1, n2 = board[num1], board[num2]
        exp_in_text = [str(operator), int(n1)if int(n1)==n1 else n1, int(n2)if int(n2)==n2 else n2]

        next_state = sorted([result] + remaining) + [MASK_VALUE] * step
        return np.array(next_state), exp_in_text
        

    def getValidMoves(self, board):
        # return a fixed size binary vector
        valids = np.ones(ACTION_SIZE, dtype=np.float32)

        step = board.tolist().count(MASK_VALUE)
        valid_index = self.getBoardSize() - step

        count = 0

        for num1 in range(self.getBoardSize()):
            for num2 in range(num1 + 1,self.getBoardSize()):
                for op in action_:
                    operator = op[-1]
                    if 'in' in op:
                        expression_list = [num2, operator, num1]
                    else:
                        expression_list = [num1, operator, num2]
                    if expression_list[0] > valid_index - 1 or expression_list[2] > valid_index - 1:
                        valids[count] = 0
                    elif board[expression_list[2]] == 0 and expression_list[1] == '/':
                        valids[count] = 0
                    count += 1
        return valids


    def getGameEnded(self, board):
         
        terminate = board.tolist().count(MASK_VALUE) >= 3
        
        if terminate:
            if np.abs(board[0] - self.target) < 1e-4:
                reward = 1
                # print("Get rewards!")
            else:
                reward = -1
        else:
            reward = 0
        return reward
    

    def isTerminate(self, board, step):
        return step >= 3 or  board.tolist().count(MASK_VALUE) >= 3
    
    def isFinishing(self, board, step):

        return step >= 3 or  board.tolist().count(MASK_VALUE) >= 3
   

    def getCanonicalForm(self, board, player):

        return player*board

    def getSymmetries(self, board, pi):
        """Board is not symmetric"""
        return [(board, pi)]

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tobytes()
