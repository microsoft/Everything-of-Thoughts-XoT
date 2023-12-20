# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import re
import os
import sympy
import pandas as pd
import numpy as np
from .utils.py222 import doAlgStr, getCube, isSolved


class CubeParser():
    """
    CubePaser provides the parsing of language model reponses specific to
    the cube example.
    """
    def __init__(self):
        pass

    def get_input(self, idx: int) -> str:
        return self.data[idx]
    
    def get_revised_state(self, x, thoughts, incorrect_step):
        actions = thoughts.split('\n')
        move_lst = actions[:incorrect_step-1]
        moves = " ".join(move_lst)
        return doAlgStr(x, moves)
    
    def test_output(self, inputs, outputs, revised_flag):
        try:

            moves = outputs.split('[Restoration Moves]:\n')[-1].replace('\n', ' ').strip()

            s1 = doAlgStr(inputs, moves)
            answer = int(isSolved(np.array(s1)))
            
            return {'r': answer, 'revised': revised_flag}
            
        except Exception as e:
            print(e)
            return {'r': -1, 'revised': revised_flag}
    
    def test_output_multi(self, inputs, outputs, revised_flag):
        moves_list =  re.findall(r"\d+\.\sRestoration Moves:\s(.+)", outputs)  
        try:
            revised_flag.extend([None]*(len(moves_list)-len(revised_flag)))
        except:
             revised_flag = [False] * len(moves_list)

        return_ = dict()
        for idx, moves in enumerate(moves_list):
            try:
                moves = moves.strip()
                s1 = doAlgStr(inputs, moves)
                answer = int(isSolved(np.array(s1)))
                return_['r%s'%(idx)] = {'r': answer, 'revised': revised_flag[idx]}
            except Exception as e:
                print(e)
                return_['r%s'%(idx)] = {'r': -1, 'revised': revised_flag[idx]}

        return {'r': return_} 

    def value_outputs_unwrap(self, x: str, y: str, value_outputs: list) -> float:

        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value

    def select_outputs_unwrap(self, x: str, y: str, select_outputs: list, multi_solution) -> float:
  
        select_names = select_outputs[0].split('[Best Next Move End]')[0].strip().split('\n')
        result = []
        for s in select_names:
            input_str = s.strip().split("\n")[-1].rstrip("\n")
           
            match = re.search(r'\((\d+)\)', input_str)
            if match:  
                number = int(match.group(1))  
                result.append(number)
            else:  
                print('No number found inside parentheses.') 
                continue 

        return result
    
    def action_to_thoughs(self, actions, x):
        return '\n'.join(actions)
    
    def extract_top_select(self, select_new_ys):
        res = []
        for item in select_new_ys:
            top_select_new_ys = item.strip().split('\n')
            res.append(" ".join(top_select_new_ys))
        return  res