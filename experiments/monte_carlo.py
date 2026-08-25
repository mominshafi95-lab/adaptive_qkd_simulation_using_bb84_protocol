import sys
from pathlib import Path

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import numpy as np
from core.bb84_engine import BB84Engine
from utils.visualization import plot_histogram, save_histogram
from config import ExperimentConfig

def run_monte_carlo(runs=None, qubits=None, noise=0.05):
    # Use config values if not provided
    if runs is None:
        runs = ExperimentConfig.MONTE_CARLO_RUNS
    if qubits is None:
        qubits = ExperimentConfig.NUM_QUBITS

    print(f"Running {runs} Monte Carlo simulations with {qubits} qubits at {noise*100:.1f}% noise...")
    
    qbers = []

    for i in range(runs):
        if ExperimentConfig.VERBOSE_OUTPUT and (i+1) % max(1, runs//10) == 0:
            print(f"  Progress: {i+1}/{runs} simulations complete ({(i+1)*100//runs}%)")
        engine = BB84Engine(qubits, noise)
        result = engine.run()
        if "qber" in result:
            qbers.append(result["qber"])

    print("\n" + "="*50)
    print("Monte Carlo Results:")
    print("="*50)
    print(f"Mean QBER: {np.mean(qbers):.6f}")
    print(f"Std Dev: {np.std(qbers):.6f}")
    print(f"Min QBER: {np.min(qbers):.6f}")
    print(f"Max QBER: {np.max(qbers):.6f}")
    print("="*50 + "\n")

    plot_histogram(qbers, "QBER", "Frequency", "Monte Carlo QBER Distribution")

    # Save histogram to disk (if enabled)
    if ExperimentConfig.SAVE_PLOTS:
        outdir = 'output/plots'
        _ = save_histogram(qbers, 'QBER', 'Frequency', 'Monte Carlo QBER Distribution', f"{outdir}/monte_carlo_qber.png")

