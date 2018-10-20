from __future__ import print_function
import matplotlib.pyplot as plt
from inequalities import *
from ncpol2sdpa import *
from itertools import cycle
lines = ["-","--","-.",":"]
linecycler = cycle(lines)
# for plotting chsh_AB vs. chsh_BC given a fixed value of svetlichny game

def __main__():
  P = Probability([2, 2], [2, 2], [2, 2])
  Objective = chsh_BC(P) # set objective function
  Constraints1 = svetlichny_game(P) # set primary constraint inequality
  Constraints2 = chsh_AB(P)

# define outer loop parameters
  dx = 0.675 # set initialization for primary constraint
  step = 0.025 # incremental value for primary constraint
  lim = 0.85354 # upper bound to the primary constraint
  x=[]
  flag2=0 # you know what flags are all about?

# outer loop begins
  while dx  <= lim :
    print("dx=",dx)

# define outer loop parameters
    dy = 0.5 # set initialization for second constraint
    div = 1.0 # normalization factor for objective
    step_y = 0.005 # incremental value for second constraint
    lim_y = 0.85354 # upper bound to the second constraint
    y = []
    z = []
    flag=0 # variable to ensure precision
# inner loop begins
    while dy <= lim_y :
      print(dy)

# prepare relaxation
# set primary constraints here
      ineq = []
      ineq.append(Constraints1 - dx)
      ineq.append(-1*Constraints1 + dx)

# set second set of constraints here
      ineq.append(Constraints2 - dy)
      ineq.append(-1*Constraints2 + dy)

# start relaxation
      sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
      sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,momentinequalities = ineq)
      sdpRelaxation.set_objective(-Objective)

# check for good solution, if not next loop
      try:
        sdpRelaxation.solve(solver="cvxopt")
      except Exception:
        if flag==0:
          flag=1
          dy=dy-step_y
          step_y=0.00005
          dy=dy+step_y
          continue;
        else:
          break;

# collect data points
      y.append(dy)
      z.append(abs(sdpRelaxation.primal)/div)
      print(abs(sdpRelaxation.primal)/div)
      dy = dy + step_y
      if dy>=lim_y and flag==0:
        print('fuckMyLife')
        dy=dy-step_y
        step_y=0.00005
        dy=dy+step_y
        flag=1
# plot results
    x.append(dx)
    if dx==lim:
      plt.plot(y,z,marker='o',ms=4,mew=4)
    else:
      plt.plot(y,z,linewidth=4.0,ls=next(linecycler))
    dx = dx + step
    if dx>lim and flag2==0:
      dx=lim
      flag2=1
# the loop must be kept straight.

# ask pyplot to use latex
  plt.rc('text', usetex=True)

# create list of lengends, awww yeah
  list_of_labels=['$p(S_3)=$'+str(i) for i in x]

# display/save the graph
  plt.xlim(0.5,1.09)
  plt.ylim(0.5,1.09)
  plt.ylabel('$\max_{Q}\{p_{A_1A_3}(S_2)\}$',size=16)
  plt.xlabel('$p_{A_1A_2}(S_2)$',size=16)
  plt.legend((list_of_labels))
  plt.grid()
  plt.tick_params(axis='x', labelsize=14)
  plt.tick_params(axis='y', labelsize=14)

  plt.savefig('../../../graphs/chsh_chsh_snQ.pdf',bbox_inches='tight')
  plt.show()
if __name__=="__main__":
   __main__()
