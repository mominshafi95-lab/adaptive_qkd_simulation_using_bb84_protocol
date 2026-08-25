"""Cross-version Aer imports.

Qiskit exposes Aer either under the `qiskit_aer` top-level package or as
`qiskit.providers.aer` depending on installation/version. Try the preferred
`qiskit_aer` imports first and fall back to the older path.
"""
try:
    from qiskit_aer.noise import NoiseModel, depolarizing_error
    from qiskit_aer import AerSimulator
except Exception as e:
    from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
    from qiskit.providers.aer import AerSimulator

from qiskit import transpile
from qiskit_aer import AerSimulator

def apply_noise_model(circuit, probability):

    if probability == 0:
        return circuit

    noise_model = NoiseModel()
    error = depolarizing_error(probability, 1)
    noise_model.add_all_qubit_quantum_error(error, ['x', 'h'])

    simulator = AerSimulator(noise_model=noise_model)
    transpiled = transpile(circuit, simulator)

    return transpiled
