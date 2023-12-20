# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import itertools
import random

class GoT_Solver:
    """
    A class used to solve a game using a GPT model.

    ...

    Attributes
    ----------
    args : object
        a configuration object with various parameters
    gpt : object
        a GPT model used for generating proposals and selections
    game : object
        a game object representing the current state of the game
    prompter : object
        an object used to generate prompts for the GPT model
    parser : object
        an object used to parse the outputs of the GPT model

    Methods
    -------
    get_proposals(args, gpt, prompter, x, y, isFinished)
        Generates a set of proposals or possible solutions to the game.
    get_select_got(args, gpt, prompter, parser, x, ys, cache_value=True)
        Selects the best proposal from a set of proposals.
    solve(idx)
        Solves the game by generating proposals and selecting the best ones until the game is finished.
    """
    def __init__(self, args, gpt, game, prompter, parser, to_print=False):
        """Initializes the GoT_Solver with the given arguments."""
        self.args = args
        self.gpt = gpt
        self.game = game
        self.prompter = prompter
        self.parser = parser
        self.to_print = to_print
    
    
    def get_proposals(self, args, gpt, prompter, x, y, isFinished):
        """
        Generates a set of proposals or possible solutions to the game.

        Parameters:
        args (object): a configuration object with various parameters
        gpt (object): a GPT model used for generating proposals
        prompter (object): an object used to generate prompts for the GPT model
        x (object): the current state of the game
        y (object): the current output candidates
        isFinished (bool): a flag indicating whether the game is finished or not

        Returns:
        list: a list of proposals
        object: the current state of the game
        """
        # Get instruction prompt
        instruct = prompter.get_instruction_prompt()
        # Get propose prompt and current state
        propose_prompt, current_state = prompter.propose_prompt_wrap(x, y, isFinished)
        # Generate proposals
        proposals = gpt(propose_prompt, instruct, n=args.param.n_generate_sample, stop=args.gpt.stop)[0]

        # Print propose prompt and proposals if in debug mode
        if self.to_print:
            print('propose_prompt', propose_prompt)
            print('proposals', proposals)

        # If game is finished, return proposals
        if isFinished:
            return [proposals + '\n'], current_state
        else:
            # If game environment is 'game24', perform precheck on proposals
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
                # If game environment is not 'game24', split proposals
                proposals_aftercheck = proposals.replace('\n', '').strip().split(', ')
            
            # Return proposals after check
            return [y + _ + '\n' for _ in proposals_aftercheck], current_state


    def get_select_got(self, args, gpt, prompter, parser, x, ys, cache_value=True):
        """
        Selects the best proposal from a set of proposals.

        Parameters:
        args (object): a configuration object with various parameters
        gpt (object): a GPT model used for generating selections
        prompter (object): an object used to generate prompts for the GPT model
        parser (object): an object used to parse the outputs of the GPT model
        x (object): the current state of the game
        ys (list): a list of proposals
        cache_value (bool): a flag indicating whether to cache the value or not

        Returns:
        list: a list of selected proposals
        """
        # Get instruction prompt
        instruct = prompter.get_instruction_prompt()
        # Get select prompt
        select_prompt = prompter.select_prompt_wrap(x, ys, args.param.n_select_sample)
        # Generate select outputs
        select_outputs = gpt(select_prompt, instruct, n=args.param.n_generate_sample, stop=args.gpt.stop)
        # Unwrap select outputs and select the best one
        select = parser.select_outputs_unwrap(x, ys, select_outputs, args.multi_solution)

        # Print select prompt and select outputs if in debug mode
        if self.to_print:
            print('select_prompt', select_prompt)
            print('select_outputs', select_outputs)
 
        # Return selected proposals
        return select


    def solve(self, idx):
        """
        Solves the game by generating proposals and selecting the best ones until the game is finished.

        Parameters:
        idx (int): the index of the game to be solved

        Returns:
        list: a list of final proposals
        dict: a dictionary of steps taken to solve the game
        """
        # Get one test board from the game
        x = self.game.getOneTestBoard(idx)

        # Set total game step based on the game environment and whether multiple solutions are allowed
        if self.args.multi_solution and self.args.env == 'cube':
            total_game_step = self.args.task.total_game_step + 3
        elif self.args.multi_solution and self.args.env == 'npuzzle':
            total_game_step = self.args.task.total_game_step + 3
        elif not self.args.param.last_step and self.args.env == 'game24':
            total_game_step = self.args.task.total_game_step - 1
        else: 
            total_game_step = self.args.task.total_game_step

        # Initialize current output candidates and other variables
        ys = ['']  
        infos = []
        isFinished = False

        # Start solving the game
        for step in range(total_game_step+1):
            # Generation phase
            new_ys = []

            for y in ys:
                # Generate proposals
                ys_, current_state = self.get_proposals(self.args, self.gpt, self.prompter, x, y, isFinished)
                new_ys.append(ys_)
                
            new_ys = list(itertools.chain(*new_ys))

            # If game is finished, log information and break the loop
            if isFinished:
                infos.append({'step': step, 'x': str(x), 'thoughts': ys, 'answer': new_ys})
                ys = new_ys
                break

            # If there's no new candidates, it's impossible to reach the answer: early stop
            if len(new_ys) == 0:
                isFinished = True
                select_new_ys = ys[:min(self.args.param.n_select_sample, len(ys))]
                ys = select_new_ys
                infos.append({'step': step, 'x': str(x), 'ys': ys, 'new_ys': new_ys, 'select': [], 'select_new_ys': select_new_ys})
                continue
        
            # Evaluation phase
            # Select the best proposals
            select = self.get_select_got(self.args, self.gpt, self.prompter, self.parser, x, new_ys)

            # Print select and new proposals if in debug mode
            if self.to_print:
                print('select', select)
                print('ys', ys)
                print('new_ys', new_ys)

            # Preselect new proposals
            select_new_ys_pre = []
            for m in select:
                idx = m - 1
                select_new_ys_pre.append(new_ys[idx])
            
            # Select new proposals
            if len(select_new_ys_pre) > 0:
                select_new_ys = select_new_ys_pre[:min(self.args.param.n_select_sample, len(select_new_ys_pre))]
            else:
                select_new_ys = ys[:min(self.args.param.n_select_sample, len(ys))]

            # Log information
            if self.to_print: 
                print('select_new_ys_pre', select_new_ys_pre)
                print('select_new_ys', select_new_ys)
                print(f'select --: {select}\n-- choices --: {select_new_ys}\n')
            
            infos.append({'step': step, 'x': str(x), 'ys': ys, 'new_ys': new_ys, 'select': select, 'select_new_ys': select_new_ys})
            ys = select_new_ys

            # Check if game is finished
            if self.args.env == 'game24':
                isFinished = step == total_game_step - 1
            else:
                moves = self.parser.extract_top_select(select_new_ys)
                # Condition to Stop: 1. One of the candiates Reach the Correct Answer; 2. Reach the maximum step; 3. only left impossible answer
                success = False
                for m in moves:
                    success = success or self.game.isFinishing(x, m) 
                isFinished = success or step == total_game_step - 1

        # Print final proposals if in debug mode
        if self.to_print: 
            print(ys)
        # Return final proposals and steps taken to solve the game
        return ys, {'steps': infos}