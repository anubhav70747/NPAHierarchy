from __future__ import print_function
from ncpol2sdpa import *
import pickle
from itertools import product

# Generalized function for parallel repetition of the CHSH inequality
def chsh_n_ABS(P, n):
    chshn = 0
    N = 2 ** n  # Number of possible inputs/outputs per party

    # Generate all possible inputs and outputs for Alice and Bob
    inputs_A = range(N)
    inputs_B = range(N)
    outputs_A = range(N)
    outputs_B = range(N)

    # Iterate over all possible combinations
    for x_value in inputs_A:
        for y_value in inputs_B:
            for u_value in outputs_A:
                for v_value in outputs_B:
                    # Convert integer inputs/outputs to bit lists
                    x_bits = [(x_value >> i) & 1 for i in reversed(range(n))]
                    y_bits = [(y_value >> i) & 1 for i in reversed(range(n))]
                    u_bits = [(u_value >> i) & 1 for i in reversed(range(n))]
                    v_bits = [(v_value >> i) & 1 for i in reversed(range(n))]

                    # Check the winning condition for all bits
                    if all((x_i * y_i) == (u_i ^ v_i) for x_i, y_i, u_i, v_i in zip(x_bits, y_bits, u_bits, v_bits)):
                        # Accumulate the probability
                        chshn += P([u_value, v_value], [x_value, y_value], ['A', 'B'])

    # Normalize the accumulated value
    total_input_pairs = N * N  # Total number of input pairs (x, y)
    return chshn / total_input_pairs

def __main__():
    n = 3  # Set the value of n here (can be any positive integer)
    N = 2 ** n  # Number of possible inputs/outputs per party

    # Generalize the Probability function call for arbitrary n
    P = Probability([N] * N, [N] * N)

    # Define the objective function (can be customized as needed)
    # For example, summing over specific probabilities
    Objective = sum(P([0], [x], ['A']) for x in range(N))

    # Set primary constraint inequality
    Constraints = chsh_n_ABS(P, n)  # Compute the CHSH value for n repetitions

    # Set primary constraints here
    ineq = []
    # The bound value may need to be adjusted depending on n
    # For demonstration, we'll use 0.728553390 as in the original code
    # You can adjust this value based on theoretical bounds for n
    bound_value = 0.728553390
    ineq.append(Constraints - bound_value)
    ineq.append(-Constraints + bound_value)

    # Prepare the SDP relaxation
    sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
    sdpRelaxation.get_relaxation(
        level=1,
        substitutions=P.substitutions,
        momentinequalities=ineq
    )
    sdpRelaxation.set_objective(-Objective)
    sdpRelaxation.solve(solver="mosek")

    # Collect data points
    print("Primal objective value:", abs(sdpRelaxation.primal))
    print("Dual objective value:", abs(sdpRelaxation.dual))

if __name__ == "__main__":
    __main__()
