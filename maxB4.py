from __future__ import print_function
from ncpol2sdpa import *
import pickle
# for evaluating maximum value of B4 inequality



def exp_val(P, input_):
    vals = [-1, 1]
    return sum(a*b*P([a, b], input_) for a in vals for b in vals )

def B4(P):
    S = 0
    S = S + exp_val(P, [0,0]) + exp_val(P, [0,1]) + exp_val(P, [0,2]) + exp_val(P, [0,3])
    S = S + exp_val(P, [1,0]) + exp_val(P, [1,1]) - exp_val(P, [1,2]) - exp_val(P, [1,3])
    S = S + exp_val(P, [2,0]) - exp_val(P, [2,1]) + exp_val(P, [2,2]) - exp_val(P, [2,3])
    S = S + exp_val(P, [3,0]) - exp_val(P, [3,1]) - exp_val(P, [3,2]) + exp_val(P, [3,3])
    S = S + exp_val(P, [4,0]) + exp_val(P, [4,1]) + exp_val(P, [4,2]) - exp_val(P, [4,3])
    S = S + exp_val(P, [5,0]) + exp_val(P, [5,1]) - exp_val(P, [5,2]) + exp_val(P, [5,3])
    S = S + exp_val(P, [6,0]) - exp_val(P, [6,1]) + exp_val(P, [6,2]) + exp_val(P, [6,3])
    S = S + exp_val(P, [7,0]) - exp_val(P, [7,1]) - exp_val(P, [7,2]) - exp_val(P, [7,3])
    return S


def __main__():

  P = Probability([2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2])
  Objective = B4(P) # set objective function
# set primary constraints here
  ineq = []
 # ineq.append(Constraints - 0.45)
 # ineq.append(-1*Constraints + 0.45)
# prepare relaxation
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(3, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="mosek")
# collect data points
  print(abs(sdpRelaxation.primal))

if __name__=="__main__":
   __main__()
