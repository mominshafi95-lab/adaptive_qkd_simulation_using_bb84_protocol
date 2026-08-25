"""Simple smoke test that runs a fast noise sweep to verify plotting works.

This reduces configuration sizes to run quickly and checks for generated files.
"""
from pathlib import Path
import sys
from pathlib import Path

# Ensure project root is on sys.path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config import ExperimentConfig
from experiments.noise_sweep import run_noise_sweep

def run_smoke():
    # Use fast settings
    ExperimentConfig.NUM_QUBITS = 4
    ExperimentConfig.NOISE_LEVELS = 5
    ExperimentConfig.MONTE_CARLO_RUNS = 10
    ExperimentConfig.SAVE_PLOTS = True

    out_dir = Path('output/plots')
    if out_dir.exists():
        # remove old files (keep simple)
        for f in out_dir.glob('smoke_*'):
            try:
                f.unlink()
            except Exception:
                pass

    print('Running smoke test (fast noise sweep)...')
    run_noise_sweep()

    # Check for created files
    created = list(out_dir.glob('noise_sweep*'))
    if created:
        print('Smoke test passed - plots created:')
        for f in created:
            print('  -', f)
    else:
        print('Smoke test failed - no plots found in', out_dir)

if __name__ == '__main__':
    run_smoke()
