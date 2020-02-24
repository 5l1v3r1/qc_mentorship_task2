
import numpy as np
import random

class ParameterOptimizer:
    """
    ParameterOptimizer class includes utitlies to perform Gradient Descent Optimization
    on the parameters of an input parametric pyquil executable
    """

    def __init__(self):
        """
        Starting value of the parameter that needs to be optimized is fixed at 0
        """
        
        self.theta = 0

    def cost_function(self, x00, x11, specialized_cost):
        """
        Calcuates cost of the parametric circuit for a given theta based on the probability
        of |11> and |00> measured in terms of bitstrings from sampled outputs

        Parameters:
        -----------

        x00              : Probability of the state |00>
        x11              : Probability of the state |11>
        specialized_cost : This flag determines whether the final state should be a|00> + b|11> and not
                           a|00> - b|11>. If True, a modified cost function is used that ensures that only
                           states of the form a|00> + b|11> are produced
        """

        if specialized_cost:
            return (x11 - 0.5)
        return (x00 - x11)**2

    def optimize_circuit_parameter(self, qc, executable, shots, specialized_cost, verbose = False):
        """
        Performs Gradient Descent Optimization to find the optimal parameter for a given pyquil executable

        Parameters:
        -----------

        qc               : A QuantumComputer that runs the pyquil executable
        executable       : A parameteric pyquil executable whose optimal parameter needs to be determined using 
                           Gradient Descent
        shots            : The number of trials for which the executable is run
        specialized_cost : This flag determines whether the final state should be a|00> + b|11> and not
                           a|00> - b|11>. If True, a modified cost function is used that ensures that only
                           states of the form a|00> + b|11> are produced
        verbose          : If True, prints the status of Gradient Descent at every 20 iterations
        """

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


