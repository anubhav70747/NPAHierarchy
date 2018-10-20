from __future__ import print_function
from ncpol2sdpa import *
from inequalities import *
import sys
import pickle
import matplotlib.pyplot as plt

def I3322(P):
  sum = 0
  sum = sum - P([0],[0],'B') - 2*P([0],[0],'A') - P([0],[1],'A') + P([0,0],[0,0],['A','B']) + P([0,0],[1,0],['A','B']) + P([0,0],[2,0],['A','B']) + P([0,0],[0,1],['A','B']) + P([0,0],[1,1],['A','B']) - P([0,0],[2,1],['A','B']) + P([0,0],[0,2],    ['A','B']) - P([0,0],[1,2],['A','B'])
  return sum

def I3322AB(P):
  sum = 0.5*(P([0],[0],'B') + 2*P([0],[0],'A') + P([0],[1],'A'))
  return sum

def I3322AB2(P):
  sum = (0.5*P([0],[1],'A')-0.5*P([0],[1],'B'))
  return sum
def I3322AB3(P):
  sum = (10+P([0],[0],'A')-P([0],[0],'B')-P([0],[2],'A')+P([0],[2],'B'))/18.0
  return sum
def __main__():
    x=[]
    y=[]
    P = Probability([2, 2, 2], [2, 2, 2])
    Objective = I3322AB3(P) # set objective function
 #   Objective = I3322(P) # set objective function
    for i in range(26):
        I1 = [[ 0, -1.0,  0,  0],
              [-2.0,  1.0,  1.0,  1.0],
              [-1.0,  1.0,  1.0, -1.0],
              [ 0,  1.0, -1.0,  0]]

        I2 = [[ 0, -2.0, -1.0,  0],
              [-1.0,  1.0,  1.0,  1.0],
              [ 0,  1.0,  1.0, -1.0],
              [ 0,  1.0, -1.0,  0]]
        Constraints = I3322(P)
        #Constraints = -1*define_objective_with_I(I2,P)
# set primary constraints here
        ineq = []
     #   ineq.append(-1*Constraints + 0.2508)
     #   ineq.append(Constraints - (0.2508))
        ineq.append(-1*Constraints + i*0.01)
        ineq.append(Constraints - (i*0.01))
# prepare relaxation
        sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
        sdpRelaxation.get_relaxation(3, substitutions = P.substitutions,         momentinequalities = ineq)
        sdpRelaxation.set_objective(-Objective)
        sdpRelaxation.solve(solver="cvxopt")
        x.append(((i*0.01)+6)/9.0)
        y.append(abs(sdpRelaxation.primal))
        print(((i*0.01)+6)/9.0,abs(sdpRelaxation.primal))
# set primary constraints here
    ineq = []
    ineq.append(-1*Constraints + 0.2508)
    ineq.append(Constraints - (0.2508))
# prepare relaxation
    sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
    sdpRelaxation.get_relaxation(3, substitutions = P.substitutions,         momentinequalities = ineq)
    sdpRelaxation.set_objective(-Objective)
    sdpRelaxation.solve(solver="cvxopt")
    x.append((0.2508+6)/9.0)
    y.append(abs(sdpRelaxation.primal))
    print((0.25087+6)/9.0,abs(sdpRelaxation.primal))
    plt.plot(x,y,markersize=10,marker='o')
    plt.xlim(0.666,0.7)
    plt.ylim(0.54,0.67)
    plt.ylabel('Object',size=16)
    plt.xlabel('I3322',size=16)
    plt.grid()
    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=14)
    plt.savefig('../../../niko.pdf',bbox_inches='tight')
    plt.show()

if __name__=="__main__":
   __main__()
