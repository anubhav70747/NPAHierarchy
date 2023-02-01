from __future__ import print_function
from ncpol2sdpa import *
import pickle
# evaluate the maximum success probability of entanglement assisted classical communication protocols for generalized RAC 

def rac(P,z):
  Pwin = 0
  for x0 in range(2):
    for x1 in range(2):
      for x2 in range(2):
          for a in range(2):      
            if z[0] == 1:
              Pwin = Pwin + P([a,a ^ x0],[4*x2 + 2*x1 + x0, 0],['A','B'])
            if z[1] == 1:
              Pwin = Pwin + P([a,a ^ x1],[4*x2 + 2*x1 + x0, 1],['A','B'])
            if z[2] == 1:
              Pwin = Pwin + P([a,a ^ x2],[4*x2 + 2*x1 + x0, 2],['A','B'])
            if z[3] == 1:
              Pwin = Pwin + P([a,a ^ x0 ^ x1],[4*x2 + 2*x1 + x0, 3],['A','B'])
            if z[4] == 1:
              Pwin = Pwin + P([a,a ^ x0 ^ x2],[4*x2 + 2*x1 + x0, 4],['A','B'])
            if z[5] == 1:
              Pwin = Pwin + P([a,a ^ x1 ^ x2],[4*x2 + 2*x1 + x0, 5],['A','B'])
            if z[6] == 1:
              Pwin = Pwin + P([a,a ^ x0 ^ x1 ^ x2],[4*x2 + 2*x1 + x0, 6],['A','B'])
  return Pwin/(8*sum(z))
def __main__():

  P = Probability([2,2,2,2,2,2,2,2], [2,2,2,2,2,2,2])
  
# prepare relaxation
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(1, substitutions = P.substitutions)
  # collect data points
  flag = 0 
  total_cases = 0
  for a0 in range(2):
    for a1 in range(2):
      for a2 in range(2):
        for a3 in range(2):
          for a4 in range(2):
            for a5 in range(2):
              for a6 in range(2):
                z = [a0,a1,a2,a3,a4,a5,a6]
                if sum(z) > 1:
                  total_cases = total_cases + 1
                  Objective = rac(P,z) # set objective function
                  sdpRelaxation.set_objective(-Objective)
                  sdpRelaxation.solve(solver="mosek")
                  LowerBound = 0.5*(1+1/(sum(z)**0.5))
                  print('case z =',z,'bound =',abs(sdpRelaxation.primal))
                  if abs(abs(sdpRelaxation.primal)-LowerBound) >= 0.0000001 :
                    print('Oops, the bounds don''t match for',z)
                    flag = 1
  if flag == 0 :
    print('checked',total_cases,'cases, and everything went smooth :-)')

if __name__=="__main__":
   __main__()
