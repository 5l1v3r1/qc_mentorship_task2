# QC Mentorship Problem 2 
### Problem Statement:
To find a circuit that returns `|00>` and `|11>` with equal probability where the circuit is parameterized, contains only `RX`, `RY` and `CNOT` gates and all parameters are determined using Gradient Descent

### Approach to Solution:
The `RX`, `RY` and `CNOT` gates are defined as follows:

![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20RX%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Ccos%28%5CPhi%20/2%29%20%26%20-i%5Csin%28%5CPhi%20/2%29%20%5C%5C%20-i%5Csin%28%5CPhi%20/2%29%20%26%20%5Ccos%28%5CPhi%20/2%29%20%5C%5C%20%5Cend%7Bbmatrix%7D%20RY%20%3D%20%5Cbegin%7Bbmatrix%7D%20%5Ccos%28%5CPhi%20/2%29%20%26%20-%5Csin%28%5CPhi%20/2%29%20%5C%5C%20%5Csin%28%5CPhi%20/2%29%20%26%20%5Ccos%28%5CPhi%20/2%29%20%5C%5C%20%5Cend%7Bbmatrix%7D)

![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20%5Csmall%20CNOT%20%3D%20%5Cbegin%7Bbmatrix%7D%201%20%26%200%20%26%200%20%26%200%5C%5C%200%20%26%201%20%26%200%20%26%200%5C%5C%200%20%26%200%20%26%200%20%26%201%5C%5C%200%20%26%200%20%26%201%20%26%200%20%5Cend%7Bbmatrix%7D)

We consider two qubits `q0` and `q1` both intialized to `|0>`. A circuit that returns a state of the form `a|00> + b|11>` can be constructed by applying an `RX` gate to qubit `q0` and then applying a `CNOT` gate with `q0` as control and `q1` as target. The amplitudes `a` and `b` depend on the angle, `theta` of the `RX` rotation. For `theta = n*pi/2` where `n` is any positive or negative integer, this produces a circuit that returns `|00>` and `|11>` with equal probability, i.e., `1/2`. However, it adds a phase of `-i` to `|11>`. For the given problem, we use `RY` gate instead of `RX` to perform the rotation. From the gate definition given above, applying `RY` and then `CNOT` also produces a state of the form `a|00> + b|11>` without an additional complex phase. 

For determining the parameter using gradient descent, we start with the parameter initialized to `0` and use a cost function of the form `(prob00 - prob11)^2` where `prob00` and `prob11` are probabilities of the states `|00>` and `|11>` respectively when the circuit is run for given number of trials. The cost function encodes the condition that the probabilities of `|00>` and `|11>` must be equal which is the objective of the given problem.

### Code Structure:
The code in this repository is structured as follows:
1. `equal_probability_circuit_util/equal_probability_circuit.py` : Includes utilities for constructing a circuit that returns `|00>` and `|11>` with equal probabilities using the appraoch described above, running the circuit for a limited number of trials and verifying the final state produced using the parameter determined from gradient descent
2. `equal_probability_circuit_util/parameter_optimizer.py` : Includes utilities for performing gradient descent to determine the parameter for equal probability circuit and a cost function that measures the performance
3. `main.py` : Generates a comparison of results produced by applying gradient descent for the parameter of the equal probability circuit

### Bonus Question:
To ensure that our circuit returns only states of the form `a|00> + b|11>` and not `a|00> - b|11>` we use a different cost function `prob11 - 0.5` where `prob11` is the probability of the state `|11>`. This cost function encodes the condition that the probability of the state `|11>` must be `1/2` for it to be equal to the probability of `|00>` and vice versa.





