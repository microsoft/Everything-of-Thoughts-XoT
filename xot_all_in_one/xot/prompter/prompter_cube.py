# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import re
import os
import sympy
import numpy as np
import pandas as pd
from .prompts.prompts_cube import * 
from .utils.py222 import doAlgStr, getCube

class CubePrompter():
    """
    CubePrompter provides the generation of prompts specific to the cube
    example for the language models.
    """
    def __init__(self, last_step=True):
        self.last_step = int(last_step)
        self.value_cache = {}

    
    def get_current_state(self, x, y: str) -> str:
        moves = y.strip().replace('\n', ' ')
        s = doAlgStr(np.array(x), moves)

        return s.tolist()
    
    def count_inconsistencies(self, input_):  
        color_key = ['Upper', 'Right', 'Front', 'Down', 'Left', 'Back']
        color_dict = dict()
        for i in range(6):
            order = i*4
            color = input_[order:order+4]
            color_dict[color_key[i]] = len(set(color))
        return color_dict  


    def format_thoughts(self, x: str, y: str) -> str:

        current_s = x
        moves = ''
        thoughts = y.strip().split('\n')
        for i, m in enumerate(thoughts):
            s2 = doAlgStr(np.array(current_s), m)
            state2 = getCube(s2)
            moves += '[Step %s]\n[Move] %s\n[Current Cube State]\n%s\n'%(i+1, m, state2)
            current_s = s2

        return moves, thoughts, current_s  

    def format_thoughts_wo_last_step(self, x: str, y: str) -> str:

        current_s = x
        moves = ''
        thoughts = y.strip().split('\n')[:-1]
        for i, m in enumerate(thoughts):
            s2 = doAlgStr(np.array(current_s), m)
            state2 = getCube(s2)
            moves += '[Step %s]\n[Move] %s\n[Current Cube State]\n%s\n'%(i+1, m, state2)
            current_s = s2

        return moves, thoughts, current_s 
    
    def get_instruction_prompt(self) -> str:
        return cube_instruct

    def standard_prompt_wrap(self, x, y='') -> str:
        s = getCube(x)
        return cube_prompt_io.format(state=s) + y
    
    def standard_prompt_wrap_multi(self, x, y='') -> str:
        s = getCube(x)
        return cube_prompt_io_multi.format(state=s) + y

    def cot_prompt_wrap(self, x, y='') -> str:
        s = getCube(x)
        return cube_prompt_cot.format(state=s) + y

    def cot_prompt_wrap_multi(self, x, y='') -> str:
        s = getCube(x)
        return cube_prompt_cot_multi.format(state=s) + y
    
    def xot_prompt_wrap(self, x, y='') -> str:
        s = getCube(x)
        if self.last_step:
            move_, thoughts, _ = self.format_thoughts(x, y)
            prompt = cube_prompt_xot_with_laststap.format(state=s, move=move_)
        else:
            move_, thoughts, _ = self.format_thoughts_wo_last_step(x, y)
            prompt = cube_prompt_xot_wo_laststap.format(state=s, move=move_)
        
        return prompt, thoughts
    
    def xot_prompt_multi_wrap(self, x, y) -> str:
        s = getCube(x)
        moves = ''
        for idx, ys in enumerate(y):
            move_, thoughts, _ = self.format_thoughts(x, ys)
            moves += '[Solution %s]:\n%s\nFinished.\n'%(idx+1, move_)
        prompt = cube_prompt_xot_multi.format(state=s, move=moves)
        return prompt, move_
    
    def xot_prompt_revised_wrap(self, x, y='') -> str:
        s = getCube(x)
        move_, thoughts, current_state = self.format_thoughts(x, y)
        checking_dict = self.count_inconsistencies(current_state)
     
        reason = 'After finishing all the moves: '
        for item in ['Upper', 'Front', 'Down', 'Left', 'Right', 'Back']:
            if checking_dict[item] > 1:
                reason += 'The %s face still has %s differnet colors. '%(item, checking_dict[item])
        
        prompt = cube_prompt_revised.format(state=s, move=move_, reason=reason)
    
        return prompt, thoughts
    

    def propose_prompt_wrap(self, x, y='', isFinished=False) -> str:
        if y != '':
            current_state = self.get_current_state(x, y)
        else:
            current_state = x
            
        if isFinished:
            state = getCube(x)
            if self.last_step:
                move_, _, _ = self.format_thoughts(x, y)
                prompt = cube_prompt_xot_with_laststap.format(state=state, move=move_)
            else:
                move_, _, _ = self.format_thoughts_wo_last_step(x, y)
                prompt = cube_prompt_xot_wo_laststap.format(state=state, move=move_)
            
            return prompt, current_state
        else:
            state = getCube(current_state)
            prompt = propose_prompt.format(state=state)
            return prompt, current_state
        

    def select_prompt_wrap(self, x, ys, n_select_sample) -> str:
        '''
        [Proposed Move List]:
        [U2, F']
        '''
        move = ''
        for idx, y in enumerate(ys):
            moves =  y.strip().split('\n')
            current_move = moves[-1]
            if len(moves) > 1:
                current_state = self.get_current_state(x, '\n'.join(moves[:-1]))
            else:
                current_state = x
            state = getCube(current_state)
            s1 = self.get_current_state(current_state, current_move)
            s_after = getCube(s1)
            if n_select_sample == 3:
                move += '(%s)\n[Current Cube State]:%s\n[Move]: %s\n[After the Move]:\n%s\n'%((idx+1), current_state, current_move, s_after)
            else:
                move += '(%s)\n[Move]: %s\n[After the Move]:\n%s\n'%((idx+1), current_move, s_after)

        if n_select_sample == 3:
            return merge_prompt_3_select_sample.format(n_select_sample=n_select_sample, state=state, move=move)
        else:
            return merge_prompt.format(n_select_sample=n_select_sample, state=state, move=move)

    def value_prompt_wrap(self, x, y) -> str:
        moves =  y.strip().split('\n')
        current_move = moves[-1]
        if len(moves) > 1:
            current_state = self.get_current_state(x, '\n'.join(moves[:-1]))
        else:
            current_state = x
        state = getCube(current_state)
        after_state = self.get_current_state(current_state, moves[-1])
        move = current_move 
        next_state = getCube(after_state)
        return value_prompt.format(state=state, move=move, next_state=next_state)