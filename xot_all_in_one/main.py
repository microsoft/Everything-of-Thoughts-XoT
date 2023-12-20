# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from argparse import ArgumentParser
from functools import partial
import random
import yaml

from utils import Config, load_config
from xot import env
from xot.controller import chatgpt
from xot.controller import Controller
from xot.prompter import CubePrompter, Game24Prompter, NPuzzlePrompter
from xot.parser import CubeParser, Game24Parser, NPuzzleParser
 
  
parser = ArgumentParser("Everything of Thoughts! 🎉")  
parser.add_argument('--config', type=str, required=True, help='Path to YAML configuration file.')  
args = parser.parse_args()  
  
# Load the configuration file  
config = Config(load_config(args.config))
gpt = partial(chatgpt, model=config.gpt.backend, temperature=config.gpt.temperature)

if config.env == 'cube':
    game = env.Cube(test_dir=config.task.data)
    prompter = CubePrompter(last_step=config.param.last_step)
    parser = CubeParser()
elif config.env == 'game24':
    game = env.Game24(test_dir=config.task.data)
    prompter = Game24Prompter(last_step=config.param.last_step)
    parser = Game24Parser()
elif config.env == 'npuzzle':
    game = env.NPuzzle(test_dir=config.task.data)
    prompter = NPuzzlePrompter(last_step=config.param.last_step)
    parser = NPuzzleParser()
else:
    raise ValueError("Invalid Environment")

# Create the Controller
ctrl = Controller(config, gpt, game, prompter, parser)
# Run the Controller and generate the output
ctrl.run()



