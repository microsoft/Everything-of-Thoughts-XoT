# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from argparse import ArgumentParser
from functools import partial
import random
import yaml

class AverageMeter(object):
    """From https://github.com/pytorch/examples/blob/master/imagenet/main.py"""

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def __repr__(self):
        return f'{self.avg:.2e}'

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class dotdict(dict):
    def __getattr__(self, name):
        return self[name]
    
class Config:  
    def __init__(self, dictionary):  
        for k, v in dictionary.items():  
            if isinstance(v, dict):  
                self.__dict__[k] = Config(v)  
            else:  
                self.__dict__[k] = v  


def load_config(config_path):  
    with open(config_path, 'r') as f:  
        return yaml.safe_load(f) 