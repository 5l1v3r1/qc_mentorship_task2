import numpy as np

class ParameterOptimizer():

    def __init__(self):
        self.theta = 0

    def cost_function(self, x):
        return x - 0.5

    def optimize_circuit_parameter(self, qc, executable, shots, verbose = False):
        learning_rate = 0.1
        precision = 0
        previous_step_size = 1
        iteration = 0
        max_iterations = 1000
        while previous_step_size > precision and iteration < max_iterations:
            previous_theta = self.theta
            measurement_bitstrings = qc.run(executable, memory_map={'theta' : [self.theta]})
            sum_bitstrings = np.sum(measurement_bitstrings, axis=1)
            probability = np.count_nonzero(sum_bitstrings) / shots
            self.theta = self.theta - learning_rate*self.cost_function(probability)
            previous_step_size = abs(self.theta - previous_theta)
            iteration = iteration + 1
            factor = np.round(self.theta / np.pi, 2)
            if verbose and iteration % 20 == 0:
                print("Iteration", iteration, "\nProbability of |00> :", (1 - probability), "\nProbability of |11> :", probability, "\nCost Value:", self.cost_function(probability), "\nTheta Value:", factor, "pi")

        return factor, iteration


