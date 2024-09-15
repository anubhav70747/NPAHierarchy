from __future__ import print_function
from ncpol2sdpa import *
import pickle
# just a basic code to run tri vs bi (or reverse) party NPA optimization
# use inequalities from inequalities.py
# whats up?
def chsh_AB(P):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
          if  x * y == u ^ v:
            chsh=chsh+P([u,v],[x,y],['A','B'])
  return chsh/4

def chsh_BC(P):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
          if  x * y == u ^ v:
            chsh=chsh+P([u,v],[x,y],['B','C'])
  return chsh/4
def __main__():

  P = Probability([2, 2], [2, 2], [2,2])
  Objective = chsh_BC(P) # set objective function


# set primary constraints here
  equalities = [chsh_AB(P)- 0.5*(1+1/(2**0.5))]
 
# prepare relaxation
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(4, substitutions = P.substitutions,momentequalities = equalities)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="cvxpy")
# collect data points
  print(abs(sdpRelaxation.primal))

if __name__=="__main__":
   __main__()
