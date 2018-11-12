from __future__ import print_function
from ncpol2sdpa import *
from inequalities import *
import pickle
# use inequalities from inequalities.py

def minmax_biased_chsh(P,level,p,q):
  Objective = biased_chsh(P,p,q) # set objective function
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(level, substitutions = P.substitutions,momentinequalities = [])
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="cvxopt")
  return {'c':p+q-p*q,'q':abs(sdpRelaxation.primal)}

def minmax_biased_chshA(P,level,p,q,chsh):
  Objective = biased_chshA(P,p,q) # set objective function

  ineq=[]

  Constraints = biased_chsh(P,p,q)
  ineq.append(Constraints - chsh)
  ineq.append(-1*Constraints + chsh)

  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(level, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(Objective)
  sdpRelaxation.solve(solver="cvxopt")
  Min = abs(sdpRelaxation.primal)

  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(level, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="cvxopt")
  Max = abs(sdpRelaxation.primal)

  return {'min':Min,'max':Max}

def max_biased_chshB(P,level,p,q,chsh,chshA):
  Objective = biased_chshB(P,p,q) # set objective function

  ineq=[]

  Constraints1 = biased_chsh(P,p,q)
  ineq.append(Constraints1 - chsh)
  ineq.append(-1*Constraints1 + chsh)

  Constraints2 = biased_chshA(P,p,q)
  ineq.append(Constraints2 - chshA)
  ineq.append(-1*Constraints2 + chshA)

  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(level, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="cvxopt")
  Max = abs(sdpRelaxation.primal)

  return Max



def __main__():
  P = Probability([2, 2], [2, 2])
  p=0.5
  q=0.5
  print(minmax_biased_chsh(P,2,p,q))
  print(minmax_biased_chshA(P,2,p,q,0.75))
  print(max_biased_chshB(P,2,p,q,0.5,0.5))
if __name__=="__main__":
   __main__()

