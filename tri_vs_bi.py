from __future__ import print_function
from inequalities import *
from ncpol2sdpa import *
import pickle
# just a basic code to run tri vs bi (or reverse) party NPA optimization
# use inequalities from inequalities.py

def __main__():

  P = Probability([2, 2], [2, 2], [2, 2])
  Objective = mermin_game_2(P) # set objective function
  Constraints1 = mermin_game_2(P)# set primary constraint inequality
  flag=0 # a loop control variable to make the loop the limit case
  dx = 0.77 # set initialization for primary constraint
  div = 1.0 # normalization factor
  step = 0.01 # incremental value for primary constraint
  lim = 0.7818 # upper bound to the primary constraint
  x = []
  y = []

  while dx  <= lim :
    print (dx)
# set primary constraints here
    ineq = []
    ineq.append(Constraints1 - dx)
    ineq.append(-1*Constraints1 + dx)
# prepare relaxation
    sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
    sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
    sdpRelaxation.set_objective(-Objective)
    sdpRelaxation.solve(solver="cvxopt")
# collect data points
    x.append(dx)
    y.append(abs(sdpRelaxation.primal)/div)
    print(abs(sdpRelaxation.primal)/div)
    if (dx + step > lim) & (flag==0):
      dx=lim
      flag=1
    else:
      dx = dx + step
#  with open('../Plotting/data/chshvsgyniQ.plot','wb') as fp:                                                pickle.dump([x,y],fp)

if __name__=="__main__":
   __main__()
