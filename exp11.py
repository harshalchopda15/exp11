# Quantum Algorithm and Computational Methods
# Program: Deutsch-Jozsa Algorithm (n=3) for a balanced oracle (parity f(x)=x0⊕x1⊕x2)

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from IPython.display import display

def deutsch_jozsa_parity(n=3, shots=1024):
    """
    Implements Deutsch-Jozsa algorithm for n input qubits and a parity oracle:
    f(x) = x0 XOR x1 XOR ... XOR x_{n-1} (balanced)
    """
    # total qubits = n input + 1 ancilla
    qc = QuantumCircuit(n + 1, n)  # last qubit is ancilla; classical reg for n input qubits

    # 1) Initialize ancilla to |1>
    qc.x(n)        # ancilla index = n
    # 2) Apply Hadamard to all qubits (inputs + ancilla)
    qc.h(range(n + 1))

    # --- Oracle for parity: flip ancilla if parity of inputs is 1 ---
    # This is achieved by CNOT from each input qubit to the ancilla.
    for i in range(n):
        qc.cx(i, n)

    # --- End oracle ---

    # 3) Apply Hadamard on input qubits only
    qc.h(range(n))

    # 4) Measure input qubits (ignore ancilla)
    qc.measure(range(n), range(n))

    # Simulate
    sim = AerSimulator()
    job = sim.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Display circuit and results
    print("Deutsch–Jozsa circuit (parity oracle) — n =", n)
    display(qc.draw('mpl'))
    print("\nMeasurement counts (input qubits):")
    display(plot_histogram(counts))

    return counts

# Run the algorithm for n=3
counts = deutsch_jozsa_parity(n=3, shots=1024)