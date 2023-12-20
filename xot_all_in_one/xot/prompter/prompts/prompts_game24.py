# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

game24_instruct = '''
Use numbers and basic arithmetic operations (+ - * /) to obtain 24.
'''

# 5-shot
standard_prompt = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24.
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) = 24
Input: 2 9 10 12
Answer: 2 * 12 * (10 - 9) = 24
Input: 4 9 10 13
Answer: (13 - 9) * (10 - 4) = 24
Input: 1 4 8 8
Answer: (8 / 4 + 1) * 8 = 24
Input: 5 5 5 9
Answer: 5 + 5 + 5 + 9 = 24
Input: {state}
'''

# 5-shot
standard_prompt_multi = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. 
There may be multiple solutions to a problem, please find 3 correct answers if there are multiple answers to the problem. Otherwise, only the only correct answer can be returned.
Input: 4 4 6 8
[Solution]
Answer: (4 + 8) * (6 - 4) = 24
[Solution]
Answer: ((4 - 6) + 8) * 4 = 24
[Solution]
Answer: (8 - (6 - 4)) * 4 = 24

Input: 2 9 10 12
[Solution]
Answer: 2 * 12 * (10 - 9) = 24
[Solution]
Answer: (2 * 12) / (10 - 9) = 24
[Solution]
Answer: (9 - 12) * (2 - 10) = 24

Input: 4 9 10 13
[Solution]
Answer: (13 - 9) * (10 - 4) = 24
[Solution]
Answer: 4 * ((9 + 10) - 13) = 24
[Solution]
Answer: (9 - 13) * (4 - 10) = 24

Input: 1 4 8 8
[Solution]
Answer: (8 / 4 + 1) * 8 = 24
[Solution]
Answer: (8 * (4 * 1)) - 8 = 24
[Solution]
Answer: ((8 * 4) - 8) * 1 = 24

Input: 5 5 5 9
[Solution]
Answer: 5 + 5 + 5 + 9 = 24

Input: {state}
'''


# 5-shot
cot_prompt = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Each step, you are only allowed to choose two of the remaining numbers to obtain a new number.
Input: 4 4 6 8
Steps:
4 + 8 = 12 (left: 4 6 12)
6 - 4 = 2 (left: 2 12)
2 * 12 = 24 (left: 24)
Answer: (6 - 4) * (4 + 8) = 24
Input: 2 9 10 12
Steps:
12 * 2 = 24 (left: 9 10 24)
10 - 9 = 1 (left: 1 24)
24 * 1 = 24 (left: 24)
Answer: (12 * 2) * (10 - 9) = 24
Input: 4 9 10 13
Steps:
13 - 10 = 3 (left: 3 4 9)
9 - 3 = 6 (left: 4 6)
4 * 6 = 24 (left: 24)
Answer: 4 * (9 - (13 - 10)) = 24
Input: 1 4 8 8
Steps:
8 / 4 = 2 (left: 1 2 8)
1 + 2 = 3 (left: 3 8)
3 * 8 = 24 (left: 24)
Answer: (1 + 8 / 4) * 8 = 24
Input: 5 5 5 9
Steps:
5 + 5 = 10 (left: 5 9 10)
10 + 5 = 15 (left: 9 15)
15 + 9 = 24 (left: 24)
Answer: ((5 + 5) + 5) + 9 = 24
Input: {state}
'''

# 5-shot
cot_prompt_multi = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Each step, you are only allowed to choose two of the remaining numbers to obtain a new number. Use numbers and basic arithmetic operations (+ - * /) to obtain 24. 
There may be multiple solutions to a problem, please find 3 correct answers if there are multiple answers to the problem. Otherwise, only the only correct answer can be returned.
Please provide each [Solution] with **exact three steps thoughts**.
Input: 4 4 6 8
[Solution]
Steps:
4 + 8 = 12 (left: 4 6 12)
6 - 4 = 2 (left: 2 12)
2 * 12 = 24 (left: 24)
Answer: (6 - 4) * (4 + 8) = 24
[Solution]
Steps:
8 - 6 = 2 (left: 2 4 4)
4 + 2 = 6 (left: 4 6)
6 * 4 = 24 (left: 24)
Answer: (4 + (8 - 6)) * 4 = 24
[Solution]
Steps:
6 - 4 = 2 (left: 2 4 8)
8 - 2 = 6 (left: 4 6)
6 * 4 = 24 (left: 24)
Answer:  (8 - (6 - 4)) * 4 = 24

Input: 2 9 10 12
[Solution]
Steps:
12 * 2 = 24 (left: 9 10 24)
10 - 9 = 1 (left: 1 24)
24 * 1 = 24 (left: 24)
Answer: (12 * 2) * (10 - 9) = 24
[Solution]
Steps:
10 - 2 = 8 (left: 8 9 12)
12 - 9 = 3 (left: 3 8)
3 * 8 = 24 (left: 24)
Answer: (10 - 2) * (12 - 9) = 24
[Solution]
Steps:
2 - 10 = -8 (left: -8 9 12)
9 - 12 = -3 (left: -3 -8)
-3 * -8 = 24 (left: 24)
Answer: (2 - 10) * (9 - 12) = 24


Input: 4 9 10 13
[Solution]
Steps:
13 - 10 = 3 (left: 3 4 9)
9 - 3 = 6 (left: 4 6)
4 * 6 = 24 (left: 24)
Answer: 4 * (9 - (13 - 10)) = 24
[Solution]
Steps:
13 - 9 = 4 (left: 4 4 10)
10 - 4 = 6 (left: 4 6)
4 * 6 = 24 (left: 24)
Answer: (13 - 9) * (10 - 4) = 24
[Solution]
Steps:
9 - 13 = -4 (left: -4 4 10)
4 - 10 = -6 (left: -4 -6)
-4 * -6 = 24 (left: 24)
Answer: (9 - 13) * (4 - 10) = 24

Input: 1 4 8 8
[Solution]
Steps:
8 / 4 = 2 (left: 1 2 8)
1 + 2 = 3 (left: 3 8)
3 * 8 = 24 (left: 24)
Answer: (1 + 8 / 4) * 8 = 24
[Solution]
Steps:
4 * 8 = 32 (left: 1 8 32)
1 * 8 = 8 (left: 8 32)
32 - 8 = 24 (left: 24)
Answer: (4 * 8) - (1 * 8) = 24
[Solution]
Steps:
8 - 4 = 4 (left: 1 4 8)
4 - 1 = 3 (left: 3 8)
8 * 3 = 24 (left: 24)
Answer: 8 * ((8 - 4) - 1) = 24

Input: 5 5 5 9
[Solution]
Steps:
5 + 5 = 10 (left: 5 9 10)
10 + 5 = 15 (left: 9 15)
15 + 9 = 24 (left: 24)
Answer: ((5 + 5) + 5) + 9 = 24
Input: {state}
'''

game24_xot_revised_prompt = """
Using the given [input] numbers and basic arithmetic operations (+, -, *, /), follow the steps strictly to achieve a result of 24. 
All the [input] numbers can reach 24 by basic arithmetic operations (+, -, *, /).
If the final answer is not exactly 24, then the corresponding [Steps] is considered [wrong]. Please help me identify the exact wrong step based on its left number, among [Step 1, Step 2, Step 3]. If you are uncertain about which step is wrong, please begin your analysis with [Step 1] for better understanding.
Input: 2 9 10 12
Steps:
[Steps 1] 12 * 2 = 24 (left: 9 10 24) Expression: 9, 10, (12) * (2)
[Steps 2] 24 - 10 = 14 (left: 9 14) Expression: 9, ((12) * (2)) - (10)
[Steps 3] 9 + 14 = 23 (left: 23) Expression: (9) + ((12) * (2)) - (10)
The Steps are wrong. Because it can not reach 24 in the end. To be specific, 23 is not equal to 24.
[Steps 2] is wrong. Because it is impossible to reach 24 from the step 2. After Step 2, left numbers are 9, 13. 
9 + 13 = 22
9 * 13 = 111
9 -  13 = -4
It is impossible to reach 24 from [Steps 2].

Input: 4 9 10 13
Steps:
[Steps 1] 13 + 10 = 23 (left: 4 9 23) Expression: 4, 9, (13) + (10)
[Steps 2] 9 + 4 = 13 (left: 13 23) Expression: (9) + (4), (13) + (10)
[Steps 3] 23 - 13 = 10 (left: 10) Expression: ((13) + (10)) - ((9) + (4)) 
The Steps are wrong. Because it can not reach 24 in the end. To be specific, 10 is not equal to 24. 
All steps are wrong. Because it is impossible to reach 24 from the step 1. After Step 1, left numbers are 4, 9, 23. 
4 * 9 + 23 = 59
23 + (9 - 4) = 28
23 - 9 + 4 = 18
It is impossible to reach 24 from [Steps 1].

Input: 4 4 6 8
Steps:
[Steps 1] 4 - 8 = 12 (left: 4 6 -4) Expression: 4, 6, (4) - (8)
[Steps 2] 6 - 4 = 2 (left: 2 -4) Expression: (6) - (4), (4) - (8)
[Steps 3] 2 * -4 = -8 (left: -8) Expression: ((6) - (4)) * ((4) - (8))
The Steps are wrong. Because it can not reach 24 in the end. To be specific, -8 is not equal to 24. 
All steps are wrong. Because it is impossible to reach 24 from the step 1. After Step 1, left numbers are 4, 6 -4. 
4 - (-4) + 6 = 14
(4 - (-4)) * 6 = 48
(4 * (-4)) * 6 = -96
It is impossible to reach 24 from [Steps 1].

Input: {state}
Steps:
{move}
The Steps are wrong. Because it can not reach 24 in the end. To be specific, 
"""


game24_xot_prompt_wo_laststep = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. For each step, you are only allowed to choose two of the remaining numbers to obtain a new number.
The last step is not provided. Please complete the last step and return the answer. 
For example, the last step could be:
a) 2 * 12 = 24 (left: 24); 
b) 1 * 24 = 24 (left: 24); 
c) 4 * 6 = 24 (left: 24); 
d) 3 * 8 = 24 (left: 24); 
e) 9 + 15 = 24 (left: 24)
...

Input: 4 4 6 8
Steps:
4 + 8 = 12 (left: 4 6 12) Expression: 4, 6, (4) + (8)
6 - 4 = 2 (left: 12 2) Expression: (4) + (8), (6) - (4)
2 * 12 = 24 (left: 24) Expression: ((6) - (4)) * ((4) + (8))
Answer: (6 - 4) * (4 + 8) = 24

Input: 2 9 10 12
Steps:
12 * 2 = 24 (left: 9 10 24) Expression: 9, 10, (12) * (2)
10 - 9 = 1 (left: 24 1) Expression: (12) * (2), (10) - (9)
1 * 24 = 24 (left: 24) Expression: ((10) - (9)) * ((12) * (2)) 
Answer: (12 * 2) * (10 - 9) = 24

Input: 4 9 10 13
Steps:
13 - 10 = 3 (left: 4 9 3) Expression: 4, 9, (13) - (10)
9 - 3 = 6 (left: 4 6) Expression: 4, (9) - ((13) - (10))
4 * 6 = 24 (left: 24) Expression: (4) * ((9) - ((13) - (10)))
Answer: 4 * (9 - (13 - 10)) = 24

Input: 1 4 8 8
Steps:
8 / 4 = 2 (left: 1 8 2) Expression: 1, 8, (8) / (4)
1 + 2 = 3 (left: 8 3) Expression: 8, (1) + ((8) / (4))
3 * 8 = 24 (left: 24) Expression: ((1) + ((8) / (4))) * (8)
Answer: (1 + 8 / 4) * 8 = 24

Input: 5 5 5 9
Steps:
5 + 5 = 10 (left: 5 9 10) Expression: 5, 9, (5) + (5)
10 + 5 = 15 (left: 9 15) Expression: 9, ((5) + (5)) + (5)
9 + 15 = 24 (left: 24) Expression: (9) + (((5) + (5)) + (5))
Answer: ((5 + 5) + 5) + 9 = 24

Input: {state}
Steps: {move}
'''


game24_xot_prompt = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. For each step, you are only allowed to choose two of the remaining numbers to obtain a new number.
Input: 4 4 6 8
Steps:
4 + 8 = 12 (left: 4 6 12) Expression: 4, 6, (4) + (8)
6 - 4 = 2 (left: 12 2) Expression: (4) + (8), (6) - (4)
2 * 12 = 24 (left: 24) Expression: ((6) - (4)) * ((4) + (8))
Answer: (6 - 4) * (4 + 8) = 24

Input: 2 9 10 12
Steps:
12 * 2 = 24 (left: 9 10 24) Expression: 9, 10, (12) * (2)
10 - 9 = 1 (left: 24 1) Expression: (12) * (2), (10) - (9)
1 * 24 = 24 (left: 24) Expression: ((10) - (9)) * ((12) * (2)) 
Answer: (12 * 2) * (10 - 9) = 24

Input: 4 9 10 13
Steps:
13 - 10 = 3 (left: 4 9 3) Expression: 4, 9, (13) - (10)
9 - 3 = 6 (left: 4 6) Expression: 4, (9) - ((13) - (10))
4 * 6 = 24 (left: 24) Expression: (4) * ((9) - ((13) - (10)))
Answer: 4 * (9 - (13 - 10)) = 24

Input: 1 4 8 8
Steps:
8 / 4 = 2 (left: 1 8 2) Expression: 1, 8, (8) / (4)
1 + 2 = 3 (left: 8 3) Expression: 8, (1) + ((8) / (4))
3 * 8 = 24 (left: 24) Expression: ((1) + ((8) / (4))) * (8)
Answer: (1 + 8 / 4) * 8 = 24

Input: 5 5 5 9
Steps:
5 + 5 = 10 (left: 5 9 10) Expression: 5, 9, (5) + (5)
10 + 5 = 15 (left: 9 15) Expression: 9, ((5) + (5)) + (5)
9 + 15 = 24 (left: 24) Expression: (9) + (((5) + (5)) + (5))
Answer: ((5 + 5) + 5) + 9 = 24

Input: {state}
Steps: {move}
'''


game24_xot_prompt_multi = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Each step, you are only allowed to choose two of the remaining numbers to obtain a new number.
There may be multiple solutions to a problem, please find 3 correct answers if there are multiple answers to the problem. Otherwise, only the only correct answer can be returned.
Input: 4 4 6 8
[Solution 1]
Steps:
4 + 8 = 12 (left: 4 6 12) Expression: 4, 6, (4) + (8)
6 - 4 = 2 (left: 12 2) Expression: (4) + (8), (6) - (4)
2 * 12 = 24 (left: 24) Expression: ((6) - (4)) * ((4) + (8))
[Solution 2]
Steps:
8 - 6 = 2 (left: 4 4 2) Expression: 4, 4, (8) - (6)
4 + 2 = 6 (left: 4 6) Expression: 4, (4) + ((8) - (6))
6 * 4 = 24 (left: 24) Expression: ((4) + ((8) - (6))) * (4)
[Solution 3]
Steps:
6 - 4 = 2 (left: 4 8 2) Expression: 4, 8, (6) - (4)
8 - 2 = 6 (left: 4 6) Expression: 4, (8) - ((6) - (4))
6 * 4 = 24 (left: 24) Expression: ((8) - ((6) - (4))) * (4)
Answer 1: (6 - 4) * (4 + 8) = 24
Answer 2: (4 + (8 - 6)) * 4 = 24
Answer 3:  (8 - (6 - 4)) * 4 = 24

Input: 2 9 10 12
[Solution 1]
Steps:
12 * 2 = 24 (left: 9 10 24) Expression: 9, 10, (12) * (2)
10 - 9 = 1 (left: 24 1) Expression: (12) * (2), (10) - (9)
24 * 1 = 24 (left: 24) Expression: ((12) * (2)) * ((10) - (9))
[Solution 2]
Steps:
10 - 2 = 8 (left: 9 12 8) Expression: 9, 12, (10) - (2)
12 - 9 = 3 (left: 8 3) Expression: (10) - (2), (12) - (9)
3 * 8 = 24 (left: 24) Expression: ((12) - (9)) * ((10) - (2))
[Solution 3]
Steps:
2 - 10 = -8 (left: 9 12 -8) Expression: 9, 12, (2) - (10)
9 - 12 = -3 (left: -8 -3) Expression: (2) - (10), (9) - (12)
-3 * -8 = 24 (left: 24) Expression: ((9) - (12)) * ((2) - (10))
Answer 1: (12 * 2) * (10 - 9) = 24
Answer 2: (12 - 9) * (10 - 2) = 24
Answer 3: (9 - 12) * (2 - 10) = 24


Input: 4 9 10 13
[Solution 1]
Steps:
13 - 10 = 3 (left: 4 9 3) Expression: 4, 9, (13) - (10)
9 - 3 = 6 (left: 4 6) Expression: 4, (9) - ((13) - (10))
4 * 6 = 24 (left: 24) Expression: (4) * ((9) - ((13) - (10)))
[Solution 2]
Steps:
13 - 9 = 4 (left: 4 10 4) Expression: 4, 10, (13) - (9)
10 - 4 = 6 (left: 4 6) Expression: (13) - (9), (10) - (4)
4 * 6 = 24 (left: 24) Expression: ((13) - (9)) * ((10) - (4))
[Solution 3]
Steps:
9 - 13 = -4 (left: 4 10 -4) Expression: 4, 10, (9) - (13)
4 - 10 = -6 (left: -4 -6) Expression: (9) - (13), (4) - (10)
-4 * -6 = 24 (left: 24) Expression: ((9) - (13)) * ((4) - (10))
Answer 1: 4 * (9 - (13 - 10)) = 24
Answer 2: (13 - 9) * (10 - 4) = 24
Answer 3: (9 - 13) * (4 - 10) = 24

Input: 1 4 8 8
[Solution 1]
Steps:
8 / 4 = 2 (left: 1 8 2) Expression: 1, 8, (8) / (4)
1 + 2 = 3 (left: 8 3) Expression: 8, (1) + ((8) / (4))
3 * 8 = 24 (left: 24) Expression: ((1) + ((8) / (4))) * (8)
[Solution 2]
Steps:
4 * 8 = 32 (left: 1 8 32) Expression: 1, 8, (4) * (8)
1 * 8 = 8 (left: 32 8) Expression: (4) * (8), (1) * (8)
32 - 8 = 24 (left: 24) Expression: ((4) * (8)) - ((1) * (8))
[Solution 3]
Steps:
8 - 4 = 4 (left: 1 8 4) Expression: 1, 8, (8) - (4)
4 - 1 = 3 (left: 8 3) Expression: 8, ((8) - (4)) - (1)
8 * 3 = 24 (left: 24) Expression: (8) * (((8) - (4)) - (1))
Answer 1: (1 + 8 / 4) * 8 = 24
Answer 2: (4 * 8) - (1 * 8) = 24
Answer 3: 8 * ((8 - 4) - 1) = 24

Input: 5 5 5 9
[Solution 1]
Steps:
5 + 5 = 10 (left: 5 9 10) Expression: 5, 9, (5) + (5)
10 + 5 = 15 (left: 9 15) Expression: 9, ((5) + (5)) + (5)
15 + 9 = 24 (left: 24) Expression: (((5) + (5)) + (5)) + (9)
Answer 1: ((5 + 5) + 5) + 9 = 24

Input: {state}
{move}
'''

# 1-shot
propose_prompt = '''Pick ONLY TWO numbers from the Input and return Possible next steps.
Input: 2 8 8 14
Possible next steps:
2 + 8 = 10 (left: 8 10 14)
8 / 2 = 4 (left: 4 8 14)
14 + 2 = 16 (left: 8 8 16)
2 * 8 = 16 (left: 8 14 16)
8 - 2 = 6 (left: 6 8 14)
14 - 8 = 6 (left: 2 6 8)
14 /  2 = 7 (left: 7 8 8)
14 - 2 = 12 (left: 8 8 12)

Input: {state}
Possible next steps:
'''

value_prompt = '''Evaluate if given numbers can reach 24 (sure/likely/impossible)
10 14
10 + 14 = 24
sure
11 12
11 + 12 = 23
12 - 11 = 1
11 * 12 = 132
11 / 12 = 0.91
impossible
4 4 10
4 + 4 + 10 = 8 + 10 = 18
4 * 10 - 4 = 40 - 4 = 36
(10 - 4) * 4 = 6 * 4 = 24
sure
4 9 11
9 + 11 + 4 = 20 + 4 = 24
sure
5 7 8
5 + 7 + 8 = 12 + 8 = 20
(8 - 5) * 7 = 3 * 7 = 21
I cannot obtain 24 now, but numbers are within a reasonable range
likely
5 6 6
5 + 6 + 6 = 17
(6 - 5) * 6 = 1 * 6 = 6
I cannot obtain 24 now, but numbers are within a reasonable range
likely
10 10 11
10 + 10 + 11 = 31
(11 - 10) * 10 = 10
10 10 10 are all too big
impossible
1 3 3
1 * 3 * 3 = 9
(1 + 3) * 3 = 12
1 3 3 are all too small
impossible
{state}
'''

value_last_step_prompt = '''Use numbers and basic arithmetic operations (+ - * /) to obtain 24. Given an input and an answer, give a judgement (sure/impossible) if the answer is correct, i.e. it uses each input exactly once and no other numbers, and reach 24.
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) = 24
Judge: 
sure
Input: 2 9 10 12
Answer: 2 * 12 * (10 - 9) = 24
Judge: 
sure
Input: 4 9 10 13
Answer: (13 - 9) * (10 - 4) = 24
Judge: 
sure
Input: 4 4 6 8
Answer: (4 + 8) * (6 - 4) + 1 = 25
Judge: 
impossible
Input: 2 9 10 12
Answer: 2 * (12 - 10) = 24
Judge: 
impossible
Input: 4 9 10 13
Answer: (13 - 4) * (10 - 9) = 24
Judge: 
impossible
Input: {state}
Answer: {answer}
Judge:'''

merge_prompt_multi = '''
Please strictly {n_select_sample} step from the proposed step list, which you believe can lead the input number to be closer to the goal of 24.
[Input]: 
2 8 8 14
[Proposed next steps]:
(1) 8 / 2 = 4 (left: 4 8 14)
(2) 14 + 2 = 16 (left: 8 8 16)
(3) 8 - 8 = 0 (left 0 2 14)
(4) 14 - 8 = 6 (left 2 6 8)
(5) 8 - 2 = 6 (left 6 8 14)
(6) 2 / 8 = 0.25 (left 0.25 8 14)
[Best Next Step Set]:
(1) 8 / 2 = 4 (left: 4 8 14)
(4) 14 - 8 = 6 (left 2 6 8)
(6) 2 / 8 = 0.25 (left 0.25 8 14)

[Input]: 
4 8 8
[Proposed next steps]:
(1) 4 * 8 = 32 (left: 8 32)
(2) 8 * 8 = 64 (left: 4 64)
(3) 4 - 8 = -4 (left: -4 8)
(4) 8 - 8 = 0 (left: 0 4)
(5) 8 / 4 = 2 (left: 2 8)
[Best Next Step Set]:
(1) 4 * 8 = 32 (left: 8 32)
(2) 8 * 8 = 64 (left: 4 64)
(5) 8 / 4 = 2 (left: 2 8)

[Input]: 
{state}
[Proposed next steps]:
{proposal}
[Best Next Step Set]:
'''

merge_prompt = '''
Please select {n_select_sample} step from the proposed step list, which you believe can lead the input number to be closer to the goal of 24.
[Input]: 
2 8 8 14
[Proposed next steps]:
(1) 8 / 2 = 4 (left: 4 8 14)
(2) 14 + 2 = 16 (left: 8 8 16)
[Best Next Step]:
(1) 8 / 2 = 4 (left: 4 8 14)

[Input]: 
4 8 8
[Proposed next steps]:
(1) 8 * 8 = 64 (left: 4 64)
(2) 4 * 8 = 32 (left: 8 32)
[Best Next Step]:
(2) 4 * 8 = 32 (left: 8 32)

[Input]: 
{state}
[Proposed next steps]:
{proposal}
[Best Next Step]:
'''



