# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import itertools
import random

class ToT_Solver:
    def __init__(self, args, gpt, game, prompter, parser, to_print=False):
        """
        Initialize the ToT_Solver with the necessary components.

        Args:
            args: The arguments for the solver.
            gpt: The GPT model to be used in the solver.
            game: The game or simulation to be solved.
            prompter: The prompter for generating prompts for the GPT model.
            parser: The parser for parsing the output of the GPT model.
            to_print (bool, optional): A flag indicating whether to print debug information. Defaults to False.
        """
        self.args = args
        self.gpt = gpt
        self.game = game
        self.prompter = prompter
        self.parser = parser
        self.to_print = to_print
    
    def get_max_index(self, lst):
        """
        This function returns the index of the maximum value in a list.

        Args:
            lst (list): The list in which the maximum value is to be found.
        
        Returns:
            max_indices: The index of the maximum value in the list.
        """
        max_value = max(lst)
        max_indices = [index for index, value in enumerate(lst) if value == max_value]
        return random.choice(max_indices)

    def get_proposals(self, args, gpt, prompter, x, y, isFinished): 
        """
        This function generates proposals for a partial output 'y' using the 'get_proposals' method.

        Args:
            args (gpt): The arguments to be passed to the 'get_proposals' method.
            gpt: The GPT model to be used in the 'get_proposals' method.
            prompter: The prompter to be used in the 'get_proposals' method.
            x: The input to be passed to the 'get_proposals' method.
            y: The partial output for which proposals are to be generated.
            isFinished (bool): A flag indicating whether the partial output 'y' is a complete output.
        
        Returns:
            proposals: A list of generated proposals.
            current_state: The current state of the game after the partial output 'y' is applied.
        """
        instruct = prompter.get_instruction_prompt()
        propose_prompt, current_state = prompter.propose_prompt_wrap(x, y, isFinished)
        
        proposals = gpt(propose_prompt, instruct, n=args.param.n_generate_sample, stop=args.gpt.stop)[0]
        if self.to_print:
            print('propose_prompt', propose_prompt)
            print('proposals', proposals)

        if isFinished:
            return [proposals + '\n'], current_state
        else:
            if args.env == 'game24':
                proposals_precheck = proposals.strip().split('\n')
                proposals_aftercheck = []
                for idx, p in enumerate(proposals_precheck):
                    try:
                        exp = p.lower().split("=")[0].strip()
                        terms = exp.split(' ')
                        num1, _, num2 = terms[0], terms[1], terms[2]
                        if num1 in current_state and num2 in current_state:
                                res = eval(exp)
                                proposals_aftercheck.append(p)
                    except:
                        continue
            else:
                proposals_aftercheck = proposals.replace('\n', '').strip().split(', ')
            
            return [y + _ + '\n' for _ in proposals_aftercheck], current_state
    

    def get_value_tot(self, args, gpt, prompter, parser, x, y, cache_value=True):
        """
        This function calculates the total value for a partial output 'y' using the 'get_value' method.
        It uses a local cache to avoid duplicate calculations.

        Args:
            args (gpt): The arguments to be passed to the 'get_value' method.
            gpt: The GPT model to be used in the 'get_value' method.
            prompter: The prompter to be used in the 'get_value' method.
            parser: The parser to be used in the 'get_value' method.
            x: The input to be passed to the 'get_value' method.
            y: The partial output for which the total value is to be calculated.
            cache_value (bool, optional): A flag indicating whether to cache the calculated values. Defaults to True.
        
        Returns:
            value: The calculated value for the partial output 'y'.
        """
        instruct = prompter.get_instruction_prompt()
        value_prompt = prompter.value_prompt_wrap(x, y)
        
        if cache_value and value_prompt in prompter.value_cache:
            return prompter.value_cache[value_prompt]
        value_outputs = gpt(value_prompt, instruct, n=args.param.n_generate_sample, stop=args.gpt.stop)
        value = parser.value_outputs_unwrap(x, y, value_outputs)
        
        if self.to_print:
            print('value_prompt', value_prompt)
            print('value_outputs', value_outputs)
    
        if cache_value:
            prompter.value_cache[value_prompt] = value
        return value


    def get_values_tot(self, args, gpt, prompter, parser, x, ys, cache_value=True):
        """
        This function calculates the total value for each partial output in 'ys' using the 'get_value_tot' method.
        It uses a local cache to avoid duplicate calculations.

        Args:
            args (gpt): The arguments to be passed to the 'get_value_tot' method.
            gpt: The GPT model to be used in the 'get_value_tot' method.
            prompter: The prompter to be used in the 'get_value_tot' method.
            parser: The parser to be used in the 'get_value_tot' method.
            x: The input to be passed to the 'get_value_tot' method.
            ys (list): A list of partial outputs for which the total value is to be calculated.
            cache_value (bool, optional): A flag indicating whether to cache the calculated values. Defaults to True.

        Returns:
            values: A list of calculated values for each partial output in 'ys'.
        """
        values = []
        local_value_cache = {}
        for y in ys:  # each partial output
            if y in local_value_cache:  # avoid duplicate calculations
                value = 0
            else:    
                value = self.get_value_tot(args, gpt, prompter, parser, x, y, cache_value=cache_value)
                local_value_cache[y] = value
            values.append(value)
        return values
    

    def solve(self, idx):
        """_summary_
        Parameters:
            idx: index of the test board

        Return:
            ys: a list of solutions
            info: a dictionary of information
        """
        x = self.game.getOneTestBoard(idx)


        if self.args.multi_solution and self.args.env == 'cube':
            total_game_step = self.args.task.total_game_step + 3
        elif self.args.multi_solution and self.args.env == 'npuzzle':
            total_game_step = self.args.task.total_game_step + 3
        elif not self.args.param.last_step and self.args.env == 'game24':
            total_game_step = self.args.task.total_game_step - 1
        else: 
            total_game_step = self.args.task.total_game_step


        ys = ['']  # current output candidates
        infos = []
        isFinished = False
        for step in range(total_game_step+1):
            if self.to_print:
                print('Current Step: %s'%(step+1))
            # generation
            new_ys = []
            for y in ys:
                ys_, current_state = self.get_proposals(self.args, self.gpt, self.prompter, x, y, isFinished)
                new_ys.append(ys_)
                
            new_ys = list(itertools.chain(*new_ys))

            if self.to_print:
                print('new_ys', new_ys)

            if isFinished:
                infos.append({'step': step, 'x': str(x), 'thoughts': ys, 'answer': new_ys})
                ys = new_ys
                break
        
            # evaluation
            values = self.get_values_tot(self.args, self.gpt, self.prompter, self.parser, x, new_ys)
            if len(values) == 0:
                isFinished = True
                continue

            # selection
            if self.args.param.n_select_sample == 1: # b=1
                max_values = max(values)
                select_ids = [self.get_max_index(values)]
                select_new_ys = [new_ys[select_id] for select_id in select_ids]
            else:
                ids = list(range(len(new_ys)))
                max_values = max(values)
                select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:self.args.param.n_select_sample]
                select_new_ys = [new_ys[select_id] for select_id in select_ids]

            # log
            if self.to_print: 
                sorted_new_ys, sorted_values = zip(*sorted(zip(new_ys, values), key=lambda x: x[1], reverse=True))
                print(f'-- new_ys --: {sorted_new_ys}\n-- sol values --: {sorted_values}\n-- choices --: {select_new_ys}\n')
            
            infos.append({'step': step, 'x': str(x), 'ys': ys, 'new_ys': new_ys, 'values': values, 'select_new_ys': select_new_ys})
            ys = select_new_ys

            if self.args.env == 'game24':
                isFinished = step == total_game_step - 1 # or float(max_values) == 0.001
            else:
                moves = self.parser.extract_top_select(select_new_ys)
                # Condition to Stop: 1. One of the candiates Reach the Correct Answer; 2. Reach the maximum step; 3. only left impossible answer
                success = False
                for m in moves:
                    success = success or self.game.isFinishing(x, m) 
                isFinished = success or step == total_game_step - 1 # or float(max_values) == 0.001 

        if self.to_print: 
            print(ys)

        info = {'steps': infos}

        return ys, info
    
    