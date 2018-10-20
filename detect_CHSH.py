from __future__ import print_function
from ncpol2sdpa import *
import sys
import pickle

def chsh_AB(P,etaA,etaB):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
          if  x * y == u ^ v:
            chsh=chsh+P([u,v],[x,y],['A','B'])
  chsh_mod=(chsh)*etaA*etaB + (2*P([0],[0],['A'])+1)*etaA*(1-etaB) + (2*P([0],[0],['B'])+1)*etaB*(1-etaA) + 3*(1-etaA)*(1-etaB)
  return chsh_mod/4


def __main__():
  x = []
  y = []
  etaA = 2/3.0
  lim_etaA = 1.02
  while etaA <= lim_etaA:
    etaB=0.5
    P = Probability([2, 2], [2, 2])
    loop_control=0
    while loop_control <= 0.75:
      etaB = etaB + 0.001
      Objective = chsh_AB(P,etaA,etaB) # set objective function
#  Constraints = P([0],[0],['A']) # set primary constraint inequality

# set primary constraints here
      ineq = []
#  ineq.append(Constraints - 0.45)
#  ineq.append(-1*Constraints + 0.45)
# prepare relaxation
      sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
      sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
      sdpRelaxation.set_objective(-Objective)
      sdpRelaxation.solve(solver="cvxopt")
# collect data points
      loop_control=(abs(sdpRelaxation.primal))
      print(etaA,etaB,'------->',loop_control)
# update counter
    print(etaA,'----------------',etaB)
    x.append(etaA)
    y.append(etaB)
    etaA = etaA + 0.02
# dump data to file nearby
  with open('../Plotting_python/data/chshetaAvsetaB.plot','wb') as fp:
    pickle.dump([x,y],fp)

if __name__=="__main__":
   __main__()
