# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

cube_instruct = """You are a virtual expert in solving a 2x2 Pocket Cube. Your task is to restore a scrambled 2x2 Rubik's Cube to its original state. All the given problems can be solved in 1 to 4 moves. You cannot exceed more than 11 moves. Provide the sequence of moves required for the restoration. Please follow the instructions and rules below to complete the solving:
1. A 2x2 Pocket Cube has six faces, namely: [Upper, Front, Bottom, Left, Right, Back] Each consisting of a 2x2 grid of squares, with each square having its own color.
2. Colors in the Cube are represented in numbers: [0, 1, 2, 3, 4, 5]
3. The Cube's state is represented into a facelets expanding graph, for instance:
Upper: 
0 0 
0 0
Front: 
5 5 
2 2
Down: 
3 3 
3 3
Left: 
1 1 
4 4
Right: 
4 4 
1 1
Back: 
2 2 
5 5

4. A restoration of a Pocket Cube is to move squares in each face to have same numbers. Some example Restored States are:
[Restored State]
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5
Or
[Restored State]
Upper: 
2 2 
2 2
Front: 
0 0
0 0
Down: 
3 3 
3 3
Left: 
1 1 
1 1
Right: 
4 4 
4 4
Back: 
5 5 
5 5
You must make move to the Cube to achieve a Restored State, not limited to the above one. Note that we just need each face to have same numbers, no matter which face has which color.

5. You are only allowed to use following moves [U, U', U2, R, R', R2, F, F', F2]. 
["U": Turn the Upper face of the cube 90 degrees clockwise.
For instance, after taking move U:
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5

will become
Up:
0 0
0 0
Front:
1 1
2 2
Down:
3 3
3 3
Left:
2 2
4 4
Right:
5 5
1 1
Back:
4 4
5 5

"U'": Turn the Upper face of the cube 90 degrees counterclockwise (or anti-clockwise).
For instance, after taking move U':
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5

will become
Upper:
0 0
0 0
Front:
4 4
2 2
Down:
3 3
3 3
Left:
5 5
4 4
Right:
2 2
1 1
Back:
1 1
5 5

"U2": Turn the Upper face of the cube 180 degrees (a half turn).
For instance, after taking move U2:
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5
will become
Up:
0 0
0 0
Front:
5 5
2 2
Down:
3 3
3 3
Left:
1 1
4 4
Right:
4 4
1 1
Back:
2 2
5 5
      
"R": Turn the Right face of the cube 90 degrees clockwise.
For instance, after taking move R:
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5

will become
Upper:
0 2
0 2
Front:
2 3
2 3
Down:
3 5
3 5
Left:
4 4
4 4
Right:
1 1
1 1
Back:
0 5
0 5
      
"R'": Turn the Right face of the cube 90 degrees counterclockwise.
For instance, after taking move R':
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5

will become
Upper:
0 5
0 5
Front:
2 0
2 0
Down:
3 2
3 2
Left:
4 4
4 4
Right:
1 1
1 1
Back:
3 5
3 5
      
"R2": Turn the Right face of the cube 180 degrees.
For instance, after taking move R':
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5
will become
Up:
0 3
0 3
Front:
2 5
2 5
Down:
3 0
3 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 5
2 5

"F": Turn the Front face of the cube 90 degrees clockwise.
For instance, after taking move F:
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5

will become
Up:
0 0
4 4
Front:
2 2
2 2
Down:
1 1
3 3
Left:
4 3
4 3
Right:
0 1
0 1
Back:
5 5
5 5

"F'": Turn the Front face of the cube 90 degrees counterclockwise.
For instance, after taking move F':
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5

will become
Upper: 
0 0 
1 1
Front: 
2 2 
2 2
Down: 
4 4 
3 3
Left: 
4 0 
4 0
Right: 
3 1 
3 1
Back: 
5 5 
5 5      
 
"F2": Turn the Front face of the cube 180 degrees.
For instance, after taking move F2:
Upper: 
0 0 
0 0
Front: 
2 2 
2 2
Down: 
3 3 
3 3
Left: 
4 4 
4 4
Right: 
1 1 
1 1
Back: 
5 5 
5 5

will become
Upper:
0 0
3 3
Front:
2 2
2 2
Down:
0 0
3 3
Left:
4 1
4 1
Right:
4 1
4 1
Back:
5 5
5 5
"""


cube_prompt_revised = """
The given [Process] is not correct since it does not reach the goal state in the end. 
If the final answer does not reach the goal state, then the corresponding [Process] is considered [wrong]. Please help me identify the exact wrong step based on its left number, among [Step 1, Step 2, Step 3, ...]. If you are uncertain about which step is wrong, please begin your analysis with [Step 1] for better understanding.
Please help me identify the exact step number that is wrong. You must provide one wrong step.
[Initial Cube State]:
Upper:
4 5
4 4
Front:
5 1
5 0
Down:
0 0
2 0
Left:
1 1
3 2
Right:
2 2
4 3
Back:
3 3
1 5
[Process]:
[Step 1]
[Move] R
[Current Cube State]
Upper:
4 0
4 0
Front:
5 5
0 1
Down:
0 1
2 2
Left:
1 1
3 3
Right:
2 2
4 3
Back:
4 3
5 5
[Step 2]
[Move] U'
[Current Cube State]
Upper:
0 0
4 4
Front:
0 1
0 1
Down:
2 2
2 2
Left:
1 1
3 3
Right:
4 3
4 3
Back:
5 5
5 5
[Step 3]
[Move] F2
[Current Cube State]
Upper:
0 0
1 1
Front:
2 2
2 2
Down:
4 4
3 3
Left:
4 0
4 0
Right:
3 1
3 1
Back:
5 5
5 5
Finished.
After finishing all the moves: The Upper face still has 2 differnet colors. The Down face still has 2 differnet colors. The Left face still has 2 differnet colors. The Right face still has 2 differnet colors. 
The given [Process] is not correct because not every face has the same numbers in the end. The cube has failed on restoring to its original state.
Now please help me identify the exact step number that is wrong. You must provide one wrong step. If you can not provide an exact step number, please consider that it could be "all steps are wrong".
[Step 3] is wrong, with Move: F2.

[Initial Cube State]:
Upper:
5 5
0 2
Front:
2 3
4 4
Down:
3 3
2 0
Left:
3 4
1 5
Right:
1 0
2 4
Back:
1 1
5 0
[Process]:
[Step 1]
[Move] F2
[Current Cube State]
Upper:
5 5
3 3
Front:
4 4
3 2
Down:
2 0
2 0
Left:
3 2
1 1
Right:
5 0
4 4
Back:
1 1
5 0
[Step 2]
[Move] U2
[Current Cube State]
Upper:
3 3
5 5
Front:
1 1
3 2
Down:
2 0
2 0
Left:
5 0
1 1
Right:
3 2
4 4
Back:
4 4
5 0
[Step 3]
[Move] R
[Current Cube State]
Upper:
3 1
5 2
Front:
1 0
3 0
Down:
2 5
2 4
Left:
5 0
1 1
Right:
4 3
4 2
Back:
5 4
3 0
Finished.
After finishing all the moves: The Upper face still has 4 differnet colors. The Front face still has 3 differnet colors. The Down face still has 3 differnet colors. The Left face still has 2 differnet colors. The Right face still has 2 differnet colors. The Right face still has 4 differnet colors. 
The given [Process] is not correct because not every face has the same numbers in the end. The cube has failed on restoring to its original state.
Now please help me identify the exact step number that is wrong. You must provide one wrong step. If you can not provide an exact step number, please consider that it could be "all steps are wrong".
[Step 2] is wrong, with Move: U2.

[Initial Cube State]:
Upper:
3 2
0 5
Front:
2 3
5 0
Down:
0 2
3 5
Left:
1 4
1 4
Right:
4 4
1 1
Back:
3 5
0 2
[Process]:
[Step 1]
[Move] R
[Current Cube State]
Upper:
3 3
0 0
Front:
2 2
5 5
Down:
0 0
3 3
Left:
1 4
1 4
Right:
1 4
1 4
Back:
5 5
2 2
[Step 2]
[Move] U2
[Current Cube State]
Upper:
0 0
3 3
Front:
5 5
5 5
Down:
0 0
3 3
Left:
1 4
1 4
Right:
1 4
1 4
Back:
2 2
2 2
[Step 3]
[Move] R'
[Current Cube State]
Upper:
0 2
3 2
Front:
5 0
5 3
Down:
0 5
3 5
Left:
1 4
1 4
Right:
4 4
1 1
Back:
3 2
0 2
Finished.
After finishing all the moves: The Upper face still has 3 differnet colors. The Front face still has 3 differnet colors. The Down face still has 3 differnet colors. The Left face still has 2 differnet colors. The Right face still has 2 differnet colors. The Right face still has 3 differnet colors. 
The given [Process] is not correct because not every face has the same numbers in the end. The cube has failed on restoring to its original state.
Now please help me identify the exact step number that is wrong. You must provide one wrong step. If you can not provide an exact step number, please consider that it could be "all steps are wrong".
[Step 3] is wrong, with Move: R'.

[Initial Cube State]
{state}
[Process]
{move}
Finished.
{reason}
The given [Process] is not correct because not every face has the same numbers in the end. The cube has failed on restoring to its original state.
Now please help me identify the exact step number that is wrong. You must provide one wrong step. If you can not provide an exact step number, please consider that it could be "all steps are wrong".
"""

cube_prompt_xot_with_laststap = """
[Initial Cube State]:
Upper:
4 5
4 4
Front:
5 1
5 0
Down:
0 0
2 0
Left:
1 1
3 2
Right:
2 2
4 3
Back:
3 3
1 5
[Process]:
[Step 1]
[Move] R
[Current Cube State]
Upper:
4 0
4 0
Front:
5 5
0 1
Down:
0 1
2 2
Left:
1 1
3 3
Right:
2 2
4 3
Back:
4 3
5 5
[Step 2]
[Move] U'
[Current Cube State]
Upper:
0 0
4 4
Front:
0 1
0 1
Down:
2 2
2 2
Left:
1 1
3 3
Right:
4 3
4 3
Back:
5 5
5 5
[Step 3]
[Move] F'
[Current Cube State]
Upper:
0 0
0 0
Front:
1 1
1 1
Down:
2 2
2 2
Left:
3 3
3 3
Right:
4 4
4 4
Back:
5 5
5 5
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R U' F'

[Initial Cube State]:
Upper:
5 5
0 2
Front:
2 3
4 4
Down:
3 3
2 0
Left:
3 4
1 5
Right:
1 0
2 4
Back:
1 1
5 0
[Process]:
[Step 1]
[Move] F2
[Current Cube State]
Upper:
5 5
3 3
Front:
4 4
3 2
Down:
2 0
2 0
Left:
3 2
1 1
Right:
5 0
4 4
Back:
1 1
5 0
[Step 2]
[Move] U'
[Current Cube State]
Upper:
5 3
5 3
Front:
3 2
3 2
Down:
2 0
2 0
Left:
1 1
1 1
Right:
4 4
4 4
Back:
5 0
5 0
[Step 3]
[Move] R'
[Current Cube State]
Upper:
5 5
5 5
Front:
3 3
3 3
Down:
2 2
2 2
Left:
1 1
1 1
Right:
4 4
4 4
Back:
0 0
0 0
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
F2 U' R'

[Initial Cube State]:
Upper:
3 2
0 5
Front:
2 3
5 0
Down:
0 2
3 5
Left:
1 4
1 4
Right:
4 4
1 1
Back:
3 5
0 2
[Process]:
[Step 1]
[Move] R
[Current Cube State]
Upper:
3 3
0 0
Front:
2 2
5 5
Down:
0 0
3 3
Left:
1 4
1 4
Right:
1 4
1 4
Back:
5 5
2 2
[Step 2]
[Move] U2
[Current Cube State]
Upper:
0 0
3 3
Front:
5 5
5 5
Down:
0 0
3 3
Left:
1 4
1 4
Right:
1 4
1 4
Back:
2 2
2 2
[Step 3]
[Move] F2
[Current Cube State]
Upper:
0 0
0 0
Front:
5 5
5 5
Down:
3 3
3 3
Left:
1 1
1 1
Right:
4 4
4 4
Back:
2 2
2 2
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R U2 F2

[Initial Cube State]
{state}
[Process]
{move}
Finished.
Now strictly follow the above process to form Restoration Moves.
"""

# Please complete the moves and return the cube state after all moves.
cube_prompt_xot_wo_laststap = """
The process does not provide the last step. Complete the last step by choosing a valid move from [U, U', U2, R, R', R2, F, F', F2], then reach the goal state.
[Initial Cube State]:
Upper:
4 5
4 4
Front:
5 1
5 0
Down:
0 0
2 0
Left:
1 1
3 2
Right:
2 2
4 3
Back:
3 3
1 5
[Process]:
The process does not provide the last step. Follow and complete the process and return the moves.
[Step 1]
[Move] R
[Current Cube State]
Upper:
4 0
4 0
Front:
5 5
0 1
Down:
0 1
2 2
Left:
1 1
3 3
Right:
2 2
4 3
Back:
4 3
5 5
[Step 2]
[Move] U'
[Current Cube State]
Upper:
0 0
4 4
Front:
0 1
0 1
Down:
2 2
2 2
Left:
1 1
3 3
Right:
4 3
4 3
Back:
5 5
5 5
The last step is:
[Step 3]
[Move] F'
[Current Cube State]
Upper:
0 0
0 0
Front:
1 1
1 1
Down:
2 2
2 2
Left:
3 3
3 3
Right:
4 4
4 4
Back:
5 5
5 5
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R U' F'

[Initial Cube State]:
Upper:
5 5
0 2
Front:
2 3
4 4
Down:
3 3
2 0
Left:
3 4
1 5
Right:
1 0
2 4
Back:
1 1
5 0
[Process]:
The process does not provide the final step. Follow and complete the process and return the moves.
[Step 1]
[Move] F2
[Current Cube State]
Upper:
5 5
3 3
Front:
4 4
3 2
Down:
2 0
2 0
Left:
3 2
1 1
Right:
5 0
4 4
Back:
1 1
5 0
[Step 2]
[Move] U'
[Current Cube State]
Upper:
5 3
5 3
Front:
3 2
3 2
Down:
2 0
2 0
Left:
1 1
1 1
Right:
4 4
4 4
Back:
5 0
5 0
The last step is:
[Step 3]
[Move] R'
[Current Cube State]
Upper:
5 5
5 5
Front:
3 3
3 3
Down:
2 2
2 2
Left:
1 1
1 1
Right:
4 4
4 4
Back:
0 0
0 0
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
F2 U' R'

[Initial Cube State]:
Upper:
3 2
0 5
Front:
2 3
5 0
Down:
0 2
3 5
Left:
1 4
1 4
Right:
4 4
1 1
Back:
3 5
0 2
[Process]:
The process does not provide the final step. Follow and complete the process and return the moves.
[Step 1]
[Move] R
[Current Cube State]
Upper:
3 3
0 0
Front:
2 2
5 5
Down:
0 0
3 3
Left:
1 4
1 4
Right:
1 4
1 4
Back:
5 5
2 2
[Step 2]
[Move] U2
[Current Cube State]
Upper:
0 0
3 3
Front:
5 5
5 5
Down:
0 0
3 3
Left:
1 4
1 4
Right:
1 4
1 4
Back:
2 2
2 2
The last step is:
[Step 3]
[Move] F2
[Current Cube State]
Upper:
0 0
0 0
Front:
5 5
5 5
Down:
3 3
3 3
Left:
1 1
1 1
Right:
4 4
4 4
Back:
2 2
2 2
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R U2 F2

[Initial Cube State]:
Upper:
2 5
2 5
Front:
0 0
0 0
Down:
2 5
2 5
Left:
1 1
4 4
Right:
1 1
4 4
Back:
3 3
3 3
[Process]:
The process does not provide the final step. Follow and complete the process and return the moves.
[Step 1]
[Move] R2
[Current Cube State]
Upper:
2 5
2 5
Front:
0 3
0 3
Down:
2 5
2 5
Left:
1 1
4 4
Right:
4 4
1 1
Back:
0 3
0 3
[Step 2]
[Move] U2
[Current Cube State]
Upper:
5 2
5 2
Front:
0 3
0 3
Down:
2 5
2 5
Left:
4 4
4 4
Right:
1 1
1 1
Back:
0 3
0 3
The last step is:
[Step 3]
[Move] R2
[Current Cube State]
Upper:
5 5
5 5
Front:
0 0
0 0
Down:
2 2
2 2
Left:
4 4
4 4
Right:
1 1
1 1
Back:
3 3
3 3
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R2 U2 R2

[Initial Cube State]:
Upper:
5 4
0 4
Front:
4 3
4 2
Down:
3 1
2 1
Left:
3 5
3 5
Right:
2 2
0 0
Back:
0 1
5 1
[Process]:
The process does not provide the final step. Follow and complete the process and return the moves.
[Step 1]
[Move] R'
[Current Cube State]
Upper:
5 5
0 0
Front:
4 4
4 4
Down:
3 3
2 2
Left:
3 5
3 5
Right:
2 0
2 0
Back:
1 1
1 1
The last step is:
[Step 2]
[Move] F
[Current Cube State]
Upper:
5 5
5 5
Front:
4 4
4 4
Down:
2 2
2 2
Left:
3 3
3 3
Right:
0 0
0 0
Back:
1 1
1 1
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R' F

[Initial Cube State]:
Upper:
2 2
1 1
Front:
3 3
5 1
Down:
4 5
4 5
Left:
4 2
3 3
Right:
5 1
0 0
Back:
0 0
4 2
[Process]:
The process does not provide the final step. Follow and complete the process and return the moves.
[Step 1]
[Move] U
[Current Cube State]
Upper:
1 2
1 2
Front:
5 1
5 1
Down:
4 5
4 5
Left:
3 3
3 3
Right:
0 0
0 0
Back:
4 2
4 2
The last step is:
[Step 2]
[Move] R
[Current Cube State]
Upper:
1 1
1 1
Front:
5 5
5 5
Down:
4 4
4 4
Left:
3 3
3 3
Right:
0 0
0 0
Back:
2 2
2 2
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
U R

[Initial Cube State]:
Upper:
5 0
5 4
Front:
0 2
4 2
Down:
2 1
2 3
Left:
4 4
3 3
Right:
0 1
0 1
Back:
5 3
5 1
[Process]:
The process does not provide the final step. Follow and complete the process and return the moves.
[Step 1]
[Move] R'
[Current Cube State]
Upper:
5 5
5 5
Front:
0 0
4 4
Down:
2 2
2 2
Left:
4 4
3 3
Right:
1 1
0 0
Back:
3 3
1 1
The last step is:
[Step 2]
[Move] U'
[Current Cube State]
Upper:
5 5
5 5
Front:
4 4
4 4
Down:
2 2
2 2
Left:
3 3
3 3
Right:
0 0
0 0
Back:
1 1
1 1
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R' U'

[Initial Cube State]:
Upper:
4 5
1 5
Front:
2 4
4 5
Down:
2 1
2 4
Left:
3 0
3 3
Right:
0 0
3 0
Back:
1 5
2 1
[Process]:
The process does not provide the final step. Follow and complete the process and return the moves.
[Step 1]
[Move] U2
[Current Cube State]
Upper:
5 1
5 4
Front:
1 5
4 5
Down:
2 1
2 4
Left:
0 0
3 3
Right:
3 0
3 0
Back:
2 4
2 1
[Step 2]
[Move] R
[Current Cube State]
Upper:
5 5
5 5
Front:
1 1
4 4
Down:
2 2
2 2
Left:
0 0
3 3
Right:
3 3
0 0
Back:
4 4
1 1
The last step is:
[Step 3]
[Move] U2
[Current Cube State]
Upper:
5 5
5 5
Front:
4 4
4 4
Down:
2 2
2 2
Left:
3 3
3 3
Right:
0 0
0 0
Back:
1 1
1 1
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
U2 R U2

[Initial Cube State]:
Upper:
3 0
3 0
Front:
4 2
5 1
Down:
0 3
0 3
Left:
2 2
4 4
Right:
1 1
5 5
Back:
5 1
4 2
[Process]:
The process does not provide the final step. Follow and complete the process and return the moves.
[Step 1]
[Move] R2
[Current Cube State]
Upper:
3 3
3 3
Front:
4 4
5 5
Down:
0 0
0 0
Left:
2 2
4 4
Right:
5 5
1 1
Back:
1 1
2 2
The last step is:
[Step 2]
[Move] U
[Current Cube State]
Upper:
3 3
3 3
Front:
5 5
5 5
Down:
0 0
0 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 2
2 2
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R2 U

[Initial Cube State]
{state}
[Process]
The process does not provide the final step. Follow and complete the process and return the moves.
{move}
The last step is:
"""


cube_prompt_xot_multi = """
All the given problems can be solved in 1 to 7 moves. You cannot exceed more than 11 moves.
There may be multiple solutions to a problem, please find 3 correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
Please return the [Restoration Moves].

[Initial Cube State]:
Upper:
1 1
3 3
Front:
4 1
2 5
Down:
0 4
0 4
Left:
5 2
4 1
Right:
2 5
0 3
Back:
0 3
5 2
[Solution 1]
[Process]:
[Step 1]
[Move] U
[Current Cube State]
Upper:
3 1
3 1
Front:
2 5
2 5
Down:
0 4
0 4
Left:
4 1
4 1
Right:
0 3
0 3
Back:
5 2
5 2
[Step 2]
[Move] F2
[Current Cube State]
Upper:
3 1
4 0
Front:
5 2
5 2
Down:
1 3
0 4
Left:
4 0
4 0
Right:
1 3
1 3
Back:
5 2
5 2
[Step 3]
[Move] R2
[Current Cube State]
Upper:
3 3
4 4
Front:
5 5
5 5
Down:
1 1
0 0
Left:
4 0
4 0
Right:
3 1
3 1
Back:
2 2
2 2
[Step 4]
[Move] F'
[Current Cube State]
Upper:
3 3
3 3
Front:
5 5
5 5
Down:
0 0
0 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 2
2 2
Finished.

[Solution 2]
[Process]:
[Step 1]
[Move] F2
[Current Cube State]
Upper:
1 1
4 0
Front:
5 2
1 4
Down:
3 3
0 4
Left:
5 0
4 2
Right:
1 5
2 3
Back:
0 3
5 2
[Step 2]
[Move] R2
[Current Cube State]
Upper:
1 3
4 4
Front:
5 5
1 0
Down:
3 1
0 0
Left:
5 0
4 2
Right:
3 2
5 1
Back:
4 3
2 2
[Step 3]
[Move] F2
[Current Cube State]
Upper:
1 3
1 3
Front:
0 1
5 5
Down:
4 4
0 0
Left:
5 5
4 3
Right:
2 2
0 1
Back:
4 3
2 2
[Step 4]
[Move] U'
[Current Cube State]
Upper:
3 3
1 1
Front:
5 5
5 5
Down:
4 4
0 0
Left:
4 3
4 3
Right:
0 1
0 1
Back:
2 2
2 2
[Step 5]
[Move] F
[Current Cube State]
Upper:
3 3
3 3
Front:
5 5
5 5
Down:
0 0
0 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 2
2 2
Finished.

[Solution 3]
[Process]:
[Step 1]
[Move] R2
[Current Cube State]
Upper:
1 4
3 4
Front:
4 5
2 0
Down:
0 1
0 3
Left:
5 2
4 1
Right:
3 0
5 2
Back:
5 3
1 2
[Step 2]
[Move] F2
[Current Cube State]
Upper:
1 4
1 0
Front:
0 2
5 4
Down:
4 3
0 3
Left:
5 5
4 3
Right:
1 0
2 2
Back:
5 3
1 2
[Step 3]
[Move] R2
[Current Cube State]
Upper:
1 3
1 3
Front:
0 1
5 5
Down:
4 4
0 0
Left:
5 5
4 3
Right:
2 2
0 1
Back:
4 3
2 2
[Step 4]
[Move] U'
[Current Cube State]
Upper:
3 3
1 1
Front:
5 5
5 5
Down:
4 4
0 0
Left:
4 3
4 3
Right:
0 1
0 1
Back:
2 2
2 2
[Step 5]
[Move] F
[Current Cube State]
Upper:
3 3
3 3
Front:
5 5
5 5
Down:
0 0
0 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 2
2 2
Finished.

Now strictly follow the above process to form Restoration Moves.
1. Restoration Moves: U F2 R2 F'
2. Restoration Moves: F2 R2 F2 U' F
3. Restoration Moves: R2 F2 R2 U' F

[Initial Cube State]
{state}
{move}
Now strictly follow the above process to form Restoration Moves.
"""

cube_prompt_io = """
All the given problems can be solved in 1 to 4 moves. You cannot exceed more than 11 moves.
Please return the [Restoration Moves].
[Initial Cube State]:
Upper:
4 5
4 4
Front:
5 1
5 0
Down:
0 0
2 0
Left:
1 1
3 2
Right:
2 2
4 3
Back:
3 3
1 5
[Restoration Moves]:
R U' F'

[Initial Cube State]:
Upper:
5 5
0 2
Front:
2 3
4 4
Down:
3 3
2 0
Left:
3 4
1 5
Right:
1 0
2 4
Back:
1 1
5 0
[Restoration Moves]:
F2 U' R'

[Initial Cube State]:
Upper:
3 2
0 5
Front:
2 3
5 0
Down:
0 2
3 5
Left:
1 4
1 4
Right:
4 4
1 1
Back:
3 5
0 2
[Restoration Moves]:
R U2 F2

[Initial Cube State]
{state}
"""

cube_prompt_io_multi = """
All the given problems can be solved in 1 to 7 moves. You cannot exceed more than 11 moves.
There may be multiple solutions to a problem, please find 3 correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
Please return the [Restoration Moves].
[Initial Cube State]:
Upper:
1 1
3 3
Front:
4 1
2 5
Down:
0 4
0 4
Left:
5 2
4 1
Right:
2 5
0 3
Back:
0 3
5 2

1. Restoration Moves: U F2 R2 F'
2. Restoration Moves: F2 R2 F2 U' F
3. Restoration Moves: R2 F2 R2 U' F

[Initial Cube State]:
Upper:
5 1
0 2
Front:
5 0
2 2
Down:
1 1
2 4
Left:
4 1
4 3
Right:
4 3
0 5
Back:
5 3
0 3
1. Restoration Moves: F' R2 F' R
2. Restoration Moves: F R2 F2 R2 F R
3. Restoration Moves: F' U2 R2 F R2 U2 R'

[Initial Cube State]:
Upper:
5 1
4 4
Front:
3 3
3 4
Down:
1 2
2 4
Left:
1 5
3 5
Right:
2 0
0 5
Back:
2 0
0 1
1. Restoration Moves: U' R' F U F R
2. Restoration Moves: F R U F'
3. Restoration Moves: U R U F U R' F2

[Initial Cube State]
{state}
"""

# Please complete the moves and return the cube state after all moves.
cube_prompt_cot = """
All the given problems can be solved in 1 to 4 moves. **You cannot exceed more than 11 moves.**
Please complete [Process] and return the [Restoration Moves].
[Initial Cube State]:
Upper:
4 5
4 4
Front:
5 1
5 0
Down:
0 0
2 0
Left:
1 1
3 2
Right:
2 2
4 3
Back:
3 3
1 5
[Process]:
[Step 1]
[Move] R
[Current Cube State]
Upper:
4 0
4 0
Front:
5 5
0 1
Down:
0 1
2 2
Left:
1 1
3 3
Right:
2 2
4 3
Back:
4 3
5 5
[Step 2]
[Move] U'
[Current Cube State]
Upper:
0 0
4 4
Front:
0 1
0 1
Down:
2 2
2 2
Left:
1 1
3 3
Right:
4 3
4 3
Back:
5 5
5 5
[Step 3]
[Move] F'
[Current Cube State]
Upper:
0 0
0 0
Front:
1 1
1 1
Down:
2 2
2 2
Left:
3 3
3 3
Right:
4 4
4 4
Back:
5 5
5 5
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R U' F'

All the given problems can be solved in 1 to 4 moves. **You cannot exceed more than 11 moves.**
Please complete [Process] and return the [Restoration Moves].
[Initial Cube State]:
Upper:
5 5
0 2
Front:
2 3
4 4
Down:
3 3
2 0
Left:
3 4
1 5
Right:
1 0
2 4
Back:
1 1
5 0
[Process]:
[Step 1]
[Move] F2
[Current Cube State]
Upper:
5 5
3 3
Front:
4 4
3 2
Down:
2 0
2 0
Left:
3 2
1 1
Right:
5 0
4 4
Back:
1 1
5 0
[Step 2]
[Move] U'
[Current Cube State]
Upper:
5 3
5 3
Front:
3 2
3 2
Down:
2 0
2 0
Left:
1 1
1 1
Right:
4 4
4 4
Back:
5 0
5 0
[Step 3]
[Move] R'
[Current Cube State]
Upper:
5 5
5 5
Front:
3 3
3 3
Down:
2 2
2 2
Left:
1 1
1 1
Right:
4 4
4 4
Back:
0 0
0 0
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
F2 U' R'

All the given problems can be solved in 1 to 4 moves. **You cannot exceed more than 11 moves.**
Please complete [Process] and return the [Restoration Moves].
[Initial Cube State]:
Upper:
3 2
0 5
Front:
2 3
5 0
Down:
0 2
3 5
Left:
1 4
1 4
Right:
4 4
1 1
Back:
3 5
0 2
[Process]:
[Step 1]
[Move] R
[Current Cube State]
Upper:
3 3
0 0
Front:
2 2
5 5
Down:
0 0
3 3
Left:
1 4
1 4
Right:
1 4
1 4
Back:
5 5
2 2
[Step 2]
[Move] U2
[Current Cube State]
Upper:
0 0
3 3
Front:
5 5
5 5
Down:
0 0
3 3
Left:
1 4
1 4
Right:
1 4
1 4
Back:
2 2
2 2
[Step 3]
[Move] F2
[Current Cube State]
Upper:
0 0
0 0
Front:
5 5
5 5
Down:
3 3
3 3
Left:
1 1
1 1
Right:
4 4
4 4
Back:
2 2
2 2
Finished.
Now strictly follow the above process to form Restoration Moves.
[Restoration Moves]:
R U2 F2

All the given problems can be solved in 1 to 4 moves. **You cannot exceed more than 11 moves.**
Please complete [Process] and return the [Restoration Moves].
[Initial Cube State]
{state}
"""


cube_prompt_cot_multi = """
All the given problems can be solved in 1 to 7 moves. You cannot exceed more than 11 moves.
There may be multiple solutions to a problem, please find 3 correct solutions if there are multiple solutions to the problem. Otherwise, only the only correct answer can be returned.
Please return the Restoration Moves.

[Initial Cube State]:
Upper:
1 1
3 3
Front:
4 1
2 5
Down:
0 4
0 4
Left:
5 2
4 1
Right:
2 5
0 3
Back:
0 3
5 2
[Solution 1]
[Process]:
[Step 1]
[Move] U
[Current Cube State]
Upper:
3 1
3 1
Front:
2 5
2 5
Down:
0 4
0 4
Left:
4 1
4 1
Right:
0 3
0 3
Back:
5 2
5 2
[Step 2]
[Move] F2
[Current Cube State]
Upper:
3 1
4 0
Front:
5 2
5 2
Down:
1 3
0 4
Left:
4 0
4 0
Right:
1 3
1 3
Back:
5 2
5 2
[Step 3]
[Move] R2
[Current Cube State]
Upper:
3 3
4 4
Front:
5 5
5 5
Down:
1 1
0 0
Left:
4 0
4 0
Right:
3 1
3 1
Back:
2 2
2 2
[Step 4]
[Move] F'
[Current Cube State]
Upper:
3 3
3 3
Front:
5 5
5 5
Down:
0 0
0 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 2
2 2
Finished.
Now strictly follow the above process to form Restoration Moves.
1. Restoration Moves: U F2 R2 F'

[Solution 2]
[Process]:
[Step 1]
[Move] F2
[Current Cube State]
Upper:
1 1
4 0
Front:
5 2
1 4
Down:
3 3
0 4
Left:
5 0
4 2
Right:
1 5
2 3
Back:
0 3
5 2
[Step 2]
[Move] R2
[Current Cube State]
Upper:
1 3
4 4
Front:
5 5
1 0
Down:
3 1
0 0
Left:
5 0
4 2
Right:
3 2
5 1
Back:
4 3
2 2
[Step 3]
[Move] F2
[Current Cube State]
Upper:
1 3
1 3
Front:
0 1
5 5
Down:
4 4
0 0
Left:
5 5
4 3
Right:
2 2
0 1
Back:
4 3
2 2
[Step 4]
[Move] U'
[Current Cube State]
Upper:
3 3
1 1
Front:
5 5
5 5
Down:
4 4
0 0
Left:
4 3
4 3
Right:
0 1
0 1
Back:
2 2
2 2
[Step 5]
[Move] F
[Current Cube State]
Upper:
3 3
3 3
Front:
5 5
5 5
Down:
0 0
0 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 2
2 2
Finished.
Now strictly follow the above process to form Restoration Moves.
2. Restoration Moves: F2 R2 F2 U' F
[Solution 3]
[Process]:
[Step 1]
[Move] R2
[Current Cube State]
Upper:
1 4
3 4
Front:
4 5
2 0
Down:
0 1
0 3
Left:
5 2
4 1
Right:
3 0
5 2
Back:
5 3
1 2
[Step 2]
[Move] F2
[Current Cube State]
Upper:
1 4
1 0
Front:
0 2
5 4
Down:
4 3
0 3
Left:
5 5
4 3
Right:
1 0
2 2
Back:
5 3
1 2
[Step 3]
[Move] R2
[Current Cube State]
Upper:
1 3
1 3
Front:
0 1
5 5
Down:
4 4
0 0
Left:
5 5
4 3
Right:
2 2
0 1
Back:
4 3
2 2
[Step 4]
[Move] U'
[Current Cube State]
Upper:
3 3
1 1
Front:
5 5
5 5
Down:
4 4
0 0
Left:
4 3
4 3
Right:
0 1
0 1
Back:
2 2
2 2
[Step 5]
[Move] F
[Current Cube State]
Upper:
3 3
3 3
Front:
5 5
5 5
Down:
0 0
0 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 2
2 2
Finished.
Now strictly follow the above process to form Restoration Moves.
3. Restoration Moves: R2 F2 R2 U' F

[Initial Cube State]:
Upper:
5 1
0 2
Front:
5 0
2 2
Down:
1 1
2 4
Left:
4 1
4 3
Right:
4 3
0 5
Back:
5 3
0 3
[Solution 1]
[Step 1]
[Move] F'
[Current Cube State]
Upper:
5 1
4 0
Front:
0 2
5 2
Down:
1 3
2 4
Left:
4 2
4 0
Right:
1 3
1 5
Back:
5 3
0 3
[Step 2]
[Move] R2
[Current Cube State]
Upper:
5 3
4 4
Front:
0 0
5 5
Down:
1 1
2 0
Left:
4 2
4 0
Right:
5 1
3 1
Back:
2 3
2 3
[Step 3]
[Move] F'
[Current Cube State]
Upper:
5 3
5 3
Front:
0 5
0 5
Down:
2 0
2 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 3
2 3
[Step 4]
[Move] R
[Current Cube State]
Upper:
5 5
5 5
Front:
0 0
0 0
Down:
2 2
2 2
Left:
4 4
4 4
Right:
1 1
1 1
Back:
3 3
3 3
Finished.
Now strictly follow the above process to form Restoration Moves.
1. Restoration Moves: F' R2 F' R

[Solution 2]
[Process]:
[Step 1]
[Move] F
[Current Cube State]
Upper:
5 1
3 1
Front:
2 5
2 0
Down:
0 4
2 4
Left:
4 1
4 1
Right:
0 3
2 5
Back:
5 3
0 3
[Step 2]
[Move] R2
[Current Cube State]
Upper:
5 4
3 4
Front:
2 0
2 5
Down:
0 1
2 1
Left:
4 1
4 1
Right:
5 2
3 0
Back:
0 3
5 3
[Step 3]
[Move] F2
[Current Cube State]
Upper:
5 4
1 0
Front:
5 2
0 2
Down:
4 3
2 1
Left:
4 3
4 5
Right:
1 2
1 0
Back:
0 3
5 3
[Step 4]
[Move] R2
[Current Cube State]
Upper:
5 3
1 1
Front:
5 5
0 0
Down:
4 4
2 0
Left:
4 3
4 5
Right:
0 1
2 1
Back:
2 3
2 3
[Step 5]
[Move] F
[Current Cube State]
Upper:
5 3
5 3
Front:
0 5
0 5
Down:
2 0
2 0
Left:
4 4
4 4
Right:
1 1
1 1
Back:
2 3
2 3
[Step 6]
[Move] R
[Current Cube State]
Upper:
5 5
5 5
Front:
0 0
0 0
Down:
2 2
2 2
Left:
4 4
4 4
Right:
1 1
1 1
Back:
3 3
3 3
Finished.
Now strictly follow the above process to form Restoration Moves.
2. Restoration Moves: F R2 F2 R2 F R

[Solution 3]
[Process]:
[Step 1]
[Move] F'
[Current Cube State]
Upper:
5 1
4 0
Front:
0 2
5 2
Down:
1 3
2 4
Left:
4 2
4 0
Right:
1 3
1 5
Back:
5 3
0 3
[Step 2]
[Move] U2
[Current Cube State]
Upper:
0 4
1 5
Front:
5 3
5 2
Down:
1 3
2 4
Left:
1 3
4 0
Right:
4 2
1 5
Back:
0 2
0 3
[Step 3]
[Move] R2
[Current Cube State]
Upper:
0 3
1 4
Front:
5 0
5 0
Down:
1 4
2 5
Left:
1 3
4 0
Right:
5 1
2 4
Back:
2 2
3 3
[Step 4]
[Move] F
[Current Cube State]
Upper:
0 3
0 3
Front:
5 5
0 0
Down:
2 5
2 5
Left:
1 1
4 4
Right:
1 1
4 4
Back:
2 2
3 3
[Step 5]
[Move] R2
[Current Cube State]
Upper:
0 5
0 5
Front:
5 3
0 2
Down:
2 3
2 3
Left:
1 1
4 4
Right:
4 4
1 1
Back:
0 2
5 3
[Step 6]
[Move] U2
[Current Cube State]
Upper:
5 0
5 0
Front:
0 2
0 2
Down:
2 3
2 3
Left:
4 4
4 4
Right:
1 1
1 1
Back:
5 3
5 3
[Step 7]
[Move] R'
[Current Cube State]
Upper:
5 5
5 5
Front:
0 0
0 0
Down:
2 2
2 2
Left:
4 4
4 4
Right:
1 1
1 1
Back:
3 3
3 3
Finished.
Now strictly follow the above process to form Restoration Moves.
3. Restoration Moves: F' U2 R2 F R2 U2 R'

[Initial Cube State]
{state}
"""


# 1-shot
propose_prompt = '''
Please provide three possible next one move from [U, U', U2, R, R', R2, F, F', F2] based on the current state, which you think can lead us closer to restoration state.
[Current Cube State]:
Upper:
4 5
4 4
Front:
5 1
5 0
Down:
0 0
2 0
Left:
1 1
3 2
Right:
2 2
4 3
Back:
3 3
1 5
[Possible next move]:
R, U', F2

[Current Cube State]:
Upper:
0 0
0 0
Front:
4 4
1 1
Down:
5 5
2 2
Left:
3 3
3 3
Right:
1 1
4 4
Back:
2 2
5 5
[Possible next move]:
U2, F', U

[Current Cube State]:
{state}
[Possible next move]:
'''

value_prompt = '''
Evaluate if each face of Cube has same numbers after the move. (sure/likely/impossible)
[Current Cube State]:
Upper:
4 5
4 4
Front:
5 1
5 0
Down:
0 0
2 0
Left:
1 1
3 2
Right:
2 2
4 3
Back:
3 3
1 5
[Move]:
R
[After the Move]:
Upper:
4 0
4 0
Front:
5 5
0 1
Down:
0 1
2 2
Left:
1 1
3 3
Right:
2 2
4 3
Back:
4 3
5 5
[Evaluation]:
likely

[Current Cube State]:
Upper:
4 0
4 0
Front:
5 5
0 1
Down:
0 1
2 2
Left:
1 1
3 3
Right:
2 2
4 3
Back:
4 3
5 5
[Move]:
U'
[After the Move]:
Upper:
0 0
4 4
Front:
0 1
0 1
Down:
2 2
2 2
Left:
1 1
3 3
Right:
4 3
4 3
Back:
5 5
5 5
[Evaluation]:
likely

[Current Cube State]:
Upper:
0 0
4 4
Front:
0 1
0 1
Down:
2 2
2 2
Left:
1 1
3 3
Right:
4 3
4 3
Back:
5 5
5 5
[Move]:
F'
[After the Move]:
Upper:
0 0
0 0
Front:
1 1
1 1
Down:
2 2
2 2
Left:
3 3
3 3
Right:
4 4
4 4
Back:
5 5
5 5
[Evaluation]:
sure

[Current Cube State]:
{state}
[Move]:
{move}
[After the Move]:
{next_state}
[Evaluation]:
'''

merge_prompt = '''
Please select {n_select_sample} move from the proposed move list, which you believe can lead the current state to be closer to the restoration state. 
Note that you ONLY need to provide ONE STEP of candidate moves. If you have already found one, return the best next move and stop.
[Current Cube State]:
Upper:
4 5
4 4
Front:
0 0
2 0
Down:
1 1
3 2
Left:
2 2
4 3
Right:
5 1
5 0
Back:
3 3
1 5
[Proposed Move List]:
(1) R
[After the Move]:
Upper:
4 1
4 2
Front:
2 0
0 0
Down:
1 2
3 3
Left:
2 1
4 3
Right:
5 1
5 0
Back:
4 3
5 5

(2) F
[After the Move]:
Upper:
4 5
0 1
Front:
4 0
4 0
Down:
3 1
2 1
Left:
2 0
4 3
Right:
5 2
5 2
Back:
3 3
1 5
[Best Next Move Start]
(1) R
[Best Next Move End]
We've got the next move. Stop generating and return.

[Current Cube State]:
Upper:
0 0
4 4
Front:
2 2
2 2
Down:
1 1
3 3
Left:
4 3
4 3
Right:
0 1
0 1
Back:
5 5
5 5
[Proposed Move List]:
(1) U2
[After the Move]:
Upper:
4 4
0 0
Front:
0 1
2 2
Down:
5 5
3 3
Left:
4 3
4 3
Right:
2 2
0 1
Back:
1 1
5 5

(2) F'
[After the Move]:
Upper:
0 0
2 2
Front:
3 2
4 2
Down:
1 3
1 3
Left:
1 1
4 3
Right:
0 4
0 4
Back:
5 5
5 5
[Best Next Move Start]
(2) F'
[Best Next Move End]
We've got the next move. Stop generating and return.

[Current Cube State]:
{state}
[Proposed Move List]:
{move}
[Best Next Move Start]
'''

merge_prompt_3_select_sample='''
Please select {n_select_sample} move from the proposed move list, which you believe can lead the current state to be closer to the restoration state. 
Note that you ONLY need to provide ONE STEP of candidate moves. If you have already found 1-3 moves, return the best moves and stop.
[Current Cube State]:
Upper:
0 5
4 4
Front:
0 0
5 2
Down:
1 4
3 2
Left:
1 2
4 0
Right:
5 1
3 1
Back:
3 2
3 5

[Proposed Move List]:
(1) U
[After the Move]:
Upper:
4 0
4 5
Front:
5 1
5 2
Down:
1 4
3 2
Left:
0 0
4 0
Right:
3 2
3 1
Back:
1 2
3 5

(2) F
[After the Move]:
Upper:
0 5
0 2
Front:
5 0
2 0
Down:
3 5
3 2
Left:
1 1
4 4
Right:
4 1
4 1
Back:
3 2
3 5

(3) F'
[After the Move]:
Upper:
0 5
5 3
Front:
0 2
0 5
Down:
2 0
3 2
Left:
1 4
4 4
Right:
4 1
1 1
Back:
3 2
3 5

(4) R2
[After the Move]:
Upper:
0 4
4 2
Front:
0 3
5 3
Down:
1 5
3 4
Left:
1 2
4 0
Right:
1 3
1 5
Back:
2 2
0 5

(5) U2
[After the Move]:
Upper:
4 4
5 0
Front:
3 2
5 2
Down:
1 4
3 2
Left:
5 1
4 0
Right:
1 2
3 1
Back:
0 0
3 5

[Best Next Move Start]
(2) F
(3) F'
(1) U
[Best Next Move End]
We've got three next moves. Stop generating and return.

Please select {n_select_sample} move from the proposed move list, which you believe can lead the current state to be closer to the restoration state. 
Note that you ONLY need to provide ONE STEP of candidate moves. If you have already found 1-3 moves, return the best moves and stop.
[Current Cube State]:
{state}
[Proposed Move List]:
{move}
[Best Next Move Start]
'''