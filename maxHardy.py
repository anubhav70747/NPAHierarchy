from __future__ import print_function
from ncpol2sdpa import *
import pickle


# for evaluating maximum value of the Hardy's inequality



def __main__():
  eps=0.313
  lev=8
  P = Probability([2, 2], [2, 2])
  Objective = P([0,0],[1,1],['A','B']) # set objective function
  
# set primary constraints here
  ineq = []
 # ineq.append(P([0,0],[0,0],['A','B']) - eps)
  ineq.append(-1*P([0,0],[0,0],['A','B']) + eps)

 # ineq.append(P([0,1],[1,0],['A','B']) - eps)
  ineq.append(-1*P([0,1],[1,0],['A','B']) + eps)
  
 # ineq.append(P([1,0],[0,1],['A','B']) - eps)
  ineq.append(-1*P([1,0],[0,1],['A','B']) + eps)
# prepare relaxation
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(lev , substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="mosek")
# collect data points
  print(abs(sdpRelaxation.primal))

if __name__=="__main__":
   __main__()
 