from __future__ import print_function
from ncpol2sdpa import *
import pickle
# for evaluating maximum value unbalanced tripartite inequality
def expectation_value_tri(P, input_):
    vals = [-1, 1]
    return sum(a*b*c*P([a, b, c], input_) for a in vals for b in vals for c in vals)

def unbalanced(P):
    val=3*expectation_value_tri(P,[0,0,0])+expectation_value_tri(P,[0,0,1])+expectation_value_tri(P,[0,1,0])-expectation_value_tri(P,[0,1,1])+expectation_value_tri(P,[1,0,0])-expectation_value_tri(P,[1,0,1])-expectation_value_tri(P,[1,1,0])+expectation_value_tri(P,[1,1,1])
    return val
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

  P = Probability([2, 2], [2, 2], [2,2])
  Objective =unbalanced(P) # set objective function
#  Constraints = chsh_AB(P)
# Objective = unbalanced(P)
# set primary constraints here
  ineq = []
#  ineq.append(Constraints - 0.5*(1+0.5**0.5))
#  ineq.append(-1*Constraints + 0.5*(1+0.5**0.5))
# prepare relaxation
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(3, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="mosek")
# collect data points
  print(abs(sdpRelaxation.primal))

if __name__=="__main__":
   __main__()
