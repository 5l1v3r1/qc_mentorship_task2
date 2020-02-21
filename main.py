
from equal_probability_circuit.equal_probability_circuit import EqualProbabilityCircuit
from equal_probability_circuit.parameter_optimizer import ParameterOptimizer

import numpy as np

def find_equal_probability_circuit():
    epc = EqualProbabilityCircuit(shots=1000)
    parameter_optimizer = ParameterOptimizer()

    parameteric_program = epc.get_parameteric_circuit()
    qc, circuit_executable, shots = epc.get_circuit_executable(parameteric_program=parameteric_program)
    factor, iterations = parameter_optimizer.optimize_circuit_parameter(qc, circuit_executable, shots)

    state, state_probabilities = epc.verify_final_circuit(factor * np.pi)
    print(factor, state, state_probabilities, iterations)

if __name__ == "__main__":
    find_equal_probability_circuit()
