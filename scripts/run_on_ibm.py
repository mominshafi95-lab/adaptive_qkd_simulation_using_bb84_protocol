"""Example script to authenticate and list IBM Quantum backends.

This script will only list backends by default. To attempt a test run,
use the `--run-test` flag (requires qiskit and a valid token).

Set your IBM token in the environment variable `IBM_QUANTUM_TOKEN`.
"""
import sys
from pathlib import Path

# Ensure project root is importable
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import argparse
from utils.ibm_backend import IBMBackendManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', action='store_true', default=True, help='List available backends')
    parser.add_argument('--run-test', action='store_true', help='Attempt a small test circuit run (requires qiskit)')
    parser.add_argument('--backend', type=str, help='Backend name to use for test run')
    args = parser.parse_args()

    mgr = IBMBackendManager()
    try:
        provider = mgr.authenticate()
    except Exception as e:
        print('Authentication failed:', e)
        print('\nSet IBM_QUANTUM_TOKEN environment variable or pass token to authenticate() in code.')
        return

    if args.list:
        try:
            backends = mgr.list_backends(provider)
            print('Available backends:')
            for b in backends:
                print(' -', b)
        except Exception as e:
            print('Failed to list backends:', e)

    if args.run_test:
        try:
            # Lazy import qiskit to build a simple circuit
            from qiskit import QuantumCircuit
            from qiskit import transpile
            q = QuantumCircuit(1, 1)
            q.h(0)
            q.measure(0, 0)

            backend_name = args.backend or (mgr.list_backends(provider)[0] if mgr.list_backends(provider) else None)
            if not backend_name:
                print('No backend selected or available to run test')
                return

            print(f'Attempting test run on backend: {backend_name} (this may take time)')
            result = mgr.run_circuit(provider, backend_name, q, shots=1024)
            print('Result:', result.get_counts() if hasattr(result, 'get_counts') else result)
        except Exception as e:
            print('Test run failed:', e)


if __name__ == '__main__':
    main()
