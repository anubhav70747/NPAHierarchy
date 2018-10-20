from __future__ import print_function
from ncpol2sdpa import *
import pickle

def chsh2_AB(P,etaA,etaB):
  chsh2 = 0
  for ai1 in range(2):
    for ai2 in range(2):
      ai = 2 * ai1 + ai2
      for bi1 in range(2):
        for bi2 in range(2):
          bi = 2 * bi1 + bi2
          for ao1 in range(2):
            for ao2 in range(2):
              ao = 2 * ao1 + ao2
              for bo1 in range(2):
                for bo2 in range(2):
                  bo = 2 * bo1 + bo2
                  if  ( ai1 * bi1 == ao1 ^ bo1 ) and ( ai2 * bi2 == ao2 ^ bo2 ):
                    chsh2 = chsh2 + P([ao,bo],[ai,bi],['A','B'])


  chsh2_mod=chsh2 * etaA * etaB + (4 * P([0],[0],['B']) + 2 * P([0],[1],['B']) + 2 * P([1],[1],['B']) + 2 * P([0],[2],['B']) + 2 * P([2],[2],['B']) + 1) * (1 - etaA) * etaB + (4 * P([0],[0],['A']) + 2 * P([0],[1],['A']) + 2 * P([1],[1],['A']) + 2 * P([0],[2],['A']) + 2 * P([2],[2],['A']) + 1) * etaA * (1 - etaB) + 9 * (1 - etaA) * (1 - etaB)
  return chsh2_mod/ 16

def __main__():
  x=[]
  y=[]
  etaA=0.653
  etaA_lim=1.02
  print(etaA_lim)
  while etaA < etaA_lim:
    P = Probability([4,4,4,4],[4,4,4,4])
    etaB = 0.38
    loop_control = 0
    while loop_control <=0.625:
      etaB = etaB + 0.002
      Objective = chsh2_AB(P,etaA,etaB) # set objective function
#  Constraints = P([0],[0],['A']) # set primary constraint inequality
# set primary constraints here
      ineq = []
#  ineq.append(Constraints - 0.45)
#  ineq.append(-1*Constraints + 0.45)
# prepare relaxation
      sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
      sdpRelaxation.get_relaxation(1, substitutions = P.substitutions,momentinequalities = ineq)
      sdpRelaxation.set_objective(-Objective)
      sdpRelaxation.solve(solver="cvxopt")
      loop_control = abs(sdpRelaxation.primal)
      print(etaA,etaB,'------>',loop_control)
# collect data points
    print(etaA,'----critical---->',etaB)
    x.append(etaA)
    y.append(etaB)
    etaA = etaA + 0.02
# dump data to file nearby
  with open('../Plotting_Python/data/chsh2etaAvsetaB.plot','wb') as fp:
    pickle.dump([x,y],fp)
if __name__=="__main__":
   __main__()
