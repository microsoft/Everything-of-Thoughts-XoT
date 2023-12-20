# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import re
import os
import sympy
import pandas as pd
import numpy as np
from .utils.puzzlesolver import printState, move, isSolved

class NPuzzleParser():
    """
    NpuzzlePaser provides the parsing of language model reponses specific to
    the npuzzle example.
    """
    def __init__(self):
        pass

    def get_current_state(self, s0, moves):
        s0 = s0.tolist()
        legal = True
        # print('s0', s0)
        for m in moves:
            # print('m', m)
            s1 = move(s0, m)
            # print('s1', s1)
            if s1 == None:
                s1 = s0
                legal = False
                break
            s0 = s1
        return s1, legal

    def get_input(self, idx: int) -> str:
        return self.data[idx]
    
    def get_revised_state(self, x, thoughts, incorrect_step):
        actions = thoughts.split('\n')
        moves = actions[:incorrect_step-1]

        if len(moves) == 0:
            return x
    
        revised_state, legal = self.get_current_state(x, moves)
        # print('revised_state', revised_state, legal)
        # input()
        return np.array(revised_state)
    
    def test_output(self, inputs, output, revised_flag):
        try:
            # print(output)
            # print('----------')
            moves = output.strip().split('[Moves]:\n')[-1].split(', ')
            s0 = inputs
            s1, legal = self.get_current_state(s0, moves)
            answer = int(isSolved(s1))

            if legal:
                return {'r': answer, 'revised': revised_flag}
            else:
                return {'r': 0, 'revised': revised_flag}
        except Exception as e:
            print(e)
            return {'r': 0, 'revised': revised_flag}


    def test_output_multi(self, inputs, outputs, revised_flag):
        moves_list =  re.findall(r"\d+\.\sMoves:\s(.+)", outputs)  
        if len(moves_list) == 0:
            moves_list =  re.findall(r"\[Solution \d+\]:\s(.+)", outputs)  
        try:
            revised_flag.extend([None]*(len(moves_list)-len(revised_flag)))
        except:
             revised_flag = [False] * len(moves_list)

        return_ = dict()
        for idx, moves in enumerate(moves_list):
            try:
                moves_ = moves.split(', ')
                # print('moves_', moves_)
                s0 = inputs
                s1, legal = self.get_current_state(s0, moves_)
                answer = int(isSolved(s1))
                return_['r%s'%(idx)] = {'r': answer, 'revised': revised_flag[idx]}
            except Exception as e:
                print(e)
                return_['r%s'%(idx)] = {'r': -1, 'revised': revised_flag[idx]}

        return {'r': return_} 
    
   
    def value_outputs_unwrap(self, x: str, y: str, value_outputs: list) -> float:

        value_names = [_.split('\n')[-1] for _ in value_outputs]
        # print('value_names', value_names)
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        # print('value', value)
        return value
    
    
    def select_outputs_unwrap(self, x, y, select_outputs, multi_solution) -> float:

        select_names = select_outputs[0].split('\n')
        # print('select_names', select_names)
        result = []
        for s in select_names:
            input_str = s.strip().split("\n")[-1].rstrip("\n")
            # print('input_str', input_str)
            match = re.search(r'\((\d+)\)', input_str)
            if match:  
                number = int(match.group(1))  
                result.append(number)
            else:  
                print('No number found inside parentheses.') 
                continue 
            
        return result

    def filter_moves(self, select_new_ys):  
        # Split the input string into a list of words  
        words = select_new_ys.strip().split('\n')
        # Filter out any words that are not "left" or "up"  
        filtered_words = [word for word in words if word in ["Left", "Up", "Down", "Right"]]  
    
        return filtered_words  


    def extract_top_select(self, select_new_ys):
        res = []
        for item in select_new_ys:
            top_select_new_ys = self.filter_moves(item)
            res.append(top_select_new_ys)
        return res
    
    def action_to_thoughs(self, actions, x):
        return '\n'.join(actions)