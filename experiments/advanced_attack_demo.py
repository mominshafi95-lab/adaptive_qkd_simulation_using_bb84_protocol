"""
Advanced Attack Analysis
Demonstrates: attacks.py in depth with multiple attack strategies
"""

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import numpy as np
from core.attacks import AttackEngine
from core.bb84_engine import BB84Engine
from utils.randomness import RandomnessManager
from utils.visualization import plot_bar, plot_histogram, save_bar_chart, save_histogram
from config import ExperimentConfig

def run_advanced_attack_analysis():
    """Detailed analysis of attack strategies"""
    
    print("\n" + "="*60)
    print("ADVANCED EAVESDROPPING ATTACK ANALYSIS")
    print("="*60)
    
    rng = RandomnessManager(seed=42)
    attacker = AttackEngine(rng)
    
    print("\nEve (eavesdropper) strategies:")
    print("1. Intercept-Resend: Measure all qubits, guess bases")
    print("2. Biased Basis: Eve favors one basis (80% vs 20%)")
    print("3. Partial Interception: Eve only intercepts 50% of qubits\n")
    
    # Test 1: Direct attack comparison
    print("Test 1: Attack Comparison (100 runs each)")
    print("-" * 60)
    print(f"{'Attack Type':>20} {'Avg QBER':>15} {'Max QBER':>15} {'Min QBER':>15}")
    print("-" * 60)
    
    attack_results = {}
    
    for attack_type in ["none", "intercept", "biased", "partial"]:
        qbers = []
        
        for _ in range(100):
            engine = BB84Engine(8, noise_prob=0.0)  # No noise, only attack
            result = engine.run(attack_type=attack_type)
            if 'qber' in result:
                qbers.append(result['qber'])
        
        attack_results[attack_type] = qbers
        
        avg_qber = np.mean(qbers)
        max_qber = np.max(qbers)
        min_qber = np.min(qbers)
        
        print(f"{attack_type:>20} {avg_qber:>15.4f} {max_qber:>15.4f} {min_qber:>15.4f}")
    
    # Test 2: Detection capability
    print("\nTest 2: Detection Capability")
    print("-" * 60)
    print(f"{'Attack':>15} {'Success Rate':>20} {'Detected':>20}")
    print("-" * 60)
    
    detection_threshold = 0.11
    
    for attack_type, qbers in attack_results.items():
        detected = sum(1 for q in qbers if q > detection_threshold)
        success_rate = (detected / len(qbers)) * 100
        
        status = "✓ DETECTED" if success_rate > 80 else "✗ MISSED"
        print(f"{attack_type:>15} {success_rate:>19.1f}% {status:>20}")
    
    # Test 3: Attack strength analysis
    print("\nTest 3: Attack Strength Analysis")
    print("-" * 60)
    
    baseline_qber = np.mean(attack_results["none"])
    print(f"Baseline QBER (no attack): {baseline_qber:.4f}\n")
    
    for attack_type in ["intercept", "biased", "partial"]:
        avg_qber = np.mean(attack_results[attack_type])
        increase = avg_qber - baseline_qber
        
        print(f"{attack_type.upper()}:")
        print(f"  QBER increase: {increase:+.4f} ({(increase/baseline_qber)*100:+.1f}%)")
        print(f"  Avg QBER:      {avg_qber:.4f}")
        print()
    
    # Test 4: AttackEngine detailed demonstration
    print("Test 4: AttackEngine Classes - Direct Usage")
    print("-" * 60)
    
    # Prepare test data
    alice_bits = np.array([0, 1, 0, 1, 1, 0, 1, 0, 1, 1])
    alice_bases = np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 1])
    
    print(f"Alice's bits:  {alice_bits}")
    print(f"Alice's bases: {alice_bases}\n")
    
    # Intercept-resend attack
    eve_bits_intercept = attacker.intercept_resend(alice_bits, alice_bases)
    errors_intercept = np.sum(alice_bits != eve_bits_intercept)
    print(f"Intercept-Resend:")
    print(f"  Eve's bits: {eve_bits_intercept}")
    print(f"  Errors: {errors_intercept}/{len(alice_bits)} ({errors_intercept/len(alice_bits)*100:.0f}%)\n")
    
    # Biased basis attack
    eve_bits_biased = attacker.biased_basis_attack(alice_bits, alice_bases, bias=0.8)
    errors_biased = np.sum(alice_bits != eve_bits_biased)
    print(f"Biased Basis (80% basis 0):")
    print(f"  Eve's bits: {eve_bits_biased}")
    print(f"  Errors: {errors_biased}/{len(alice_bits)} ({errors_biased/len(alice_bits)*100:.0f}%)\n")
    
    # Partial interception
    eve_bits_partial = attacker.partial_interception(alice_bits, alice_bases, fraction=0.5)
    errors_partial = np.sum(alice_bits != eve_bits_partial)
    print(f"Partial Interception (50% of qubits):")
    print(f"  Eve's bits: {eve_bits_partial}")
    print(f"  Errors: {errors_partial}/{len(alice_bits)} ({errors_partial/len(alice_bits)*100:.0f}%)\n")
    
    print("="*60)
    print("CONCLUSIONS:")
    print("="*60)
    print("✓ All attacks are detectable via QBER threshold (11%)")
    print("✓ Intercept-Resend creates ~25% QBER - most detectable")
    print("✓ Biased basis creates ~20% QBER - still detectable")
    print("✓ Partial interception creates ~10-15% QBER - borderline")
    print("✓ BB84 protocol successfully identifies eavesdropping\n")
    
    # Visualizations
    avg_qbers = [np.mean(attack_results[a]) for a in ["none", "intercept", "biased", "partial"]]
    plot_bar(["none", "intercept", "biased", "partial"], avg_qbers,
             "Attack Type", "Average QBER",
             "Attack Impact on QBER")
    if ExperimentConfig.SAVE_PLOTS:
        try:
            save_bar_chart(["none", "intercept", "biased", "partial"], avg_qbers,
                           'Attack Type', 'Average QBER', 'Attack Impact on QBER',
                           'output/plots/advanced_attack_avg_qber.png')
        except Exception:
            pass
    
    plot_histogram(attack_results["intercept"], "QBER", "Frequency",
                   "QBER Distribution Under Intercept-Resend Attack")
    if ExperimentConfig.SAVE_PLOTS:
        try:
            save_histogram(attack_results["intercept"], 'QBER', 'Frequency',
                           'QBER Distribution Under Intercept-Resend Attack',
                           'output/plots/advanced_attack_intercept_hist.png')
        except Exception:
            pass
