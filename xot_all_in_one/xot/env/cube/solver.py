# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from __future__ import print_function
import numpy as np
from . import py222

hO = np.ones(729, dtype=int) * 12
hP = np.ones(117649, dtype=int) * 12

moveStrs = {0: "U", 1: "U'", 2: "U2", 3: "R", 4: "R'", 5: "R2", 6: "F", 7: "F'", 8: "F2"}

# generate pruning table for the piece orientation states
def genOTable(s, d, lm=-3):
  index = py222.indexO(py222.getOP(s))
  if d < hO[index]:
    hO[index] = d
    for m in range(9):
      if int(m / 3) == int(lm / 3):
        continue
      genOTable(py222.doMove(s, m), d + 1, m)

# generate pruning table for the piece permutation states
def genPTable(s, d, lm=-3):
  index = py222.indexP(py222.getOP(s))
  if d < hP[index]:
    hP[index] = d
    for m in range(9):
      if int(m / 3) == int(lm / 3):
        continue
      genPTable(py222.doMove(s, m), d + 1, m)

# IDA* which prints all optimal solutions
def IDAStar(s, d, moves, lm=-3, solvemove=set()):

  if py222.isSolved(s):
    solvemove.add(" ".join(tuple(GetMoves(moves))))
                  
    return True, solvemove
  else:
    sOP = py222.getOP(s)
    if d > 0 and d >= hO[py222.indexO(sOP)] and d >= hP[py222.indexP(sOP)]:
      dOptimal = False
      for m in range(9):
        if int(m / 3) == int(lm / 3):
          continue
        newMoves = moves[:]; newMoves.append(m)
        solved, _ = IDAStar(py222.doMove(s, m), d - 1, newMoves, m, solvemove)
        if solved and not dOptimal:
          dOptimal = True
      if dOptimal:
        # solvemove.append(GetMoves(moves))
        return True, solvemove
  return False, solvemove

# print a move sequence from an array of move indices
# def printMoves(moves):
#   moveStr = ""
#   for m in moves:
#     moveStr += moveStrs[m] + " "
#   print(moveStr)


def GetMoves(moves):
  movelist = []
  for m in moves:
    movelist.append(moveStrs[m])
  return movelist



# solve a cube state
def solveCube(s, verbose=0):
  # print cube state
  if verbose > 0:
    py222.printCube(s)

  # FC-normalize stickers
  if verbose > 0:
    print("normalizing stickers...")
  s = py222.normFC(s)

  # generate pruning tables
  if verbose > 0:
    print("generating pruning tables...")
  genOTable(py222.initState(), 0)
  genPTable(py222.initState(), 0)

  # run IDA*
  if verbose > 0:
    print("searching...")
  solved = False
  depth = 1

  while depth <= 11 and not solved:
    if verbose > 0:
      print("depth {}".format(depth))
    
    solved, moves = IDAStar(s, depth, [], solvemove=set())
    if solved:
      depth = 0 if list(moves)[0] == "" else depth
      return list(moves), depth
    # print(solved, moves)
    depth += 1

  return 


