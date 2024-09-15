from __future__ import print_function
from ncpol2sdpa import *
import pickle
import math

# generic binary symmetric noisy channel
def noisyChannel(ep):
  return [[ep,1-ep],[ep,1-ep]]

# evaluate the wire-cut Bell inequality corresponding to the antidistinguishability task
def AntiDistBell(P,ep):
  sum = 1
  for a in range(2):
    for a1 in range(2):
      for x in range(4):
        p = noisyChannel(ep)
        sum = sum - 0.25*p[a1][a]*P([a,x],[x,a1],['A','B'])
  return sum
def Capacity(ep):
  return 1 + (ep*math.log(ep,2) + (1-ep)*math.log(1-ep,2))

def __main__():
  ep = 0.8
  P = Probability([2, 2, 2, 2], [4, 4])
  Objective = AntiDistBell(P,ep) # set objective function
#  Constraints = P([0],[0],['A']) # set primary constraint inequality

# set primary constraints here
  ineq = []
#  ineq.append(Constraints - 0.45)
#  ineq.append(-1*Constraints + 0.45)
# prepare relaxation
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="mosek")
# collect data points
  print(abs(sdpRelaxation.primal))
  print(Capacity(ep))
if __name__=="__main__":
   __main__()
