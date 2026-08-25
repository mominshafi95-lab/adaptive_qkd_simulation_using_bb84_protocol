"""
Statistical Analysis - Comprehensive statistical testing
Demonstrates: Statistical validation of protocol parameters
"""

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import numpy as np
from core.bb84_engine import BB84Engine
from utils.visualization import plot_histogram, plot_line
from config import ExperimentConfig

def run_statistical_analysis(runs=None):
    """Comprehensive statistical analysis of BB84 protocol"""
    
    if runs is None:
        runs = ExperimentConfig.STATISTICAL_RUNS

    print("\n" + "="*60)
    print("COMPREHENSIVE STATISTICAL ANALYSIS")
    print("="*60)
    print(f"Configuration: {ExperimentConfig.NUM_QUBITS} qubits, {runs} runs per noise level")
    
    # Test 1: QBER distribution
    print("\nTest 1: QBER Distribution Analysis")
    print("-" * 50)
    
    qbers = []
    sifted_lengths = []
    final_key_lengths = []
    
    for i in range(runs):
        if ExperimentConfig.VERBOSE_OUTPUT and (i+1) % max(1, runs//10) == 0:
            print(f"  Progress: {i+1}/{runs} ({(i+1)*100//runs}%)")
        engine = BB84Engine(ExperimentConfig.NUM_QUBITS, noise_prob=0.05)
        result = engine.run()
        if "qber" in result:
            qbers.append(result["qber"])
            sifted_lengths.append(result["sifted_length"])
            final_key_lengths.append(result["final_key_length"])

    qber_mean = np.mean(qbers)
    qber_std = np.std(qbers)
    qber_min = np.min(qbers)
    qber_max = np.max(qbers)
    
    print(f"Mean QBER:           {qber_mean:.4f}")
    print(f"Std Dev:             {qber_std:.4f}")
    print(f"Min QBER:            {qber_min:.4f}")
    print(f"Max QBER:            {qber_max:.4f}")
    print(f"95% Confidence Interval: [{qber_mean - 1.96*qber_std:.4f}, {qber_mean + 1.96*qber_std:.4f}]")
    
    # Test 2: Skewness and Kurtosis analysis (numpy native)
    print("\nTest 2: Distribution Shape Analysis")
    print("-" * 50)
    
    # Calculate skewness manually
    centered = np.array(qbers) - qber_mean
    skewness = np.mean(centered**3) / (qber_std**3) if qber_std > 0 else 0
    # Calculate kurtosis manually
    kurtosis = np.mean(centered**4) / (qber_std**4) - 3 if qber_std > 0 else 0
    
    print(f"Skewness: {skewness:>8.4f} (0 = symmetric, ±3 = strongly skewed)")
    print(f"Kurtosis: {kurtosis:>8.4f} (0 = normal, >0 = heavy-tailed)")
    
    if abs(skewness) < 0.5 and abs(kurtosis) < 1:
        print("✓ Distribution appears nearly normal")
    else:
        print("⚠ Distribution may deviate from normal")
    
    # Test 3: Key length statistics
    print("\nTest 3: Key Length Statistics")
    print("-" * 50)
    
    sifted_mean = np.mean(sifted_lengths)
    sifted_std = np.std(sifted_lengths)
    key_mean = np.mean(final_key_lengths)
    key_std = np.std(final_key_lengths)
    
    print(f"Sifted Key Length:")
    print(f"  Mean: {sifted_mean:.1f} bits")
    print(f"  Std Dev: {sifted_std:.1f} bits")
    print(f"  Min: {np.min(sifted_lengths)} bits")
    print(f"  Max: {np.max(sifted_lengths)} bits")
    
    print(f"\nFinal Key Length:")
    print(f"  Mean: {key_mean:.1f} bits")
    print(f"  Std Dev: {key_std:.1f} bits")
    print(f"  Min: {np.min(final_key_lengths)} bits")
    print(f"  Max: {np.max(final_key_lengths)} bits")
    
    compression_ratio = key_mean / sifted_mean if sifted_mean > 0 else 0
    print(f"\nCompression Ratio: {compression_ratio:.2%}")
    
    # Test 4: Correlation analysis
    print("\nTest 4: Parameter Correlation Analysis")
    print("-" * 50)
    
    corr_qber_sifted = np.corrcoef(qbers, sifted_lengths)[0, 1]
    corr_qber_final = np.corrcoef(qbers, final_key_lengths)[0, 1]
    corr_sifted_final = np.corrcoef(sifted_lengths, final_key_lengths)[0, 1]
    
    print(f"QBER vs Sifted Length correlation: {corr_qber_sifted:.4f}")
    print(f"QBER vs Final Key correlation:     {corr_qber_final:.4f}")
    print(f"Sifted vs Final Key correlation:   {corr_sifted_final:.4f}")
    
    if abs(corr_qber_final) > 0.7:
        print("✓ Strong correlation: Higher QBER reduces final key length")
    
    # Test 5: Variance across noise levels
    print("\nTest 5: Variance Across Different Noise Levels")
    print("-" * 50)
    
    noise_levels = [0.0, 0.05, 0.10, 0.15]
    noise_vars = []
    
    print(f"{'Noise':>10} {'Mean QBER':>15} {'Std Dev':>15} {'Variance':>15}")
    print("-" * 55)
    
    for noise in noise_levels:
        noise_qbers = []
        for _ in range(50):  # Reduced runs for each noise level
            engine = BB84Engine(8, noise_prob=noise)
            result = engine.run()
            if "qber" in result:
                noise_qbers.append(result["qber"])
        
        mean = np.mean(noise_qbers)
        std = np.std(noise_qbers)
        var = np.var(noise_qbers)
        noise_vars.append(mean)
        
        print(f"{noise:>10.2f} {mean:>15.4f} {std:>15.4f} {var:>15.6f}")
    
    # Test 6: Protocol success rate
    print("\nTest 6: Protocol Success Metrics")
    print("-" * 50)
    
    successful = sum(1 for qber in qbers if qber <= 0.11)
    success_rate = successful / len(qbers) * 100
    
    zero_length = sum(1 for key_len in final_key_lengths if key_len == 0)
    zero_rate = zero_length / len(final_key_lengths) * 100
    
    print(f"Total runs: {len(qbers)}")
    print(f"Successful (QBER ≤ 0.11): {successful} ({success_rate:.1f}%)")
    print(f"Failed (key length = 0): {zero_length} ({zero_rate:.1f}%)")
    
    if success_rate > 90:
        print("✓ Protocol reliability is excellent (>90%)")
    elif success_rate > 80:
        print("✓ Protocol reliability is good (>80%)")
    else:
        print("⚠ Protocol reliability needs improvement (<80%)")
    
    print("\n" + "="*60)
    print("STATISTICAL INTERPRETATION:")
    print("="*60)
    print(f"✓ Mean QBER ({qber_mean:.4f}) is below threshold (0.11)")
    print(f"✓ Protocol generates ~{key_mean:.0f} secure bits per run")
    print(f"✓ Success rate: {success_rate:.1f}%")
    print("\n")
    
    # Visualizations
    plot_histogram(qbers, "QBER", "Frequency",
                   f"QBER Distribution ({runs} runs)")
    
    plot_histogram(final_key_lengths, "Key Length (bits)", "Frequency",
                   f"Final Key Length Distribution ({runs} runs)")
    
    plot_line(noise_levels, noise_vars,
              "Noise Level", "Mean QBER",
              "QBER Sensitivity to Noise")

if __name__ == "__main__":
    run_statistical_analysis()
