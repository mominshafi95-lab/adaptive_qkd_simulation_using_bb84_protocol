"""Helpers to authenticate and interact with IBM Quantum backends.

This module performs lazy imports to avoid forcing users to install
`qiskit-ibm-runtime` unless they plan to use real hardware.

Usage:
  from utils.ibm_backend import IBMBackendManager
  mgr = IBMBackendManager()
  provider = mgr.authenticate(token=os.environ.get('IBM_QUANTUM_TOKEN'))
  backends = mgr.list_backends(provider)

Note: Users must provide their IBM token via the environment variable
`IBM_QUANTUM_TOKEN` or pass it to `authenticate()`.
"""
from typing import Optional, List
import os


class IBMBackendManager:
    """Simple wrapper around qiskit-ibm-runtime provider operations."""

    def authenticate(self, token: Optional[str] = None, url: Optional[str] = None):
        """Authenticate to IBM Quantum and return a provider object.

        If `token` is None, the function will attempt to read from
        the environment variable `IBM_QUANTUM_TOKEN`.
        """
        try:
            # Lazy import to avoid hard dependency at module import
            from qiskit_ibm_runtime import IBMProvider
        except Exception as e:
            raise RuntimeError("qiskit-ibm-runtime is required for IBM integration: " + str(e))

        tok = token or os.environ.get('IBM_QUANTUM_TOKEN')
        if not tok:
            raise ValueError("IBM Quantum API token not provided. Set IBM_QUANTUM_TOKEN environment variable or pass token parameter.")

        # Create provider; url is optional for default cloud
        if url:
            provider = IBMProvider(token=tok, url=url)
        else:
            provider = IBMProvider(token=tok)
        return provider

    def list_backends(self, provider) -> List[str]:
        """Return a list of available backend names for the authenticated provider."""
        try:
            backends = provider.backends()
            return [b.name() if hasattr(b, 'name') else str(b) for b in backends]
        except Exception as e:
            raise RuntimeError("Failed to list backends: " + str(e))

    def run_circuit(self, provider, backend_name: str, circuit, shots: int = 8192, timeout: int = 600):
        """Submit a Qiskit `QuantumCircuit` to the named backend and return a job/result.

        This function uses common runtime APIs but may need adaptation depending
        on qiskit-ibm-runtime version. It raises informative errors on failure.
        """
        try:
            backend = provider.get_backend(backend_name)
        except Exception:
            # Some versions use provider.backend or provider.get_backend
            try:
                backend = provider.backend(backend_name)
            except Exception as e:
                raise RuntimeError("Could not access backend: " + str(e))

        try:
            # Many IBM runtime backends offer a simple run/circuit API
            job = backend.run(circuit, shots=shots)
            # Try to fetch result (may block until completion)
            result = job.result(timeout=timeout)
            return result
        except Exception as e:
            raise RuntimeError("Failed to run circuit on backend: " + str(e))
