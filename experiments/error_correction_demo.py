"""
Error Correction Analysis
Demonstrates: error_correction.py, metrics.py
"""

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import numpy as np
from core.bb84_engine import BB84Engine
from core.error_correction import ErrorCorrector
from core.metrics import calculate_qber
from utils.visualization import plot_histogram, plot_line, save_histogram, save_line_plot
from config import ExperimentConfig

def run_error_correction_demo():
    """Demonstrate error correction performance"""
    
    print("\n" + "="*60)
    print("ERROR CORRECTION ANALYSIS")
    print("="*60)
    
    error_corrector = ErrorCorrector()
    noise_levels = np.linspace(0, 0.2, 10)
    
    error_rates_before = []
    error_rates_after = []
    leakage_bits = []
    
    print("\nError Correction Performance Analysis:")
    print(f"{'Noise':>8} {'Errors Before':>15} {'Errors After':>15} {'Leakage':>10}")
    print("-" * 50)
    
    for noise in noise_levels:
        engine = BB84Engine(8, noise)
        result = engine.run()
        
        if result.get('sifted_length', 0) == 0:
            continue
        
        # Extract raw keys from protocol
        alice_bits = engine.random_bits()
        alice_bases = engine.random_bases()
        bob_bases = engine.random_bases()
        
        # Simulate measurement with noise
        bob_bits = alice_bits.copy()
        noise_indices = np.random.choice(len(bob_bits), 
                                        int(len(bob_bits) * noise), 
                                        replace=False)
        bob_bits[noise_indices] = 1 - bob_bits[noise_indices]
        
        # Apply error correction
        corrected_bob, leakage = error_corrector.reconcile(alice_bits, bob_bits)[1:]
        
        # Calculate error rates
        errors_before = np.sum(alice_bits != bob_bits)
        errors_after = np.sum(alice_bits != corrected_bob)
        
        error_rates_before.append(errors_before / len(alice_bits) if len(alice_bits) > 0 else 0)
        error_rates_after.append(errors_after / len(alice_bits) if len(alice_bits) > 0 else 0)
        leakage_bits.append(leakage)
        
        print(f"{noise:>8.3f} {errors_before:>15} {errors_after:>15} {leakage:>10}")
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    print(f"✓ Errors before correction: {max(error_rates_before):.2%}")
    print(f"✓ Errors after correction:  {max(error_rates_after):.2%}")
    print(f"✓ Information leakage avg:  {np.mean(leakage_bits):.2f} bits")
    print("\nError correction uses parity checks to reconcile Alice and Bob's keys.")
    print("Leakage represents bits revealed during the reconciliation process.")
    print("\n")
    
    # Visualizations
    plot_line(noise_levels[:len(error_rates_before)], error_rates_before,
              "Noise Probability", "Error Rate",
              "Error Rate Before Correction")
    if ExperimentConfig.SAVE_PLOTS:
        try:
            save_line_plot(list(noise_levels[:len(error_rates_before)]), error_rates_before,
                           'Noise Probability', 'Error Rate', 'Error Rate Before Correction',
                           'output/plots/error_correction_before.png')
        except Exception:
            pass

    plot_line(noise_levels[:len(error_rates_after)], error_rates_after,
              "Noise Probability", "Error Rate",
              "Error Rate After Correction")
    if ExperimentConfig.SAVE_PLOTS:
        try:
            save_line_plot(list(noise_levels[:len(error_rates_after)]), error_rates_after,
                           'Noise Probability', 'Error Rate', 'Error Rate After Correction',
                           'output/plots/error_correction_after.png')
        except Exception:
            pass

    plot_histogram(leakage_bits, "Leakage (bits)", "Frequency",
                   "Information Leakage Distribution")
    if ExperimentConfig.SAVE_PLOTS:
        try:
            save_histogram(leakage_bits, 'Leakage (bits)', 'Frequency', 'Information Leakage Distribution',
                           'output/plots/error_correction_leakage.png')
        except Exception:
            pass
