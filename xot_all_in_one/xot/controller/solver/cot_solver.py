# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

class CoT_Solver:
    def __init__(self, args, gpt, game, prompter, parser, to_print=False):
        self.args = args
        self.gpt = gpt
        self.game = game
        self.prompter = prompter
        self.parser = parser
        self.to_print = to_print


    def solve(self, idx):
        '''_summary_
        Parameters:
            idx: index of the test board
        
        Return:
            ys: a list of solutions
            info: a dictionary of information
        '''
        x = self.game.getOneTestBoard(idx)
        y = ''

        if not self.args.multi_solution:
            prompt = self.prompter.cot_prompt_wrap(x, y)
        else:
            prompt = self.prompter.cot_prompt_wrap_multi(x, y)
        instruct = self.prompter.get_instruction_prompt()
        samples = self.gpt(prompt, instruct, n=self.args.param.n_generate_sample, stop=self.args.gpt.stop)

        ys= [y + _ for _ in samples]
        if self.to_print:
            print('cot_solve -- input: ', x)
            print('cot_solve -- prompt: ', prompt)
            print('cot_solve -- output: ', samples)

        info = {}
        
        return ys, info
    
    
        