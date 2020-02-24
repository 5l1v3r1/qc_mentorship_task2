from pyquil import Program, get_qc
from pyquil.gates import RX, RY, CNOT, MEASURE
from pyquil.api import WavefunctionSimulator

class EqualProbabilityCircuit():
    
    def __init__(self):
        self.qc = None
        self.shots = None
        self.executable = None

    def set_number_of_shots(self, shots):
        self.shots = shots

    def use_noisy_qvm(self, noisy_qvm = False):
        self.qc = get_qc("2q-qvm", as_qvm = True, noisy = noisy_qvm)

    def get_parameteric_circuit(self, theta = None, verify = False):
        parameteric_program = Program()

        if theta is None:
            theta = parameteric_program.declare("theta", memory_type = "REAL")
        
        parameteric_program.inst(RY(theta, 0))
        parameteric_program.inst(CNOT(0, 1))

        if not verify:
            ro = parameteric_program.declare("ro", memory_type = "BIT", memory_size = 2)
            parameteric_program.inst(MEASURE(0, ro[0]))
            parameteric_program.inst(MEASURE(1, ro[1]))
            parameteric_program.wrap_in_numshots_loop(shots=self.shots)

        return parameteric_program

    def get_circuit_executable(self, parameteric_program):
        self.executable = self.qc.compile(parameteric_program)
        return self.qc, self.executable, self.shots

    def verify_final_circuit(self, theta):
        wf = WavefunctionSimulator()
        final_circuit = self.get_parameteric_circuit(theta=theta, verify = True)
        state = wf.wavefunction(final_circuit)
        state_probabilities = state.get_outcome_probs()
        return state, state_probabilities
