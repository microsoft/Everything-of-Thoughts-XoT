# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import numpy as np
import coloredlogs
from argparse import ArgumentParser
from Coach import Coach


from utils import *


def main():
    parser = ArgumentParser("Everything of Thoughts! 🎉")
    parser.add_argument('--env', type=str)
    parser.add_argument('--mode', type=str)
    parser.add_argument('--numIters', type=int, default=3) # Number of iteration.
    parser.add_argument('--numEps', type=int, default=10)  # Number of complete self-play games to simulate during a new iteration.
    parser.add_argument('--updateThreshold', type=float, default=0) # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    parser.add_argument('--maxlenOfQueue', type=int, default=10000) # Number of game examples to train the neural networks.
    parser.add_argument('--numMCTSSims', type=int, default=100) # Number of games moves for MCTS to simulate.
    parser.add_argument('--tempThreshold', type=int, default=15) # Temperature threthold
    parser.add_argument('--arenaCompare', type=int, default=100) # Number of games to play during arena play to determine if new net will be accepted.
    parser.add_argument('--cpuct', type=float, default=1)
    parser.add_argument('--winReward', type=float, default=1)
    parser.add_argument('--checkpoint', type=str, default='./temp/')
    parser.add_argument('--load_model', type=bool, default=False)
    parser.add_argument('--load_folder_file', type=tuple, default=('/dev/models','best.pth.tar'))
    parser.add_argument('--numItersForTrainExamplesHistory', type=int, default=1000)
    parser.add_argument('--training_env', type=str, default='')
    parser.add_argument('--test_env', type=str, default='')
    parser.add_argument('--multi_sol', type=int, default=0)
    parser.add_argument('--multi_times', type=int, default=500)
    args = parser.parse_args()

    logging.basicConfig(filename='logs/%s_%s.log'%(args.env, args.mode), filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  
    logging.info(args)

    if args.env.lower() == 'game24':
        from game24.Game24Game import Game24 as Game
        from game24.pytorch.NNet import NNetWrapper as nn
    elif args.env.lower() == 'cube':
        from cube.CubeGame import Cube as Game
        from cube.pytorch.NNet import NNetWrapper as nn
    elif args.env.lower() == 'npuzzle':
        from npuzzle.NPuzzleGame import NPuzzle as Game
        from npuzzle.pytorch.NNet import NNetWrapper as nn
    else:
        raise ValueError

    logging.info('Loading %s...', Game.__name__)
    g = Game(args.training_env, args.test_env)

    logging.info('Loading %s...', nn.__name__)
    nnet = nn(g)


    if args.mode.lower() == 'train':
        if args.load_model:
            logging.info('Loading checkpoint "%s/%s"...', args.load_folder_file)
            nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
        else:
            logging.warning('Not loading a checkpoint!')

        logging.info('Loading the Coach...')
        c = Coach(g, nnet, args, player=1)

        if args.load_model:
            logging.info("Loading 'trainExamples' from file...")
            c.loadTrainExamples()
        logging.info('Welcome to play %s, Starting the learning process 🎉' % args.env)

        c.learn()

    elif args.mode.lower() == 'test' and args.checkpoint:
        c = Coach(g, nnet, args, player=1)
        logging.info('Welcome to play %s, Starting the inference process 🎉' % args.env)
        c.infer()
    else:
        logging.info('[ERROR] Please input train or test mode.' % args.env)


if __name__ == "__main__":
    main()
