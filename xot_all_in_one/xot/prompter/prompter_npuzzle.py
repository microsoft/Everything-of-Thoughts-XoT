# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import re
import os
import sympy
import numpy as np
import pandas as pd
from .prompts.prompts_npuzzle import * 
from .utils.puzzlesolver import printState, move

class NPuzzlePrompter():
    """
    NpuzzlePrompter provides the generation of prompts specific to the npuzzle
    example for the language models.
    """
    def __init__(self, last_step=True):
        self.laststep = int(last_step)
        self.value_cache = {}
    
    def get_current_state(self, s0, moves):
        legal = True
        for m in moves:
            s1 = move(s0, m)
            if s1 == None:
                s1 = s0
                legal = False
                break
            s0 = s1
        return s1, legal

    
    def format_thoughts(self, x, y):
        current_s = x.tolist()
        moves = '%s\n'%(printState(current_s))
        thoughts = y.strip().split('\n')
        for i, m in enumerate(thoughts):
            legal_move = self.get_valid_move(current_s)
            s2, legal = self.get_current_state(current_s, [m])
            state2 = printState(s2)
            moves += 'Step %s: Choose one valid move from: %s\n%s\n%s\n'%(i+1, legal_move, m, state2)
            current_s = s2
        return moves, thoughts


    def format_thoughts_wo_last_step(self, x, y):
        current_s = x.tolist()
        moves = '%s\n'%(printState(current_s))
        thoughts = y.strip().split('\n')[:-1]
        for i, m in enumerate(thoughts):
            legal_move = self.get_valid_move(current_s)
            s2, legal = self.get_current_state(current_s, [m])
            state2 = printState(s2)
            moves += ' Choose one valid move from: %s\nStep %s:\n%s\n%s\n'%(legal_move, i+1, m, state2)
            current_s = s2
        
        # last valid move
        legal_move = self.get_valid_move(current_s)
        moves += 'Choose one valid move from: %s\n'%(legal_move)
        return moves, thoughts
    
    def get_valid_move(self, current_state):
        index_empty = current_state.index(0)
        legal_move = ['Up', 'Left', 'Down', 'Right']
        if index_empty in range(0, 3):
            legal_move.remove('Up')
        if index_empty in range(6, 9):
            legal_move.remove('Down')
        if index_empty in [0, 3, 6]:
            legal_move.remove('Left')
        if index_empty in [2, 5, 8]:
            legal_move.remove('Right')
        return legal_move

    def get_instruction_prompt(self) -> str:
        return npuzzle_instruct

    def standard_prompt_wrap(self, x, y:str='') -> str:
        s = printState(x)
        return npuzzle_prompt_io.format(state=s) + y
    
    def standard_prompt_wrap_multi(self, x, y='') -> str:
        s = printState(x)
        return npuzzle_prompt_io_multi.format(state=s) + y

 
    def cot_prompt_wrap(self, x: str, y:str='') -> str:
        s = printState(x)
        return npuzzle_prompt_cot.format(state=s) + y

    def cot_prompt_wrap_multi(self, x: str, y:str='') -> str:
        s = printState(x)
        # print(npuzzle_prompt_cot_multi.format(state=s) + y)
        # input()
        return npuzzle_prompt_cot_multi.format(state=s) + y
   

    def xot_prompt_wrap(self, x: str, y:str='') -> str:
        s = printState(x)
        if self.laststep:
            move_, thoughts = self.format_thoughts(x, y)
            prompt = npuzzle_prompt_pro_with_laststap.format(state=s, move=move_)
        else:
            move_, thoughts = self.format_thoughts_wo_last_step(x, y)
            prompt = npuzzle_prompt_pro_wo_laststap.format(state=s, move=move_)
        
        return prompt, thoughts

    def xot_prompt_multi_wrap(self, x, y) -> str:
        s = printState(x)
        moves = ''
        for idx, ys in enumerate(y):
            move_, thoughts = self.format_thoughts(x, ys)
            moves += '[Solution %s]:\n%s\nFinished.\n'%(idx+1, move_)
        prompt = npuzzle_prompt_xot_multi.format(state=s, move=moves)
        return prompt, move_

    def xot_prompt_revised_wrap(self, x, y='') -> str:
        s = printState(x)
        move_, thoughts = self.format_thoughts(x, y)
      
        prompt = npuzzle_prompt_revise.format(state=s, move=move_)
    
        return prompt, thoughts
  
    def propose_prompt_wrap(self, x: str, y: str='', isFinished: bool=False) -> str:
        if y != '':
            moves = y.replace('\n', ' ').strip().split(' ')
            current_state, legal = self.get_current_state(x.tolist(), moves)
        else:
            current_state = x.tolist()
       
        if isFinished:
            state = printState(x)
            if self.laststep:
                move_, thoughts = self.format_thoughts(x, y)
                prompt = npuzzle_prompt_pro_with_laststap.format(state=state, move=move_)
            else:
                move_, thoughts = self.format_thoughts_wo_last_step(x, y)
                prompt = npuzzle_prompt_pro_wo_laststap.format(state=state, move=move_)

            return prompt, x
        else:
            # print(current_state)
            state = printState(current_state)
            # print(state)
            legal_move = self.get_valid_move(current_state)
            
            move = ''
            for i, m in enumerate(legal_move):
                s1, legal = self.get_current_state(current_state, [m])
                s_after = printState(s1)
                move += '%s. %s\nAfter %s:\n%s'%(i+1, m, m, s_after)

            prompt = propose_prompt.format(state=state, move=move)
            return prompt, current_state
    

    def value_prompt_wrap(self, x: str, y: str) -> str:
        x = x.tolist()
        moves =  y.strip().split('\n')
        current_move = moves[-1]
        if len(moves) > 1:
            current_state, legal = self.get_current_state(x, moves[:-1])
        else:
            current_state = x

        state = printState(current_state)
        s1, legal = self.get_current_state(current_state, [current_move])
        s_after = printState(s1)
        move = current_move + '\n' + s_after
        return value_prompt.format(state=state, move=move)
    

    def select_prompt_wrap(self, x, ys, n_select_sample) -> str:
        '''
        [Proposed Move List]:
        1. Down
        3 1 2
        7 6 5
        0 4 8
        2. Right
        3 1 2
        6 0 5
        7 4 8
        '''
        move = ''
        for idx, y in enumerate(ys):
            moves =  y.strip().split('\n')
            current_move = moves[-1]
            if len(moves) > 1:
                current_state, legal = self.get_current_state(x.tolist(), moves[:-1])
            else:
                current_state = x.tolist()
            state = printState(current_state)
            s1, legal = self.get_current_state(current_state, [current_move])
            s_after = printState(s1)
            move += '(%s) '%(idx+1) + current_move + '\n' + s_after + '\n' 

        if n_select_sample == 3:
            return merge_prompt_3_select_sample.format(n_select_sample=n_select_sample, state=state, move=move)
        else:
            return merge_prompt.format(n_select_sample=n_select_sample, state=state, move=move)