"""
Comprehensive security analysis using SecurityAnalyzer, information theory, and finite key correction.
Demonstrates: security_analysis.py, information_theory.py, finite_key.py
"""

import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import numpy as np
from core.bb84_engine import BB84Engine
from core.security_analysis import SecurityAnalyzer
from core.information_theory import binary_entropy, mutual_information_ab, eve_information_estimate
from core.finite_key import finite_key_correction
from utils.visualization import plot_line

def run_security_deep_dive():
    """Detailed security analysis with information theory metrics"""
    
    print("\n" + "="*60)
    print("SECURITY ANALYSIS DEEP DIVE")
    print("="*60)
    
    analyzer = SecurityAnalyzer()
    noise_levels = np.linspace(0, 0.15, 8)
    
    adjusted_qbers = []
    i_ab_values = []
    i_ae_values = []
    security_margin = []
    
    print("\nAnalyzing protocol security across noise levels:")
    print(f"{'Noise':>8} {'QBER':>8} {'Adj.QBER':>10} {'I(A:B)':>8} {'I(A:E)':>8} {'Margin':>8} {'Secure':>8}")
    print("-" * 70)
    
    for noise in noise_levels:
        # Run protocol
        engine = BB84Engine(8, noise)
        result = engine.run()
        
        if result.get('sifted_length', 0) == 0:
            continue
        
        # Deep security analysis
        analysis = analyzer.analyze(result['qber'], result['sifted_length'])
        
        adjusted_qbers.append(analysis['adjusted_qber'])
        i_ab_values.append(analysis['I_AB'])
        i_ae_values.append(analysis['I_AE'])
        margin = analysis['I_AB'] - analysis['I_AE']
        security_margin.append(margin)
        
        security_status = "✓ SECURE" if analysis['secure'] else "✗ INSECURE"
        
        print(f"{noise:>8.3f} {result['qber']:>8.4f} {analysis['adjusted_qber']:>10.4f} "
              f"{analysis['I_AB']:>8.4f} {analysis['I_AE']:>8.4f} {margin:>8.4f} {security_status:>8}")
    
    print("\n" + "="*60)
    print("RESULTS INTERPRETATION:")
    print("="*60)
    print(f"I(A:B) = Alice-Bob mutual information (legitimate shared key)")
    print(f"I(A:E) = Eve's maximum information (eavesdropper potential)")
    print(f"Security Margin = I(A:B) - I(A:E) (must be > 0 for security)")
    print(f"Threshold: adjusted_QBER must be ≤ 0.11")
    print("\n")
    
    # Plot security metrics
    plot_line(noise_levels[:len(adjusted_qbers)], i_ab_values,
              "Noise Probability", "I(A:B) bits",
              "Legitimate Information vs Noise")
    
    plot_line(noise_levels[:len(adjusted_qbers)], i_ae_values,
              "Noise Probability", "I(A:E) bits",
              "Eve's Information vs Noise")
    
    plot_line(noise_levels[:len(adjusted_qbers)], security_margin,
              "Noise Probability", "Security Margin (bits)",
              "Security Margin: I(A:B) - I(A:E)")
