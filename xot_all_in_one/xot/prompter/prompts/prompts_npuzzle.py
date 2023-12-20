# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

npuzzle_instruct = """You are a virtual expert in solving a 8-puzzle problrm. Please follow the instructions and rules below to complete the solving.
Your goal is to reach the goal state with valid moves.
[The goal state]
0 1 2 
3 4 5 
6 7 8 

[Instructions]
The 8-puzzle consists of a 3x3 grid containing 8 numbered tiles (from 1 to 8) and one empty space (denoted by 0). 
Only 0 can be moved horizontally or vertically, and the objective is to reach the goal state from a given initial state. 
The goal state is typically the numbers ordered sequentially, with the 0 in the first position:
[The goal state]
0 1 2 
3 4 5 
6 7 8 
 
[Rules]
1. Only 0 can be moved horizontally or vertically.
2. Each move is chosen from the following set of options:
- 'Left': move 0 to the left
- 'Down': move 0 downward
- 'Right': move 0 to the right
- 'Up': move 0 upward

For example:
Before move:
1 2 3  
4 0 6  
7 8 5 
After move 'Left':
1 2 3  
0 4 6 
7 8 5 

Before move:
1 2 3  
4 0 6  
7 8 5 
After move 'Down':
1 2 3  
4 8 6  
7 0 5 

Before move:
1 2 3  
4 0 6  
7 8 5 
After move 'Right':
1 2 3  
4 6 0  
7 8 5 

Before move:
1 2 3  
4 0 6  
7 8 5 
After move 'Up':
1 0 3  
4 2 6  
7 8 5

3. The next move must be chosen from the valid move set depending on the position of '0'.
For example:
p1  p2  p3 
p4  p5  p6 
p7  p8  p9 
(1) If '0' is located at position 'p1', the valid move set is ['Right', 'Down'].
(2) If '0' is located at position 'p2', the valid move set is ['Left', 'Right', 'Down'].
(3) If '0' is located at position 'p3', the valid move set is ['Left', 'Down'].
(4) If '0' is located at position 'p4', the valid move set is ['Right', 'Up', 'Down'].
(5) If '0' is located at position 'p5', the valid move set is ['Left', 'Right', 'Up', 'Down'].
(6) If '0' is located at position 'p6', the valid move set is ['Left', 'Up', 'Down'].
(7) If '0' is located at position 'p7', the valid move set is ['Right', 'Up'].
(8) If '0' is located at position 'p8', the valid move set is ['Left, 'Right', 'Up'].
(9) If '0' is located at position 'p9', the valid move set is ['Left', 'Up'].

4. Diagonal moves are not allowed.
5. The objective is to return the moves which can reach the goal state.
"""


npuzzle_prompt_io = """
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 

[Initial State]:
3 1 2
6 4 5
7 8 0
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 
[Moves]:
Left, Left, Up, Up

[Initial State]:
3 1 2
6 4 5
0 7 8
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 
[Moves]:
Up, Up

[Initial State]:
3 1 2
4 0 5
6 7 8
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 
[Moves]:
Left, Up

[Initial State]:
{state}
"""

npuzzle_prompt_io_multi = """
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find 3 correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
** If you have found threee correct answer, terminate and return. **

[Initial State]:
3 1 2
6 4 5
0 7 8
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
** If you have found threee correct answer, terminate and return. **
1. Moves: Up, Up

[Initial State]:
3 1 2
4 0 5
6 7 8
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
** If you have found threee correct answer, terminate and return. **
1. Moves: Left, Up

[Initial State]:
1 4 2
0 3 5
6 7 8
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
** If you have found threee correct answer, terminate and return. **
1. Moves: Right, Up, Left
2. Moves: Down, Up, Right, Up, Left

[Initial State]:
1 4 2 
3 7 5 
0 6 8
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
** If you have found threee correct answer, terminate and return. **
1. Moves: Right, Up, Up, Left
2. Moves: Right, Right, Left, Up, Up, Left
3. Moves: Right, Up, Left, Right, Up, Left

[Initial State]:
{state}
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
** If you have found three correct answer, terminate and return. **
"""

# Please complete the moves and return the cube state after all moves.
npuzzle_prompt_cot = """
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 

[Initial State]:
3 1 2
6 4 5
7 8 0
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 
[Process] 
3 1 2
6 4 5
7 8 0
Step 1: Choose one valid move from: [Left, Up]
Move: Left
Current State:
3 1 2
6 4 5
7 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Move: Left
Current State:
3 1 2
6 4 5
0 7 8
Step 3: Choose one valid move from: [Right, Up]
Move: Up
Current State:
3 1 2
0 4 5
6 7 8
Step 4: Choose one valid move from: [Right, Up]
Move: Up
Current State:
0 1 2
3 4 5
6 7 8
Finished.
[Moves]:
Left, Left, Up, Up


[Initial State]:
3 1 2
6 4 5
0 7 8
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 
[Process] 
3 1 2
6 4 5
0 7 8
Step 1: Choose one valid move from: [Right, Up]
Move: Up
Current State:
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Down, Up]
Move: Up
Current State:
0 1 2
3 4 5
6 7 8
Finished.
[Moves]:
Up, Up

[Initial State]:
3 1 2
4 0 5
6 7 8
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 
[Process] 
Current State:
3 1 2
4 0 5
6 7 8
Step 1: Choose one valid move from: [Left, Right, Up, Down]
Move: Left
Current State:
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Up, Down]
Move: Up
Current State:
0 1 2
3 4 5
6 7 8
Finished.
[Moves]:
Left, Up

[Initial State]:
{state}
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. ** 
[Process]
"""

npuzzle_prompt_cot_multi = '''
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
**DO NOT PROVIDE ANY SOLUTION WITH > 12 STEPS!**

[Initial State]:
3 1 2
6 4 5
0 7 8
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution.**
**DO NOT PROVIDE ANY SOLUTION WITH > 12 STEPS!**
[Solution 1] 
[Process] 
Current State:
3 1 2
6 4 5
0 7 8
Step 1: Choose one valid move from: [Right, Up]
Move: Up
Current State:
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Up, Down]
Move: Up
Current State:
0 1 2
3 4 5
6 7 8
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
Finished.
1. Moves: Up, Up


[Initial State]:
1 4 2
0 3 5
6 7 8
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution.**
**DO NOT PROVIDE ANY SOLUTION WITH > 12 STEPS!**
[Solution 1] 
[Process] 
Current State:
1 4 2
0 3 5
6 7 8
Step 1: Choose one valid move from: [Right, Up, Down]
Move: Right
Current State:
1 4 2
3 0 5
6 7 8
Step 2: Choose one valid move from: [Left, Right, Up, Down]
Move: Up
Current State:
1 0 2
3 4 5
6 7 8
Step 3: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2
3 4 5
6 7 8
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
Finished.
Now strictly follow the above process to form Moves.
1. Moves: Right, Up, Left
[Solution 2] 
[Process] 
Current State:
1 4 2
0 3 5
6 7 8
Step 1: Choose one valid move from: [Right, Up, Down]
Move: Down
Current State:
1 4 2
6 3 5
0 7 8
Step 2: Choose one valid move from: [Right, Up]
Move: Up
Current State:
1 4 2
0 3 5
6 7 8
Step 3: Choose one valid move from: [Right, Up, Down]
Move: Right
Current State:
1 4 2
3 0 5
6 7 8
Step 4: Choose one valid move from: [Left, Right, Up, Down]
Move: Up
Current State:
1 0 2
3 4 5
6 7 8
Step 5: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2
3 4 5
6 7 8
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
Finished.
Now strictly follow the above process to form Moves.
2. Moves: Down, Up, Right, Up, Left


[Initial State]:
3 1 2
4 0 5
6 7 8
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution.**
**DO NOT PROVIDE ANY SOLUTION WITH > 12 STEPS!**
[Solution 1] 
[Process] 
Current State:
3 1 2
4 0 5
6 7 8
Step 1: Choose one valid move from: [Left, Right, Up, Down]
Move: Left
Current State:
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Up, Down]
Move: Up
Current State:
0 1 2
3 4 5
6 7 8
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
Finished.
Now strictly follow the above process to form Moves.
1. Moves: Left, Up


[Initial State]:
1 4 2 
3 7 5 
0 6 8
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution.**
**DO NOT PROVIDE ANY SOLUTION WITH > 12 STEPS!**
[Solution 1] 
[Process] 
Current State:
1 4 2 
3 7 5 
0 6 8
Step 1: Choose one valid move from: [Right, Up]
Move: Right
Current State:
1 4 2 
3 7 5 
6 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 4 2 
3 0 5 
6 7 8
Step 3: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 0 2 
3 4 5 
6 7 8
Step 4: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2 
3 4 5 
6 7 8
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
Finished.
Now strictly follow the above process to form Moves.
1. Moves: Right, Up, Up, Left
[Solution 2] 
[Process] 
Current State:
1 4 2 
3 7 5 
0 6 8
Step 1: Choose one valid move from: [Right, Up]
Move: Right
Current State:
1 4 2 
3 7 5 
6 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Move: Right
Current State:
1 4 2 
3 7 5 
6 8 0
Step 3: Choose one valid move from: [Left, Up]
Move: Left
Current State:
1 4 2 
3 7 5 
6 0 8
Step 4: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 4 2 
3 0 5 
6 7 8
Step 5: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 0 2 
3 4 5 
6 7 8
Step 6: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2 
3 4 5 
6 7 8
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
Finished.
Now strictly follow the above process to form Moves.
2. Moves: Right, Right, Left, Up, Up, Left
[Solution 3] 
[Process] 
Current State:
1 4 2 
3 7 5 
0 6 8
Step 1: Choose one valid move from: [Right, Up]
Move: Right
Current State:
1 4 2 
3 7 5 
6 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 4 2 
3 0 5 
6 7 8
Step 3: Choose one valid move from: [Left, Right, Up, Down]
Move: Left
Current State:
1 4 2 
0 3 5 
6 7 8
Step 4: Choose one valid move from: [Right, Up, Down]
Move: Right
Current State:
1 4 2 
3 0 5 
6 7 8
Step 5: Choose one valid move from: [Left, Right, Up, Down]
Move: Up
Current State:
1 0 2 
3 4 5 
6 7 8
Step 6: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2 
3 4 5 
6 7 8
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
Finished.
Now strictly follow the above process to form Moves.
3. Moves: Right, Up, Left, Right, Up, Left

All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
**You MUST solved the problem within 12 steps. DO NOT exceed 12 steps. **
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
**DO NOT PROVIDE ANY SOLUTION WITH > 12 STEPS!**
[Initial State]:
{state}
'''


npuzzle_prompt_pro_wo_laststap = """
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. **  The last step is not provided. Please complete the last step and return the answer. 

[Initial State]:
3 1 2
6 4 5
7 8 0
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. **  The last step is not provided. Please complete the last step and return the answer. 
[Process] 
3 1 2
6 4 5
7 8 0
Choose one valid move from: [Left, Up]
Step 1: 
Left
3 1 2
6 4 5
7 0 8
Choose one valid move from: [Left, Right, Up]
Step 2: 
Left
3 1 2
6 4 5
0 7 8
Choose one valid move from: [Right, Up]
Step 3: 
Up
3 1 2
0 4 5
6 7 8
Choose one valid move from: [Right, Up]
The last chosen step is:
Up
0 1 2
3 4 5
6 7 8
Finished.
[Moves]:
Left, Left, Up, Up


[Initial State]:
3 1 2
6 4 5
0 7 8
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. **  The last step is not provided. Please complete the last step and return the answer. 
[Process] 
3 1 2
6 4 5
0 7 8
Choose one valid move from: [Right, Up]
Step 1: 
Up
3 1 2
0 4 5
6 7 8
Choose one valid move from: [Right, Down, Up]
The last chosen step is:
Up
0 1 2
3 4 5
6 7 8
Finished.
[Moves]:
Up, Up

[Initial State]:
3 1 2
4 0 5
6 7 8
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. **  The last step is not provided. Please complete the last step and return the answer. 
[Process] 
3 1 2
4 0 5
6 7 8
Choose one valid move from: [Left, Right, Up, Down]
Step 1: 
Left
3 1 2
0 4 5
6 7 8
Choose one valid move from: [Right, Up, Down]
The last chosen step is:
Up
0 1 2
3 4 5
6 7 8
Finished.
[Moves]:
Left, Up



[Initial State]:
{state}
All given problems can be solved within 1 to 9 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 9. Try to reach the goal state using the least number of steps (<=9). 
**DO NOT exceed 9 steps. **  The last step is not provided. Please complete the last step and return the answer. 
[Process] 
{move}
The last chosen step is:
"""


npuzzle_prompt_pro_with_laststap = """
[Initial State]:
3 1 2
6 4 5
7 8 0
[Process] 
3 1 2
6 4 5
7 8 0
Step 1: Choose one valid move from: [Left, Up]
Left
3 1 2
6 4 5
7 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Left
3 1 2
6 4 5
0 7 8
Step 3: Choose one valid move from: [Right, Up]
Up
3 1 2
0 4 5
6 7 8
Step 4: Choose one valid move from: [Right, Up]
Up
0 1 2
3 4 5
6 7 8
Finished.
Fllow the process above and return the moves.
[Moves]:
Left, Left, Up, Up


[Initial State]:
3 1 2
6 4 5
0 7 8
[Process] 
3 1 2
6 4 5
0 7 8
Step 1: Choose one valid move from: [Right, Up]
Up
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Down, Up]
Up
0 1 2
3 4 5
6 7 8
Finished.
Fllow the process above and return the moves.
[Moves]:
Up, Up

[Initial State]:
3 1 2
4 0 5
6 7 8
[Process] 
3 1 2
4 0 5
6 7 8
Step 1: Choose one valid move from: [Left, Right, Up, Down]
Left
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Up, Down]
Up
0 1 2
3 4 5
6 7 8
Finished.
Fllow the process above and return the moves.
[Moves]:
Left, Up

[Initial State]:
{state}
[Process] 
{move}
Finished.
Fllow the process above and return the moves.
"""


npuzzle_prompt_revise = """
The given [Process] is not correct since it does not reach the goal state in the end. 
If the final answer does not reach the goal state, then the corresponding [Process] is considered [wrong]. Please help me identify the exact wrong step based on its left number, among [Step 1, Step 2, Step 3, ...]. If you are uncertain about which step is wrong, please begin your analysis with [Step 1] for better understanding.
Please help me identify the exact step number that is wrong. You must provide one wrong step.

[Initial State]:
3 1 2
6 4 5
7 8 0
[Process] 
3 1 2
6 4 5
7 8 0
Step 1: Choose one valid move from: [Left, Up]
Left
3 1 2
6 4 5
7 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Left
3 1 2
6 4 5
0 7 8
Step 3: Choose one valid move from: [Right, Up]
Up
3 1 2
0 4 5
6 7 8
Step 4: Choose one valid move from: [Right, Up]
Right
3 1 2
4 0 5
6 7 8
Finished.
The given [Process] is not correct because number 3, 4, 0, 5 are not their goal positions in the end. The puzzle has failed on reaching its goal state.
Now please help me identify the exact step number that is wrong. You must provide one wrong step. If you can not provide an exact step number, please consider that it could be "all steps are wrong".
[Step 4] is wrong, with Move: Right.

[Initial State]:
3 1 2
6 4 5
0 7 8
[Process] 
3 1 2
6 4 5
0 7 8
Step 1: Choose one valid move from: [Right, Up]
Up
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Down, Up]
Right
3 1 2
4 0 5
6 7 8
Finished.
The given [Process] is not correct because number 3, 4, 0, 5 are not their goal positions in the end. The puzzle has failed on reaching its goal state.
Now please help me identify the exact step number that is wrong. You must provide one wrong step. If you can not provide an exact step number, please consider that it could be "all steps are wrong".
[Step 2] is wrong, with Move: Right.


[Initial State]:
3 1 2
4 0 5
6 7 8
[Process] 
3 1 2
4 0 5
6 7 8
Step 1: Choose one valid move from: [Left, Right, Up, Down]
Up
3 0 2
4 1 5
6 7 8
Step 2: Choose one valid move from: [Right, Up, Down]
Left
0 3 2
4 1 5
6 7 8
Finished.
The given [Process] is not correct because number 3, 2, 4, 1, 5 are not their goal positions in the end. The puzzle has failed on reaching its goal state.
Now please help me identify the exact step number that is wrong. You must provide one wrong step. If you can not provide an exact step number, please consider that it could be "all steps are wrong".
[Step 1] is wrong, with Move: Up.


[Initial State]:
{state}
[Process] 
{move}
Finished.
The given [Process] is not correct because number 3, 2, 4, 1, 5 are not their goal positions in the end. The puzzle has failed on reaching its goal state.
Now please help me identify the exact step number that is wrong. You must provide one wrong step. If you can not provide an exact step number, please consider that it could be "all steps are wrong".
"""


npuzzle_prompt_xot_multi = '''
All given problems can be solved within 1 to 12 steps. The next move must be chosen from the valid move set.
The maximum step number you can take is 12. There may be multiple solutions to a problem, please find **at most 3** correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.

[Initial State]:
3 1 2
6 4 5
0 7 8
[Solution 1] 
[Process] 
Current State:
3 1 2
6 4 5
0 7 8
Step 1: Choose one valid move from: [Right, Up]
Move: Up
Current State:
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Up, Down]
Move: Up
Current State:
0 1 2
3 4 5
6 7 8
Finished.
1. Moves: Up, Up


[Initial State]:
1 4 2
0 3 5
6 7 8
[Solution 1] 
[Process] 
Current State:
1 4 2
0 3 5
6 7 8
Step 1: Choose one valid move from: [Right, Up, Down]
Move: Right
Current State:
1 4 2
3 0 5
6 7 8
Step 2: Choose one valid move from: [Left, Right, Up, Down]
Move: Up
Current State:
1 0 2
3 4 5
6 7 8
Step 3: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2
3 4 5
6 7 8
Finished.
Now strictly follow the above process to form Moves.
1. Moves: Right, Up, Left
[Solution 2] 
[Process] 
Current State:
1 4 2
0 3 5
6 7 8
Step 1: Choose one valid move from: [Right, Up, Down]
Move: Down
Current State:
1 4 2
6 3 5
0 7 8
Step 2: Choose one valid move from: [Right, Up]
Move: Up
Current State:
1 4 2
0 3 5
6 7 8
Step 3: Choose one valid move from: [Right, Up, Down]
Move: Right
Current State:
1 4 2
3 0 5
6 7 8
Step 4: Choose one valid move from: [Left, Right, Up, Down]
Move: Up
Current State:
1 0 2
3 4 5
6 7 8
Step 5: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2
3 4 5
6 7 8
**If a solution has 12 or more steps but does not reach the goal state, stop processing the current solution!!!**
Finished.
Now strictly follow the above process to form Moves.
2. Moves: Down, Up, Right, Up, Left


[Initial State]:
3 1 2
4 0 5
6 7 8
[Solution 1] 
[Process] 
Current State:
3 1 2
4 0 5
6 7 8
Step 1: Choose one valid move from: [Left, Right, Up, Down]
Move: Left
Current State:
3 1 2
0 4 5
6 7 8
Step 2: Choose one valid move from: [Right, Up, Down]
Move: Up
Current State:
0 1 2
3 4 5
6 7 8
Finished.
Now strictly follow the above process to form Moves.
1. Moves: Left, Up


[Initial State]:
1 4 2 
3 7 5 
0 6 8
[Solution 1] 
[Process] 
Current State:
1 4 2 
3 7 5 
0 6 8
Step 1: Choose one valid move from: [Right, Up]
Move: Right
Current State:
1 4 2 
3 7 5 
6 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 4 2 
3 0 5 
6 7 8
Step 3: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 0 2 
3 4 5 
6 7 8
Step 4: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2 
3 4 5 
6 7 8
Finished.
Now strictly follow the above process to form Moves.
1. Moves: Right, Up, Up, Left
[Solution 2] 
[Process] 
Current State:
1 4 2 
3 7 5 
0 6 8
Step 1: Choose one valid move from: [Right, Up]
Move: Right
Current State:
1 4 2 
3 7 5 
6 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Move: Right
Current State:
1 4 2 
3 7 5 
6 8 0
Step 3: Choose one valid move from: [Left, Up]
Move: Left
Current State:
1 4 2 
3 7 5 
6 0 8
Step 4: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 4 2 
3 0 5 
6 7 8
Step 5: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 0 2 
3 4 5 
6 7 8
Step 6: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2 
3 4 5 
6 7 8
Finished.
Now strictly follow the above process to form Moves.
2. Moves: Right, Right, Left, Up, Up, Left
[Solution 3] 
[Process] 
Current State:
1 4 2 
3 7 5 
0 6 8
Step 1: Choose one valid move from: [Right, Up]
Move: Right
Current State:
1 4 2 
3 7 5 
6 0 8
Step 2: Choose one valid move from: [Left, Right, Up]
Move: Up
Current State:
1 4 2 
3 0 5 
6 7 8
Step 3: Choose one valid move from: [Left, Right, Up, Down]
Move: Left
Current State:
1 4 2 
0 3 5 
6 7 8
Step 4: Choose one valid move from: [Right, Up, Down]
Move: Right
Current State:
1 4 2 
3 0 5 
6 7 8
Step 5: Choose one valid move from: [Left, Right, Up, Down]
Move: Up
Current State:
1 0 2 
3 4 5 
6 7 8
Step 6: Choose one valid move from: [Left, Right, Down]
Move: Left
Current State:
0 1 2 
3 4 5 
6 7 8
Finished.
Now strictly follow the above process to form Moves.
3. Moves: Right, Up, Left, Right, Up, Left

[Initial State]:
{state}
{move}
Now strictly follow the above process to form Moves.
'''

# 1-shot
propose_prompt = '''
Please provide two possible next one move from [valid next move], which you think can lead us closer to the goal state.
[Current State]:
1 6 2
3 4 5
7 8 0 
[Valid next move]:
1. Up
After Up:
1 6 2
3 4 0
7 8 5 
2. Left
After Left:
1 6 2
3 4 5
7 0 8 
[Possible next move]:
Up, Left

[Current State]:
1 2 3
6 0 5
7 4 8 
[Valid next move]:
1. Up
After Up:
1 0 3
6 2 5
7 4 8 
2. Left
After Left:
1 2 3
0 6 5
7 4 8 
3. Right
After Right:
1 2 3
6 5 0
7 4 8 
3. Down
After Down:
1 2 3
6 4 5
7 0 8 
[Possible next move]:
Left, Down

[Current State]:
{state}
[Valid next move]:
{move}
[Possible next move]:
'''

value_prompt = '''
Evaluate if we can reach the goal state after the move. (sure/likely/impossible)
[Current State]:
1 2 0
3 4 5
6 7 8 
[Move]:
Left
1 0 2
3 4 5
6 7 8 
We moved '2' to its goal position. After that, we only need to do 'Left' then we can reach the goal state.
[Evaluation]:
sure

[Current State]:
3 1 2
0 6 5
7 4 8
[Move]:
Down
3 1 2
7 6 5
0 4 8
We moved '7' away from its goal position. After that, '1', '2', and '5' are in their goal positions. However, '3', '4', '6', '7', and '8' are not in their goal positions. It will take several moves to rearrange the pieces and reach the goal state.
[Evaluation]:
impossible

[Current State]:
3 1 2
6 0 5
7 4 8
[Move]:
Down
3 1 2
6 4 5
7 0 8
We moved '4' to its goal position. After that, '1' '2' '4' '5' are in their goal position. It is plausible that only a few moves are needed to reach the goal state.
[Evaluation]:
likely

[Current State]:
{state}
[Move]:
{move}
'''

merge_prompt = '''
Please select {n_select_sample} move from the proposed move list, which you believe can lead the current state to be closer to the goal state. The state you select must be valid.
[Current State]:
1 0 2
3 4 5
6 7 8 
[Proposed Move List]:
(1) Left
0 1 2
3 4 5
6 7 8 
(2) Down
1 4 2
3 0 5
6 7 8 
[Best Next Move]:
(1) Left

[Current State]:
3 1 2
6 4 5
0 7 8
[Proposed Move List]:
(1) Right
3 1 2
6 4 5
7 0 8
(2) Up
3 1 2
0 4 5
6 7 8
[Best Next Move]:
(2) Up

[Current State]:
3 1 2
0 6 5
7 4 8
[Proposed Move List]:
(1) Down
3 1 2
7 6 5
0 4 8
(2) Right
3 1 2
6 0 5
7 4 8
[Best Next Move]:
(2) Right

[Current State]:
{state}
[Proposed Move List]:
{move}
[Best Next Move]:
'''


merge_prompt_3_select_sample = '''
Please select {n_select_sample} move from the proposed move list, which you believe can lead the current state to be closer to the goal state. The state you select must be valid.
[Current State]:
1 0 2
3 4 5
6 7 8 
[Proposed Move List]:
(1) Left
0 1 2
3 4 5
6 7 8 
(2) Down
1 4 2
3 0 5
6 7 8 
(3) Right
1 2 0
3 4 5
6 7 8 
[Best Next Move]:
(1) Left
(2) Right

[Current State]:
3 1 2
6 4 5
0 7 8
[Proposed Move List]:
(1) Right
3 1 2
6 4 5
7 0 8
(2) Up
3 1 2
0 4 5
6 7 8
[Best Next Move]:
(2) Up
(1) Right


[Current State]:
3 1 2
0 6 5
7 4 8
[Proposed Move List]:
(1) Down
3 1 2
7 6 5
0 4 8
(2) Up
0 1 2
3 6 5
7 4 8
(3) Right
3 1 2
6 0 5
7 4 8
[Best Next Move]:
(2) Up
(3) Right

[Current State]:
1 4 2 
3 0 5 
6 7 8
[Proposed Move List]:
(1) Left
1 4 2 
0 3 5 
6 7 8
(2) Right
1 4 2 
3 5 0
6 7 8
(3) Up
1 0 2 
3 4 5 
6 7 8
(4) Down
1 4 2 
3 7 5 
6 0 8
[Best Next Move]:
(1) Left
(3) Up
(2) Right

[Current State]:
{state}
[Proposed Move List]:
{move}
[Best Next Move]:
'''


