from __future__ import print_function
from ncpol2sdpa import *
import pickle
# just a basic code to run tri vs bi (or reverse) party NPA optimization
# use inequalities from inequalities.py

def chsh_AB(P):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
          if  x * y == u ^ v:
            chsh=chsh+P([u,v],[x,y],['A','B'])
  return chsh/4


def __main__():

  P = Probability([2, 2], [2, 2])
  Objective = chsh_AB(P) # set objective function
  Constraints = P([0],[0],['A']) # set primary constraint inequality

# set primary constraints here
  ineq = []
  ineq.append(Constraints - 0.45)
  ineq.append(-1*Constraints + 0.45)
# prepare relaxation
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="cvxopt")
# collect data points
  print(abs(sdpRelaxation.primal))

if __name__=="__main__":
   __main__()
