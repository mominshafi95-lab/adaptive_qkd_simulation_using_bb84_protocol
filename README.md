# BB84 Adaptive QKD Framework

Quick guide for running experiments and generating publication-ready plots.

Requirements
- Python 3.8+
- Install dependencies:

```powershell
pip install -r requirements.txt
```

Running the CLI

```powershell
python main.py
# Use menu to run experiments (1..11)
```

Toggle automatic plot saving
- Disable: `python main.py --no-plots`
- Enable explicitly: `python main.py --save-plots`

Output
- Automatic plots are saved to `output/plots/` (PNG files).

Smoke test

```powershell
python scripts\smoke_test.py
```

For more details, see `QUICK_REFERENCE.md`.

IBM Quantum Integration
-----------------------

To interact with IBM Quantum devices you must set your API token in the environment:

```powershell
setx IBM_QUANTUM_TOKEN "<YOUR_TOKEN>"
# restart terminal then verify with:
echo %IBM_QUANTUM_TOKEN%
```

Example: list available backends

```powershell
python scripts\run_on_ibm.py --list
```

To attempt a small test run (may queue on real hardware):

```powershell
python scripts\run_on_ibm.py --run-test --backend ibm_perth
```

Note: The `qiskit-ibm-runtime` package is required; it is included in `requirements.txt`.

Exporting BB84 circuits for real hardware
------------------------------------------

The `BB84Engine` can export Qiskit `QuantumCircuit` objects for submission to IBM backends.

Example code:

```python
from core.bb84_engine import BB84Engine

engine = BB84Engine(num_qubits=3)
enc_circuit, meas_circuit, metadata = engine.export_for_ibm()

# enc_circuit: Alice's state preparation
# meas_circuit: Bob's measurement basis & collapse
# metadata: {"alice_bits", "alice_bases", "bob_bases", ...}

# Submit enc_circuit to IBM backend, then meas_circuit after measurement
```

Example script:

```powershell
python scripts\run_bb84_on_ibm.py --num-qubits 3 --compare-local --backend ibm_perth
```

This runs a local simulation and exports circuits for comparison with real hardware.
