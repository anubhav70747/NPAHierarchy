from __future__ import print_function
from ncpol2sdpa import *
import pickle
# for evaluating CHSH between second Alice and Bob with inefficient detectors and assignment strategy given the CHSH between first Alice and Bob

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

def chsh_aB(P,etaA,etaB):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
          if  x * y == u ^ v:
            chsh=chsh+P([u,v],[x+2,y],['A','B'])
  chsh_mod=(chsh)*etaA*etaB + (2*P([0],[2],['A'])+1)*etaA*(1-etaB) + (2*P([0],[0],['B'])+1)*etaB*(1-etaA) + 3*(1-etaA)*(1-etaB)
  return chsh_mod/4

def local_R(P):
    sum = 0
    for x in range(2):
        sum = sum + P([0],[x+2],['A'])
    return sum/2

def __main__():
  x = []
  y = []
  for i in range(101):
  #Objective = chsh_aB(P) # set objective function
    etaa = i/100
    P = Probability([2, 2, 2, 2], [2, 2])
 #Objective = local_R(P) # set objective function
    Objective = chsh_aB(P,etaa,1)
    C1 = chsh_AB(P,1,1) # set primary constraint inequality
 #C2 = local_R(P) # set primary constraint inequality
 #C2 = chsh_aB(P)
 # set primary constraints here
    ineq = []
    ineq.append(C1 - 0.5*(1+1/2**.5))
    ineq.append(-1*C1 + 0.5*(1+1/2**.5))
 #chsh_aB_val = 0.5 + count/(100*2*2**0.5)
 #ineq.append(C2 - chsh_aB_val)
 #ineq.append(-1*C2 + chsh_aB_val)
 # prepare relaxation
    sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
    sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
    sdpRelaxation.set_objective(-Objective)
    sdpRelaxation.solve(solver="mosek")
# collect data points    
    print(etaa,',',abs(sdpRelaxation.primal))
    x.append(etaa)
    y.append(abs(sdpRelaxation.primal))

  for i in x:
    print(i,',',)

  for j in y:
    print(j,',',)

if __name__=="__main__":
   __main__()
