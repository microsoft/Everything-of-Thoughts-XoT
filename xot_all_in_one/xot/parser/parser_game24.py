# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import re
import os
import sympy
import pandas as pd
import numpy as np


class Game24Parser():
    """
    Game24Paser provides the parsing of language model reponses specific to
    the game24 example.
    """
    def __init__(self):
        pass

    def get_input(self, idx: int) -> str:
        return self.data[idx]
    
    def convert_to_numbers(self, input_list):  
        result = []  
        for item in input_list:  
            try:  
                num = int(item)  
            except ValueError:  
                try:  
                    num = float(item)  
                except ValueError:  
                    continue  
            result.append(num)  
        return result  

    
    def get_revised_state(self, x, thoughts, incorrect_step):
        move = thoughts[incorrect_step-1]
        left_num = move.split('(left:')[-1].split(')')[0].strip().split(' ')
        exp = move.split('(left:')[0].strip().split(' ')
        n1, n2, res = exp[0], exp[2], exp[4]
        left_num.remove(res)
        left_num.extend([n1, n2])
        left_num = self.convert_to_numbers(left_num)
        return np.array(left_num)

    def test_output(self, inputs, outputs, revised_flag):
        try:
            expression = outputs.strip().split('\n')[-1].lower().replace('answer: ', '').split('=')[0]
            numbers = re.findall(r'\d+', expression)
            problem_numbers  = inputs.tolist()
            numbers = self.convert_to_numbers(numbers)

            if sorted(numbers) != sorted(problem_numbers):
                return {'r': 0, 'revised': revised_flag}
            try:
                # print(sympy.simplify(expression))
                return {'r': int(sympy.simplify(expression) == 24), 'revised': revised_flag}
            except Exception as e:
                # print(e)
                return {'r': 0, 'revised': revised_flag}
        except Exception as e:
                # print(e)
                return {'r': 0, 'revised': revised_flag}
    
    def test_output_multi(self, inputs, outputs, revised_flag):
            
            moves_list =  re.findall(r"answer\s*\d*:\s*(.*)", outputs.lower())  
            try:
                revised_flag.extend([None]*(len(moves_list)-len(revised_flag)))
            except:
                revised_flag = [False] * len(moves_list)
           
            return_ = dict()
            for idx, exp in enumerate(moves_list):
                try:
                    expression = exp.strip().split('\n')[-1].lower().replace('answer: ', '').split('=')[0]
                    numbers = re.findall(r'\d+', expression)
                    problem_numbers = inputs.tolist()
                    numbers = self.convert_to_numbers(numbers)
            
                    if sorted(numbers) != sorted(problem_numbers):
                        return_['r%s'%(idx)] = {'r': 0, 'revised': revised_flag[idx]}
                    else:
                        return_['r%s'%(idx)] = {'r': int(sympy.simplify(expression) == 24), 'revised': revised_flag[idx]}
                except Exception as e:
                    print(e)
                    return_['r%s'%(idx)] = {'r': -1, 'revised': revised_flag[idx]}

            if len(return_) == 0:
                return_['r0'] = {'r': -1, 'revised': None}

            return {'r': return_}
    
        

    def value_outputs_unwrap(self, x: str, y: str, value_outputs: list) -> float:
        if len(y.strip().split('\n')) == 4 and 'answer' not in y.lower():
            return 0
        value_names = [_.split('\n')[-1] for _ in value_outputs]
        value_map = {'impossible': 0.001, 'likely': 1, 'sure': 20}  # TODO: ad hoc
        value = sum(value * value_names.count(name) for name, value in value_map.items())
        return value

    def select_outputs_unwrap(self, x: str, y: str, select_outputs: list, got_multi: bool) -> float:
        # if got_multi:
        select_names = select_outputs[0].split('\n')
       
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
    
        # else:
        #     select_names = [_.split('\n')[-1] for _ in select_outputs]
        #     result = [s for s in y if s.strip().split("\n")[-1].rstrip("\n") in select_names] 
        #     return result
    
    def action_to_thoughs(self, actions, x):
        
        current_number = x.tolist()
        result = []  
        for item in actions:  
            if item[0] == '-':  
                calculation = item[1] - item[2]  
            elif item[0] == '*':  
                calculation = item[1] * item[2]  
            elif item[0] == '+':  
                calculation = item[1] + item[2]  
            elif item[0] == '/':  
                calculation = item[1] / item[2]  
            
            current_number.append(calculation)
            current_number.remove(item[1])
            current_number.remove(item[2])
            # print(current_number)
            left_num = " ".join(map(str, current_number))
            result.append(f"{item[1]} {item[0]} {item[2]} = {calculation} (left: {left_num})")  
      
        return result  
    