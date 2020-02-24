from pyquil import Program, get_qc
from pyquil.gates import RX, RY, CNOT, MEASURE
from pyquil.api import WavefunctionSimulator

class EqualProbabilityCircuit:
    """
    EqualProbabilityCircuit class includes utilities to construct a circuit that returns |00> and |11> with equal
    probability. It creates a parameteric circuit which is compiled to a pyquil executable where the optimal parameter 
    theta needs to be determined using Gradient Descent
    """
    
    def __init__(self):
        self.qc = None
        self.shots = None
        self.executable = None

    def set_number_of_shots(self, shots):
        """
        Sets the number of trails for which the pyquil executable needs to be run using a QuantumComputer

        Parameters:
        -----------
        shots : The number of trails for which the pyquil executable needs to be run using a QuantumComputer
        """

        self.shots = shots

    def use_noisy_qvm(self, noisy_qvm = False):
        """
        Initializes a QuantumComputer with 2 qubits with/without noise

        Parameters:
        -----------
        noisy_qvm : This flag constructs a QuantumComputer with/without noise. If True, a QuantumComputer with a noise
                    model will be created
        """

        self.qc = get_qc("2q-qvm", as_qvm = True, noisy = noisy_qvm)

    def get_parameteric_circuit(self, theta = None, verify = False):        
        """
        Constructs a parameterized circuit that returns |00> and |11> with equal probability where the optimal parameter theta
        needs to be determined using Gradient Descent
        This function is also used to return a circuit for a given value of theta in order to verify the final wavefunction

        Parameters:
        -----------
        theta  : Value of the parameter for which a circuit is returned to verify the final wavefunction
        verify : If True, returns a circuit for the given value of theta
        """

        parameteric_program = Program()

        if theta is None and not verify:
            theta = parameteric_program.declare("theta", memory_type = "REAL")
        
        parameteric_program.inst(RY(theta, 0))
        parameteric_program.inst(CNOT(0, 1))

        if theta is None and not verify:
            ro = parameteric_program.declare("ro", memory_type = "BIT", memory_size = 2)
            parameteric_program.inst(MEASURE(0, ro[0]))
            parameteric_program.inst(MEASURE(1, ro[1]))
            parameteric_program.wrap_in_numshots_loop(shots=self.shots)

        return parameteric_program

    def get_circuit_executable(self, parameteric_program):   
        """
        Returns a pyquil executable obtained after compiling the given parameteric program

        Parameters:
        -----------
        parameteric_program  : The parameteric program whose pyquil executable is returned
        """

        self.executable = self.qc.compile(parameteric_program)
        return self.qc, self.executable, self.shots

    def verify_final_circuit(self, theta):   
        """
        Returns a wavefunction and state probabilities of equal probability circuit for given theta

        Parameters:
        -----------
        theta  : Value of the parameter for which a wavefunction and state probabilities are returned to verify 
                 the final wavefunction
        """

        wf = WavefunctionSimulator()
        final_circuit = self.get_parameteric_circuit(theta=theta, verify = True)
        state = wf.wavefunction(final_circuit)
        state_probabilities = state.get_outcome_probs()
        return state, state_probabilities
