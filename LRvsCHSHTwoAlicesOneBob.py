from __future__ import print_function
from ncpol2sdpa import *
import pickle
# just a basic code to run tri vs bi (or reverse) party NPA optimization
# use inequalities from inequalities.py

def chsh_AB(P):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
          if  x * y == u ^ v:
            chsh=chsh+P([u,v],[x,y],['A','B'])
  return chsh/4

def chsh_aB(P):
  chsh=0
  for x in range(2):
    for y in range(2):
      for u in range(2):
        for v in range(2):
          if  x * y == u ^ v:
            chsh=chsh+P([u,v],[x+2,y],['A','B'])
  return chsh/4

def local_R(P):
    sum = 0
    for x in range(2):
        sum = sum + P([0],[x+2],['A'])
    return sum/2

def __main__():

  #Objective = chsh_aB(P) # set objective function
  
  for count in range(101):
    P = Probability([2, 2, 2, 2], [2, 2])
  
    Objective = local_R(P) # set objective function
  
    C1 = chsh_AB(P) # set primary constraint inequality
  #C2 = local_R(P) # set primary constraint inequality
    C2 = chsh_aB(P)
  # set primary constraints here
    ineq = []
    ineq.append(C1 - 0.5*(1+1/2**.5))
    ineq.append(-1*C1 + 0.5*(1+1/2**.5))
    chsh_aB_val = 0.5 + count/(100*2*2**0.5)
    ineq.append(C2 - chsh_aB_val)
    #ineq.append(-1*C2 + chsh_aB_val)
    # prepare relaxation
    sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
    sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
    sdpRelaxation.set_objective(-Objective)
    sdpRelaxation.solve(solver="mosek")
    # collect data points
    
    print(chsh_aB_val,',',abs(sdpRelaxation.primal))

if __name__=="__main__":
   __main__()
