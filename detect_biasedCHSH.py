from __future__ import print_function
from ncpol2sdpa import *
from inequalities import *
import pickle
# use inequalities from inequalities.py

def minmax_biased_chsh(P,p,q):
  Objective = biased_chsh(P,p,q) # set objective function
  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = [])
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="cvxopt")
  return {'c':p+q-p*q,'q':abs(sdpRelaxation.primal)}

def minmax_biased_chshA(P,p,q,chsh):
  Objective = biased_chshA(P,p,q) # set objective function
  Constraints = biased_chsh(P,p,q)
  ineq.append(Constraints - chsh)
  ineq.append(-1*Constraints + chsh)

  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(Objective)
  Min=sdpRelaxation.solve(solver="cvxopt")

  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  Max=sdpRelaxation.solve(solver="cvxopt")

  return {'min':Min,'max':Max}





  return {'c':p+q-p*q,'q':abs(sdpRelaxation.primal)}




def __main__():

  P = Probability([2, 2], [2, 2])

# set primary constraints here
  ineq = []
#  ineq.append(Constraints - 0.45)
#  ineq.append(-1*Constraints + 0.45)
# prepare relaxation

if __name__=="__main__":
   __main__()
  return {'c':p+q-p*q,'q':abs(sdpRelaxation.primal)}




def __main__():

  P = Probability([2, 2], [2, 2])

# set primary constraints here
  ineq = []
#  ineq.append(Constraints - 0.45)
#  ineq.append(-1*Constraints + 0.45)
# prepare relaxation

if __name__=="__main__":
   __main__()

  sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
  sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
  sdpRelaxation.set_objective(-Objective)
  sdpRelaxation.solve(solver="cvxopt")
  
  return {'c':p+q-p*q,'q':abs(sdpRelaxation.primal)}




def __main__():

  P = Probability([2, 2], [2, 2])

# set primary constraints here
  ineq = []
#  ineq.append(Constraints - 0.45)
#  ineq.append(-1*Constraints + 0.45)
# prepare relaxation

if __name__=="__main__":
   __main__()
