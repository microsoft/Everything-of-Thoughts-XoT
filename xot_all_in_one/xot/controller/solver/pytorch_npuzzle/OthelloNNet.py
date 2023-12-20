# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import sys
from .utils import *

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

class OthelloNNet(nn.Module):
    def __init__(self, game, args):
        # game params
        self.board_size = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.hidden_size = 128
        self.args = args

        super(OthelloNNet, self).__init__()

        self.fc1 = nn.Linear(self.board_size, self.hidden_size)
        self.fc2 = nn.Linear(self.hidden_size , self.hidden_size * 2)

        self.fc_p1 = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.fc_p2 = nn.Linear(self.hidden_size, self.action_size)

        self.fc_v1 = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.fc_v2 = nn.Linear(self.hidden_size, 1)


    def forward(self, s):
        s = s.view(-1, self.board_size)                
        s = F.relu(self.fc1(s))                       
        s = F.relu(self.fc2(s))                         

        sp = self.fc_p1(s)       
        sp = self.fc_p2(sp)   

        sv = self.fc_v1(s)       
        sv = self.fc_v2(sv)                                                                        
                                                                               

        return F.log_softmax(sp, dim=1), sv
