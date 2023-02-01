from __future__ import print_function
from ncpol2sdpa import *
import sys
import pickle

def local_chsh(P, party):
    return 2*(P([0], [0],party)-P([1], [0],party))    

def expectation_value_bi(P, input_ , parties):
    vals = [-1, 1]
    return sum(a*b*P([a, b], input_ ,parties) for a in vals for b in vals )

def chsh(P,etaA,etaB):
    chsh=0
    chsh = chsh + etaA*etaB*(expectation_value_bi(P, [0,0] ,['A','B']) + expectation_value_bi(P, [0, 1],['A','B']) + \
        expectation_value_bi(P, [1,0],['A','B']) - expectation_value_bi(P, [1, 1],['A','B']))
    chsh = chsh + etaB*(1-etaA)*local_chsh(P,['B']) + etaA*(1-etaB)*local_chsh(P,['A'])
    chsh = chsh + 2*(1-etaA)*(1-etaB)
    return chsh

def __main__():
  x = []
  y = []
  eta = 0.5
  loop_control=0
  ineq = []
  while loop_control <= 2.0000001:
    P = Probability([2, 2], [2, 2])
    Objective = chsh(P,1,eta) # set objective function
# prepare relaxation
    sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
    sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
    sdpRelaxation.set_objective(-Objective)
    sdpRelaxation.solve(solver="mosek")
# collect data points
    loop_control=(abs(sdpRelaxation.primal))
      #print(etaA,etaB,'------->',loop_control)
# update counter
    print(eta,'*******',loop_control)
    eta = eta + 0.001


if __name__=="__main__":
   __main__()