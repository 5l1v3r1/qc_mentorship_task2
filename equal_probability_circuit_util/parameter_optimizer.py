
import numpy as np
import random

class ParameterOptimizer():

    def __init__(self):
        self.theta = 0

    def cost_function(self, x00, x11, specialized_cost):
        if specialized_cost:
            return (x11 - 0.5)
        return (x00 - x11)**2

    def optimize_circuit_parameter(self, qc, executable, shots, specialized_cost, verbose = False):
        learning_rate = 0.1
        precision = 0
        previous_step_size = 1
        iteration = 0
        max_iterations = 1000
        while previous_step_size > precision and iteration < max_iterations:
            previous_theta = self.theta
            measurement_bitstrings = qc.run(executable, memory_map={'theta' : [self.theta]})
            sum_bitstrings = np.sum(measurement_bitstrings, axis=1)
            probability00 = list(sum_bitstrings).count(0) / shots
            probability11 = list(sum_bitstrings).count(2) / shots
            self.theta = self.theta - learning_rate*self.cost_function(probability00, probability11, specialized_cost)
            previous_step_size = abs(self.theta - previous_theta)
            iteration = iteration + 1
            factor = np.round(self.theta / np.pi, 2)
            if verbose and iteration % 20 == 0:
                print("Iteration", iteration, "\nProbability of |00> :", probability00, "\nProbability of |11> :", probability11, "\nCost Value:", self.cost_function(probability00, probability11, specialized_cost), "\nTheta Value:", factor, "pi")

        return factor, iteration


