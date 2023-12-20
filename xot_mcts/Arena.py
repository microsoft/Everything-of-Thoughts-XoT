# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import numpy as np
from tqdm import tqdm

log = logging.getLogger(__name__)


class ArenaSingle():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, mcts1, mcts2, game, winReward=1):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.mcts1 = mcts1
        self.mcts2 = mcts2

        self.player1 = lambda x: np.argmax(mcts1.getActionProb(x, temp=0, step=0))
        self.player2 = lambda x: np.argmax(mcts2.getActionProb(x, temp=0, step=0))
        self.game = game
        self.winReward = winReward

    def playGame(self, player, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """


        if self.game.test_size > 0:
            board = self.game.getTestBoard()
        else:
            board = self.game.getInitBoard()
        it = 0

        step = 0
        while not self.game.isTerminate(board, step):
            action = player(board)
            valids = self.game.getValidMoves(board)
            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, _ = self.game.getNextState(board, action)
            step += 1
            if verbose:
                print("Game over: Turn ", str(it), "Result ", str(self.game.getGameEnded(board)))
        return self.game.getGameEnded(board)

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
        """

        oneWon = 0
        twoWon = 0

        self.game.TestReset()

        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            self.mcts1.reset()
            gameResult = self.playGame(self.player1, verbose=verbose)
            if gameResult == self.winReward:
                oneWon += 1

        self.game.TestReset()
        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            self.mcts2.reset()
            gameResult = self.playGame(self.player2, verbose=verbose)
            if gameResult == self.winReward:
                twoWon += 1

        self.game.TestReset()

        return oneWon, twoWon
    


class ArenaTest():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, mcts1, game, multi_sol=0, winReward=1):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.mcts1 = mcts1
        
        self.player1 = lambda x: np.argmax(self.mcts1.getActionProb(x, multi_sol, temp=0, step=0))
        self.game = game
        self.winReward = winReward
        self.multi_sol = multi_sol

    def playGame(self, player, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """


        if self.game.test_size > 0:
            board = self.game.getTestBoard()
        else:
            board = self.game.getInitBoard()
        it = 0
        problem_state = board

        step = 0
        actions = []
        while not self.game.isTerminate(board, step):
            action = player(board)
            valids = self.game.getValidMoves(board)
            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, action_in_text = self.game.getNextState(board, action)
            actions.append(action_in_text)
            step += 1
            if verbose:
                print("Game over: Turn ", str(it), "Result ", str(self.game.getGameEnded(board)))
        
        
        return problem_state, self.game.getGameEnded(board), actions

    def playGames(self, num, multi_times, verbose=False):
        """
        Plays num games

        Returns:
            oneWon: games won by player1
        """

        oneWon = 0
        thoughts_record = []
        self.game.TestReset()
        
        for i in range(num):
   
            print('num %s'%(i+1), 'multi_times %s'%multi_times)
            self.game.total_test = i+1
            self.mcts1.reset()
            problem_state, gameResult, actions = self.playGame(self.player1, verbose=verbose)
            thoughts_record.append([str(problem_state), str(actions), gameResult == self.winReward])

            if self.multi_sol:
                for sol in range(multi_times):
                    selected_ac_seq, res = self.mcts1.inferSinglePlayer(problem_state, step=0, seed=sol)
                    if selected_ac_seq is not None:
                        thoughts_record.append([str(problem_state), str(selected_ac_seq), res == self.winReward])

            if gameResult == self.winReward:
                oneWon += 1

        self.game.TestReset()

        return oneWon, thoughts_record
    







