# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import re
import os
import sympy
import pandas as pd
from .prompts.prompts_game24 import * 

class Game24Prompter():
    """
    Game24Prompter provides the generation of prompts specific to the game24
    example for the language models.
    """
    def __init__(self, last_step=True):
        self.last_step = int(last_step)
        self.value_cache = {}
    
    def get_current_numbers(self, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        return last_line.split('left: ')[-1].split(')')[0]

    def format_thoughts_withExp(self, question: str, steps: str) -> str:

        parts = steps.strip().split("\n")
        question = question.split(" ")  
        current_terms = question[:]
        result = ""  
        question = [float(n) for n in question]
        
        for step in parts[:]: 
           
            # print('step', step)
            operation = step.split(" (left")[0]
            op_ = operation.replace("(", "").replace(")", "").replace("(approximately)", "").split(" ")
            # print((op_, 'op_')) 
            num1, symbol, num2, result_num = op_[0], op_[1], op_[2], op_[4]

            if eval(num1) in question:
                question.remove(eval(num1))  
            if eval(num2) in question:  
                question.remove(eval(num2))  

            question.append(eval(result_num.replace('...', '')))  
            question_in_str = [str(int(n)) if int(n) == n else str(n) for n in question]

            try:
                # print('current_terms', current_terms)
                # print('num1', num1, 'num2', num2)
                for term in current_terms:
                    if eval(num1) == eval(term):
                        new_exp_left = term
                        current_terms.remove(term)
                        break
                for term in current_terms:
                    if eval(num2) == eval(term):
                        new_exp_right = term
                        current_terms.remove(term)
                        break
                    
                new_exp = f'({new_exp_left}) {symbol} ({new_exp_right})'
                current_terms.append(new_exp)
                result += f"{num1} {symbol} {num2} = {result_num} (left: {' '.join(question_in_str)}) Expression: {', '.join(current_terms)}\n"
            except:
                result += f"{num1} {symbol} {num2} = {result_num} (left: {' '.join(question_in_str)})\n"
            

        return result  

    def get_instruction_prompt(self) -> str:
            return game24_instruct

    def standard_prompt_wrap(self, x, y='') -> str:
        s = " ".join(map(str, x.tolist()))
        return standard_prompt.format(state=s) + y
    
    def standard_prompt_wrap_multi(self, x, y='') -> str:
        s = " ".join(map(str, x.tolist()))
        return standard_prompt_multi.format(state=s) + y

    def cot_prompt_wrap(self, x: str, y:str='') -> str:
        s = " ".join(map(str, x.tolist()))
        return cot_prompt.format(state=s) + y
    
    def cot_prompt_wrap_multi(self, x: str, y:str='') -> str:
        s = " ".join(map(str, x.tolist()))
        return cot_prompt_multi.format(state=s) + y
    
    def xot_prompt_wrap(self, x, y) -> str:
        s = " ".join(map(str, x.tolist()))
        if self.last_step:
            y_ = "\n".join(y)
            move_ = self.format_thoughts_withExp(s, y_)
            prompt = game24_xot_prompt.format(state=s, move=move_)
        else:
            y_ = "\n".join(y[:-1])
            move_ = self.format_thoughts_withExp(s, y_)
            prompt = game24_xot_prompt_wo_laststep.format(state=s, move=move_)
 
        return prompt, move_
    
    def xot_prompt_multi_wrap(self, x, y) -> str:
        s = " ".join(map(str, x.tolist()))
        moves = ''
        for idx, ys in enumerate(y):
            ys_ = '\n'.join(ys)
            move_ = self.format_thoughts_withExp(s, ys_)
            moves += '[Solution %s]:%s\n'%(idx+1, move_)
        prompt = game24_xot_prompt_multi.format(state=s, move=moves)
 
        return prompt, move_
    
    def xot_prompt_revised_wrap(self, x, y='') -> str:
        s = " ".join(map(str, x.tolist()))
        y_withExp = self.format_thoughts_withExp(s, '\n'.join(y)).strip().split('\n')
        # print('y_withExp', y_withExp)
        move_ = ""
        
        for idx in range(len(y_withExp)):
            move_ += '[Steps %s] %s\n'%(idx+1, y_withExp[idx])
    
        prompt = game24_xot_revised_prompt.format(state=s, move=move_)
        return prompt, move_

    def propose_prompt_wrap(self, x, y, isFinished) -> str:
        s = " ".join(map(str, x.tolist()))
        
        current_numbers = self.get_current_numbers(y if y else s)
        # print('current_numbers', current_numbers)
        if current_numbers == '24' or isFinished:
            # with Exp
            move_ = self.format_thoughts_withExp(s, y)
            prompt = game24_xot_prompt.format(state=s, move=move_)

            return prompt, move_
        else:
            prompt = propose_prompt.format(state=current_numbers)
            return prompt, current_numbers
    

    def select_prompt_wrap(self, x: str, ys: list, n_select_sample=1) -> str:
        proposal = ''
        # print('ys', ys)
        s = " ".join(map(str, x.tolist()))
        try:
            second_last_line = ys[0].strip().split('\n')[-2]
            current_numbers = self.get_current_numbers(second_last_line)
    
        except:
            current_numbers = s
        for idx, y in enumerate(ys):
            last_line = y.strip().split('\n')[-1]
            proposal += '(%s) '%(idx+1) + last_line + '\n'
        # input()
        if n_select_sample == 3:
            return merge_prompt_multi.format(n_select_sample=n_select_sample, state=current_numbers, proposal=proposal)
        else:
            return merge_prompt.format(n_select_sample=n_select_sample, state=current_numbers, proposal=proposal)


    def value_prompt_wrap(self, x: str, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        if 'left: ' not in last_line:  # last step
            ans = last_line.lower().replace('answer: ', '')
            # print([value_last_step_prompt.format(state=x, answer=ans)])
            return value_last_step_prompt.format(state=x, answer=ans)
        current_numbers = self.get_current_numbers(y)
        return value_prompt.format(state=current_numbers)
    