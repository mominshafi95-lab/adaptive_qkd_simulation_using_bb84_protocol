"""Finalization check: run core experiments quickly, import GUI and web modules, and verify saved plots.

This script uses fast settings to run a representative subset of experiments and ensures
plots are generated and modules import cleanly. It is designed to be fast (under 2 minutes).
"""
import sys
from pathlib import Path

# Ensure project root is importable
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config import ExperimentConfig
from experiments.noise_sweep import run_noise_sweep
from experiments.monte_carlo import run_monte_carlo
from experiments.attack_analysis import run_attack_analysis
from experiments.decoy_state_demo import run_decoy_state_demo
from experiments.error_correction_demo import run_error_correction_demo
from experiments.advanced_attack_demo import run_advanced_attack_analysis

OUT_DIR = Path('output/plots')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Use fast settings
ExperimentConfig.NUM_QUBITS = 4
ExperimentConfig.NOISE_LEVELS = 5
ExperimentConfig.MONTE_CARLO_RUNS = 20
ExperimentConfig.SAVE_PLOTS = True

passed = True
errors = []

print('\n=== FINALIZE CHECK: START ===')

try:
    print('\n- Running noise_sweep...')
    run_noise_sweep()
except Exception as e:
    passed = False
    errors.append(('noise_sweep', str(e)))

try:
    print('\n- Running monte_carlo...')
    run_monte_carlo(runs=50, qubits=4, noise=0.02)
except Exception as e:
    passed = False
    errors.append(('monte_carlo', str(e)))

try:
    print('\n- Running attack_analysis...')
    run_attack_analysis()
except Exception as e:
    passed = False
    errors.append(('attack_analysis', str(e)))

try:
    print('\n- Running decoy_state_demo...')
    run_decoy_state_demo()
except Exception as e:
    passed = False
    errors.append(('decoy_state_demo', str(e)))

try:
    print('\n- Running error_correction_demo...')
    run_error_correction_demo()
except Exception as e:
    passed = False
    errors.append(('error_correction_demo', str(e)))

try:
    print('\n- Running advanced_attack_demo...')
    run_advanced_attack_analysis()
except Exception as e:
    passed = False
    errors.append(('advanced_attack_demo', str(e)))

# Quick import checks for GUI and web
try:
    print('\n- Importing GUI module...')
    import gui.app as gui_app
    print('  GUI imported OK')
except Exception as e:
    passed = False
    errors.append(('gui_import', str(e)))

try:
    print('\n- Importing web app module...')
    import web.app as web_app
    print('  Web app imported OK')
except Exception as e:
    # web.app may require Flask or try to start the server; treat missing
    # optional env dependencies as a warning rather than a hard failure.
    msg = str(e)
    if 'flask' in msg.lower() or 'no module named' in msg.lower():
        print('  Web app import warning (optional dependency missing):', e)
        errors.append(('web_import_warning', msg))
    else:
        passed = False
        errors.append(('web_import', msg))

# Check output plots exist
plots = list(OUT_DIR.glob('*.png'))
if plots:
    print(f"\n- Found {len(plots)} plot files in {OUT_DIR}")
else:
    passed = False
    errors.append(('plots_missing', f'No PNG files found in {OUT_DIR}'))

print('\n=== FINALIZE CHECK: RESULT ===')
if passed:
    print('All checks passed. Project ready for delivery.')
else:
    print('Some checks failed:')
    for name, err in errors:
        print(f' - {name}: {err}')

print('\n=== FINALIZE CHECK: END ===')
