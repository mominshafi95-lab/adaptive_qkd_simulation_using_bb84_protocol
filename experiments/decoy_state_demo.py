"""
Decoy State Analysis
Demonstrates: decoy_bb84.py, channel_model.py
"""

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import numpy as np
from core.bb84_engine import BB84Engine
from core.decoy_bb84 import DecoyStateBB84
from core.channel_model import apply_noise_model
from utils.randomness import RandomnessManager
from utils.visualization import plot_bar, plot_line, save_bar_chart, save_line_plot
from config import ExperimentConfig

def run_decoy_state_demo():
    """Demonstrate decoy state enhancement"""
    
    print("\n" + "="*60)
    print("DECOY STATE ANALYSIS")
    print("="*60)
    
    rng = RandomnessManager(seed=42)
    decoy_bb84 = DecoyStateBB84(rng)
    
    print("\nDecoy State Mechanism:")
    print("- Signal states: Legitimate quantum states carrying key bits")
    print("- Decoy states: Dummy states to detect eavesdropping")
    print("- Detection rate difference reveals channel tampering\n")
    
    # Test 1: Generate decoy states
    print("Test 1: Generate Decoy States")
    print("-" * 40)
    states = decoy_bb84.generate_states(n=100, signal_prob=0.7)
    signal_count = np.sum(states == "signal")
    decoy_count = np.sum(states == "decoy")
    print(f"Generated 100 states:")
    print(f"  Signal states: {signal_count} ({signal_count/100:.1%})")
    print(f"  Decoy states:  {decoy_count} ({decoy_count/100:.1%})")
    
    # Test 2: Channel loss estimation
    print("\nTest 2: Channel Loss Estimation")
    print("-" * 40)
    
    detection_results = rng.rng.choice([0, 1], size=100, p=[0.8, 0.2])
    loss_estimate = decoy_bb84.estimate_channel_loss(detection_results, states)
    
    print(f"Signal detection rate: {loss_estimate['signal_rate']:.2%}")
    print(f"Decoy detection rate:  {loss_estimate['decoy_rate']:.2%}")
    difference = abs(loss_estimate['signal_rate'] - loss_estimate['decoy_rate'])
    print(f"Rate difference:       {difference:.2%}")
    
    if difference > 0.05:
        print("⚠ WARNING: Significant difference detected - possible eavesdropping!")
    else:
        print("✓ Normal: Channel appears secure")
    
    # Test 3: Protocol with decoy states
    print("\nTest 3: Full Protocol Performance")
    print("-" * 40)
    print(f"{'With Decoy':>15} {'Key Length':>15} {'QBER':>10}")
    print("-" * 40)
    
    decoy_on = []
    decoy_off = []
    qbers_decoy = []
    qbers_regular = []
    
    for _ in range(10):
        # With decoy
        engine = BB84Engine(8, noise_prob=0.05)
        result_decoy = engine.run(use_decoy=True)
        decoy_on.append(result_decoy['final_key_length'])
        qbers_decoy.append(result_decoy['qber'])
        
        # Without decoy
        engine = BB84Engine(8, noise_prob=0.05)
        result_regular = engine.run(use_decoy=False)
        decoy_off.append(result_regular['final_key_length'])
        qbers_regular.append(result_regular['qber'])
        
        print(f"{'Yes':>15} {result_decoy['final_key_length']:>15} {result_decoy['qber']:>10.4f}")
        print(f"{'No':>15} {result_regular['final_key_length']:>15} {result_regular['qber']:>10.4f}")
        print("-" * 40)
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    print(f"Average key length with decoy:    {np.mean(decoy_on):.1f} bits")
    print(f"Average key length without decoy: {np.mean(decoy_off):.1f} bits")
    print(f"Average QBER with decoy:          {np.mean(qbers_decoy):.4f}")
    print(f"Average QBER without decoy:       {np.mean(qbers_regular):.4f}")
    print("\nDecoy states add ~20-30% overhead but significantly enhance detection")
    print("of eavesdropping attempts.\n")
    
    # Visualization
    labels = ['With Decoy', 'Without Decoy']
    avg_keys = [np.mean(decoy_on), np.mean(decoy_off)]
    plot_bar(labels, avg_keys, "Configuration", "Average Key Length (bits)",
             "Decoy State Impact on Key Length")
    if ExperimentConfig.SAVE_PLOTS:
        try:
            save_bar_chart(labels, avg_keys, 'Configuration', 'Average Key Length (bits)',
                           'Decoy State Impact on Key Length', 'output/plots/decoy_avg_keys.png')
        except Exception:
            pass

    plot_line(range(len(qbers_decoy)), qbers_decoy,
              "Run Number", "QBER",
              "QBER Comparison: With vs Without Decoy States")
    if ExperimentConfig.SAVE_PLOTS:
        try:
            save_line_plot(list(range(len(qbers_decoy))), qbers_decoy,
                           'Run Number', 'QBER', 'QBER Comparison: With vs Without Decoy States',
                           'output/plots/decoy_qber_comparison.png')
        except Exception:
            pass
