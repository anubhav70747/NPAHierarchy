from __future__ import print_function
from ncpol2sdpa import *
from inequalities import * 
import pickle
# just a basic code to run tri vs bi (or reverse) party NPA optimization
# use inequalities from inequalities.py



def __main__():

  P = Probability([2, 2], [2, 2])
  Objective = chsh(P) # set objective function
  ConstraintsA = P([0],[0],['A']) # set primary constraint inequality
  ConstraintsB = P([0],[0],['B']) # set primary constraint inequality

# set primary constraints here
  ineq = []
  ineq.append(ConstraintsA - 0.5)
  ineq.append(-1*ConstraintsA + 0.5)
  ineq.append(ConstraintsB - 0.5)
  ineq.append(-1*ConstraintsB + 0.5)
# prepare relaxation
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="cvxopt")
# collect data points
  print(abs(sdpRelaxation.primal))

if __name__=="__main__":
   __main__()
