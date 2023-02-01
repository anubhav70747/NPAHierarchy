from __future__ import print_function
from ncpol2sdpa import *
import sys
import pickle
# for evaluating critical detection of EBI inequality
def local_EBI_A(P):
    val= 2*(P([0], [0],['A']))-2*(P([1], [0],['A'])) +2*(P([0], [1],['A']))-2*(P([1], [1],['A']))+2*(P([0], [2],['A']))-2*(P([0], [2],['A']))   
    return -1*val
def local_EBI_B(P):
    return 3*(P([0], [0],['B'])-P([1], [0],['B'])) -P([0], [1],['B'])+P([1], [1],['B'])-P([0], [2],['B'])+P([1], [2],['B'])-P([0], [3],['B'])+P([1], [3],['B'])

def expectation_value_bi(P, input_ , parties):
    vals = [-1, 1]
    return sum(a*b*P([a, b], input_ ,parties) for a in vals for b in vals )

def EBI(P,etaA,etaB):
    EBI=0
    EBI = EBI + etaA*etaB*(expectation_value_bi(P, [0,0] ,['A','B']) + expectation_value_bi(P, [0, 1],['A','B']) - \
        expectation_value_bi(P, [0,2],['A','B']) - expectation_value_bi(P, [0, 3],['A','B'])+expectation_value_bi(P, [1,0] ,['A','B']) - expectation_value_bi(P, [1, 1],['A','B']) + \
        expectation_value_bi(P, [1,2],['A','B']) - expectation_value_bi(P, [1, 3],['A','B'])+expectation_value_bi(P, [2,0] ,['A','B']) - expectation_value_bi(P, [2, 1],['A','B']) - \
        expectation_value_bi(P, [2,2],['A','B']) + expectation_value_bi(P, [2, 3],['A','B']))
    EBI = EBI + etaB*(1-etaA)*local_EBI_B(P) + etaA*(1-etaB)*local_EBI_A(P)
    EBI = EBI + 6*(1-etaA)*(1-etaB)
    return EBI

def __main__():
  x = []
  y = []
  eta = 0.5
  loop_control=0
  ineq = []
  while loop_control <= 6.0000001:
    P = Probability([2, 2, 2], [2, 2, 2, 2])
    Objective = EBI(P,1,eta) # set objective function
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
    eta = eta + 0.01


if __name__=="__main__":
   __main__()