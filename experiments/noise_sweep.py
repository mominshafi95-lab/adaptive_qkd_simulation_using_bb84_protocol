import sys
from pathlib import Path

# Ensure project root is on sys.path so sibling packages import correctly
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import numpy as np
from core.bb84_engine import BB84Engine
from core.metrics import secure_key_rate
from utils.visualization import plot_line, save_performance_plots
from config import ExperimentConfig

def run_noise_sweep():
    print("Starting Noise Sweep Analysis...")
    print(f"Simulating {ExperimentConfig.NOISE_LEVELS} noise levels from {ExperimentConfig.MIN_NOISE*100:.1f}% to {ExperimentConfig.MAX_NOISE*100:.1f}%...")
    
    noise_levels = np.linspace(ExperimentConfig.MIN_NOISE, ExperimentConfig.MAX_NOISE, ExperimentConfig.NOISE_LEVELS)
    qbers = []
    key_rates = []

    for idx, p in enumerate(noise_levels):
        print("  Progress: [{}/{}] Simulating at noise level: {:.2f}%".format(idx+1, ExperimentConfig.NOISE_LEVELS, p*100))
        engine = BB84Engine(ExperimentConfig.NUM_QUBITS, p)
        result = engine.run()
        if "qber" in result:
            qbers.append(result["qber"])
            key_rates.append(secure_key_rate(result["qber"]))
        else:
            # Mark missing data as NaN to preserve index alignment
            qbers.append(float('nan'))
            key_rates.append(float('nan'))

    print("Simulations complete. Generating plots...")
    
    # Filter out points where measurement failed (nan)
    import numpy as _np
    nl = _np.asarray(noise_levels)
    q_arr = _np.asarray(qbers)
    kr_arr = _np.asarray(key_rates)

    valid_mask_q = ~_np.isnan(q_arr)
    valid_mask_kr = ~_np.isnan(kr_arr)

    if valid_mask_q.any():
        plot_line(nl[valid_mask_q].tolist(), q_arr[valid_mask_q].tolist(),
                  "Noise Probability", "QBER",
                  "QBER vs Noise")

    if valid_mask_kr.any():
        plot_line(nl[valid_mask_kr].tolist(), kr_arr[valid_mask_kr].tolist(),
                  "Noise Probability", "Secure Key Rate",
                  "Secure Key Rate vs Noise")

    # Save publication-ready performance plots (if enabled)
    if ExperimentConfig.SAVE_PLOTS:
        out = save_performance_plots(noise_levels.tolist(), qbers, key_rates,
                                     outdir='output/plots', prefix='noise_sweep')
        print("Saved plots:", out)
    print("Noise Sweep Analysis complete!")


