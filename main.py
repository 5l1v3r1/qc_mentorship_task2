
from equal_probability_circuit_util.equal_probability_circuit import EqualProbabilityCircuit
from equal_probability_circuit_util.parameter_optimizer import ParameterOptimizer

import numpy as np
import time

def find_equal_probability_circuit(shots, noisy_qvm, specialized_cost):
    """
    Finds the optimal parameter for a circuit that returns |00> and |11> with equal probabilities

    Parameters:
    -----------
    shots            : The number of trails for which the pyquil executable needs to be run using a QuantumComputer
    noisy_qvm        : This flag constructs a QuantumComputer with/without noise. If True, a QuantumComputer with a noise
                       model will be created
    specialized_cost : This flag determines whether the final state should be a|00> + b|11> and not
                       a|00> - b|11>. If True, a modified cost function is used that ensures that only
                       states of the form a|00> + b|11> are produced
    """

    epc = EqualProbabilityCircuit()
    parameter_optimizer = ParameterOptimizer()

    epc.set_number_of_shots(shots=shots)
    epc.use_noisy_qvm(noisy_qvm=noisy_qvm)
    parameteric_program = epc.get_parameteric_circuit()
    qc, circuit_executable, shots = epc.get_circuit_executable(parameteric_program=parameteric_program)
    factor, iterations = parameter_optimizer.optimize_circuit_parameter(qc, circuit_executable, shots, specialized_cost=specialized_cost)
    state, state_probabilities = epc.verify_final_circuit(factor * np.pi)

    return factor, state, state_probabilities, iterations

def generate_circuit_results(specialized_cost):
    """
    Generates Gradient Descent comparison results for limited number of shots per iteration and noise

    Parameters:
    -----------
    specialized_cost : This flag determines whether the final state should be a|00> + b|11> and not
                       a|00> - b|11>. If True, a modified cost function is used that ensures that only
                       states of the form a|00> + b|11> are produced
    """

    shots = 1
    noisy_qvm = False
    print('\n{:<8} {:<13} {:<15} {:<20} {:<20} {:<12} {:<6} {:<15}'.format("Shots", "Noisy QVM", "Parameter", "Probability |00>", "Probability |11>","Iterations", "Time", "State"))
    while shots <= 1000:
        for i in range(0,2):
            start_time = time.time()
            factor, state, state_probabilities, iterations = find_equal_probability_circuit(shots=shots, noisy_qvm=noisy_qvm, specialized_cost=specialized_cost)
            end_time = time.time()
            program_run_time = end_time - start_time
            print('{:<8} {:<13} {:<15} {:<20} {:<20} {:<12} {:<6} {:<15}'.format(shots, str(noisy_qvm), str(factor)+"*pi", str(round(float(state_probabilities['00']), 2)), str(round(float(state_probabilities['11']), 2)), iterations, str(round(program_run_time))+"s", str(state)))
            noisy_qvm = not noisy_qvm
        shots = shots * 10



if __name__ == "__main__":
    print("\nGenerating Circuit Results with General Cost Function --->")
    generate_circuit_results(specialized_cost = False)
    
    print("\nGenerating Circuit Results with Specialized Cost Function --->")
    generate_circuit_results(specialized_cost = True)