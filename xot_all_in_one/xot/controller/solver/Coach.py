# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import os
import sys
from collections import deque
from pickle import Pickler, Unpickler
from random import shuffle

import pandas as pd
import numpy as np
from tqdm import tqdm

from .Arena import ArenaSingle, ArenaTest
from .MCTS import MCTS

class Coach():
    """
    This class executes the self-play + learning. It uses the functions defined
    in Game and NeuralNet. args are specified in main.py.
    """

    def __init__(self, game, nnet, args, player=2):
        self.game = game
        self.nnet = nnet
        self.pnet = self.nnet.__class__(self.game)  # the competitor network
        self.args = args
        self.player = player
        self.mcts = MCTS(self.game, self.nnet, self.args, self.player)
        self.trainExamplesHistory = []  # history of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False  # can be overriden in loadTrainExamples()
        

    def executeEpisode(self):
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.

        Returns:
            trainExamples: a list of examples of the form (canonicalBoard, currPlayer, pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually won the game, else -1.
        """
        trainExamples = []
        board = self.game.getInitBoard()
        self.curPlayer = 1
        episodeStep = 0
        rewards = [0]

        while True:
            
            canonicalBoard = self.game.getCanonicalForm(board, self.curPlayer) if self.player == 2 else board
            temp = int(episodeStep < self.args.tempThreshold)

            pi = self.mcts.getActionProb(canonicalBoard, temp=temp, step=episodeStep)

            sym = self.game.getSymmetries(canonicalBoard, pi)
            for b, p in sym:
                trainExamples.append([b, self.curPlayer, p, None])

            action = np.random.choice(len(pi), p=pi)
            if self.player == 2:
                board, self.curPlayer = self.game.getNextState(board, self.curPlayer, action)
                r = self.game.getGameEnded(board, self.curPlayer)
            else:
                board, self.curPlayer = self.game.getNextState(board, action)
                r = self.game.getGameEnded(board)

            rewards.append(r)

            episodeStep += 1
            terminate = self.game.isTerminate(board, episodeStep)
            if terminate:
                sym = self.game.getSymmetries(board, pi)
                for b, p in sym:
                    trainExamples.append([b, self.curPlayer, p, None])
                # if r == 1:
                #     for i, x in enumerate(trainExamples):
                #         _, v = self.nnet.predict(x[0])
                #         print(x[0], sum(rewards[i:]), v)
                return [(x[0], x[2], sum(rewards[i:])) for i, x in enumerate(trainExamples)]


    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximum length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, self.args.numIters + 1):
            # bookkeeping
            logging.info(f'Starting Iter #{i} ...')
            # examples of the iteration
            if not self.skipFirstSelfPlay or i > 1:
                iterationTrainExamples = deque([], maxlen=self.args.maxlenOfQueue)

                for _ in tqdm(range(self.args.numEps), desc="Self Play"):
                    self.mcts = MCTS(self.game, self.nnet, self.args, self.player)  # reset search tree
                    iterationTrainExamples += self.executeEpisode()

                # save the iteration examples to the history 
                self.trainExamplesHistory.append(iterationTrainExamples)

            if len(self.trainExamplesHistory) > self.args.numItersForTrainExamplesHistory:
                logging.warning(
                    f"Removing the oldest entry in trainExamples. len(trainExamplesHistory) = {len(self.trainExamplesHistory)}")
                self.trainExamplesHistory.pop(0)
            # backup history to a file
            # NB! the examples were collected using the model from the previous iteration, so (i-1)  
            self.saveTrainExamples(i - 1)

            # shuffle examples before training
            trainExamples = []
            for e in self.trainExamplesHistory:
                trainExamples.extend(e)
            shuffle(trainExamples)

            # training new network, keeping a copy of the old one
            self.nnet.save_checkpoint(folder=self.args.checkpoint + self.args.env + '/', filename='temp.pth.tar')
            self.pnet.load_checkpoint(folder=self.args.checkpoint + self.args.env + '/', filename='temp.pth.tar')
            pmcts = MCTS(self.game, self.pnet, self.args, self.player)

            self.nnet.train(trainExamples)
            nmcts = MCTS(self.game, self.nnet, self.args, self.player)

            logging.info('PITTING AGAINST PREVIOUS VERSION')
        
            pmcts_modelcall_before = pmcts.getModelCall()
            nmcts_modelcall_before = nmcts.getModelCall()
    
            arena = ArenaSingle(pmcts, nmcts, self.game, self.args.winReward)
            pwins, nwins = arena.playGames(self.args.arenaCompare, verbose=True)
            pmcts_modelcall_after = pmcts.getModelCall()
            nmcts_modelcall_after = nmcts.getModelCall()

            pmcts_modelcall_avg = round((pmcts_modelcall_after - pmcts_modelcall_before) / self.args.arenaCompare, 2)
            nmcts_modelcall_avg = round((nmcts_modelcall_after - nmcts_modelcall_before) / self.args.arenaCompare, 2)

            logging.info('NEW/PREV WINS : %d / %d, NEW/PREV AVG CALL : %s / %s, ' % (nwins, pwins, nmcts_modelcall_avg, pmcts_modelcall_avg))

            
            if pwins + nwins == 0 or float(nwins - pwins) / self.args.arenaCompare < self.args.updateThreshold:
                logging.info('REJECTING NEW MODEL')
                self.nnet.load_checkpoint(folder=self.args.checkpoint + self.args.env + '/', filename='temp.pth.tar')
            else:
                logging.info('ACCEPTING NEW MODEL')
                self.nnet.save_checkpoint(folder=self.args.checkpoint + self.args.env + '/', filename=self.getCheckpointFile(i))
                self.nnet.save_checkpoint(folder=self.args.checkpoint + self.args.env + '/', filename='best.pth.tar')


    def infer(self):
        """
        Load model and generate thoughts.
        """
      
        # training new network, keeping a copy of the old one
        self.pnet.load_checkpoint(folder=self.args.checkpoint + self.args.env + '/', filename='best.pth.tar')
        pmcts = MCTS(self.game, self.pnet, self.args, self.player)

        logging.info('TESTING BEGAIN:')
        
        pmcts_modelcall_before = pmcts.getModelCall()
   
        arena = ArenaTest(pmcts, self.game, self.args.winReward)
        pwins, thoughts_record = arena.playGames(self.args.arenaCompare, verbose=True)
        pmcts_modelcall_after = pmcts.getModelCall()

        pmcts_modelcall_avg = round((pmcts_modelcall_after - pmcts_modelcall_before) / self.args.arenaCompare, 2)
        thoughts_acc = round(pwins/self.game.test_size, 4) * 100

        logging.info('TESTING WINS :  %d / %d, THOUGHTS ACC : %d %%, TESTING AVG CALL : %s' % (pwins, self.game.test_size, thoughts_acc, pmcts_modelcall_avg))
        pd_thoughts = pd.DataFrame(data=thoughts_record, columns=['problem_state', 'thoughts', 'acc'])
        pd_thoughts.to_csv('./logs/%s_thoughts.csv'%self.args.env)
    
    def generate_thoughts(self, board, player, early_stop=1000):
        problem_state = board
        step = 0
        actions, action_in_text_list = [], []
        # print('self.game.total_game_step', self.game.total_game_step)
        # input()
        while not self.game.isTerminate(board, step):
            action = player(board)
            valids = self.game.getValidMoves(board)
            board, action_in_text = self.game.getNextState(board, action)
            actions.append(action)
            action_in_text_list.append(action_in_text)
            step += 1
   
        return problem_state, self.game.getGameEnded(board), actions, action_in_text_list

    def getCheckpointFile(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, iteration):
        folder = self.args.checkpoint + self.args.env + '/'
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration) + ".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed

    def loadTrainExamples(self):
        modelFile = os.path.join(self.args.load_folder_file[0], self.args.load_folder_file[1])
        examplesFile = modelFile + ".examples"
        if not os.path.isfile(examplesFile):
            logging.warning(f'File "{examplesFile}" with trainExamples not found!')
            r = input("Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            logging.info("File with trainExamples found. Loading it...")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            logging.info('Loading done!')

            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True
