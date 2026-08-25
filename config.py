# Configuration Module - Customize Experiment Parameters

class ExperimentConfig:
    """
    Central configuration for all experiments.
    Modify these values to customize behavior.
    """
    
    # Quantum System Settings
    NUM_QUBITS = 8                    # Number of qubits (4-16 recommended, more = slower)
    NUM_BASES = 2                     # Rectilinear and Diagonal bases
    
    # Noise Settings (Depolarizing Channel)
    MIN_NOISE = 0.0                   # Minimum noise probability
    MAX_NOISE = 0.2                   # Maximum noise probability (20%)
    NOISE_LEVELS = 10                 # Number of noise levels to simulate
    
    # Monte Carlo Settings
    MONTE_CARLO_RUNS = 200            # Number of independent runs
    
    # Error Correction Settings
    ERROR_CORRECTION_ENABLED = True   # Enable/disable error correction
    INFORMATION_LEAKAGE_TOLERANCE = 0.1  # Eve's max info leakage (bits)
    
    # Security Settings
    QBER_THRESHOLD = 0.11             # ~11% QBER threshold for eavesdropping detection
    HONEST_QBER = 0.0373              # ~3.73% QBER for honest communication (no eavesdropping)
    
    # Privacy Amplification
    PRIVACY_AMPLIFICATION_METHOD = "sha256"  # "xor" or "sha256"
    PRIVACY_COMPRESSION_RATIO = 0.5   # Compress to 50% of sifted key
    
    # Statistical Analysis
    STATISTICAL_RUNS = 100            # Number of runs per noise level
    CONFIDENCE_LEVEL = 0.95           # 95% confidence interval
    
    # Attack Simulation
    ENABLE_PNS_ATTACK = True          # Photon Number Splitting
    ENABLE_INTERCEPT_RESEND = True    # Intercept-Resend
    ENABLE_TROJAN_HORSE = True        # Trojan Horse
    
    # Output Settings
    VERBOSE_OUTPUT = True             # Show detailed progress
    SHOW_STATISTICS = True            # Show min/max/mean/stddev
    SAVE_PLOTS = True                 # Automatically save plots to disk
    
    @classmethod
    def print_current_config(cls):
        """Print current configuration"""
        print("\n" + "="*70)
        print("CURRENT EXPERIMENT CONFIGURATION")
        print("="*70)
        print(f"\n[QUANTUM SYSTEM]")
        print(f"  • Qubits: {cls.NUM_QUBITS}")
        print(f"  • Bases: {cls.NUM_BASES}")
        
        print(f"\n[NOISE SETTINGS]")
        print(f"  • Noise Range: {cls.MIN_NOISE*100:.1f}% to {cls.MAX_NOISE*100:.1f}%")
        print(f"  • Noise Levels: {cls.NOISE_LEVELS}")
        
        print(f"\n[MONTE CARLO]")
        print(f"  • Runs: {cls.MONTE_CARLO_RUNS}")
        
        print(f"\n[SECURITY]")
        print(f"  • QBER Threshold: {cls.QBER_THRESHOLD*100:.1f}%")
        print(f"  • Honest QBER: {cls.HONEST_QBER*100:.2f}%")
        print(f"  • Max Info Leakage: {cls.INFORMATION_LEAKAGE_TOLERANCE} bits")
        
        print(f"\n[PRIVACY AMPLIFICATION]")
        print(f"  • Method: {cls.PRIVACY_AMPLIFICATION_METHOD}")
        print(f"  • Compression: {cls.PRIVACY_COMPRESSION_RATIO*100:.0f}%")
        
        print(f"\n[STATISTICAL ANALYSIS]")
        print(f"  • Runs per noise level: {cls.STATISTICAL_RUNS}")
        print(f"  • Confidence: {cls.CONFIDENCE_LEVEL*100:.0f}%")
        
        print(f"\n[ATTACKS ENABLED]")
        print(f"  • PNS Attack: {'Yes' if cls.ENABLE_PNS_ATTACK else 'No'}")
        print(f"  • Intercept-Resend: {'Yes' if cls.ENABLE_INTERCEPT_RESEND else 'No'}")
        print(f"  • Trojan Horse: {'Yes' if cls.ENABLE_TROJAN_HORSE else 'No'}")
        
        print(f"\n[OUTPUT]")
        print(f"  • Verbose: {'Yes' if cls.VERBOSE_OUTPUT else 'No'}")
        print(f"  • Statistics: {'Yes' if cls.SHOW_STATISTICS else 'No'}")
        print(f"  • Auto-save plots: {'Yes' if cls.SAVE_PLOTS else 'No'}")
        print("="*70 + "\n")
    
    @classmethod
    def interactive_configuration(cls):
        """Launch interactive configuration menu"""
        while True:
            print("\n" + "="*70)
            print("CONFIGURE EXPERIMENT PARAMETERS")
            print("="*70)
            print("\n[QUICK PRESETS]")
            print("  1. Fast & Simple (4 qubits, 5 noise levels, 50 runs)")
            print("  2. Balanced (8 qubits, 10 noise levels, 100 runs) - DEFAULT")
            print("  3. Detailed (8 qubits, 20 noise levels, 200 runs)")
            print("  4. Comprehensive (12 qubits, 15 noise levels, 300 runs) - SLOW!")
            
            print("\n[MANUAL CONFIGURATION]")
            print("  5. Custom Quantum Settings (qubits, noise range)")
            print("  6. Custom Simulation Settings (runs, noise levels)")
            print("  7. Custom Security Settings (thresholds, parameters)")
            print("  8. Custom Attack Settings (which attacks to enable)")
            print("  9. Toggle Output Verbosity")
            
            print("\n[OTHER]")
            print("  10. View Current Configuration")
            print("  11. Save Configuration to File")
            print("  12. Load Configuration from File")
            print("  0. Exit Configuration & Run Experiments")
            
            choice = input("\nSelect option (0-12): ").strip()
            
            if choice == "1":
                cls.preset_fast()
                print("✅ Applied: Fast & Simple preset")
            elif choice == "2":
                cls.preset_balanced()
                print("✅ Applied: Balanced preset (DEFAULT)")
            elif choice == "3":
                cls.preset_detailed()
                print("✅ Applied: Detailed preset")
            elif choice == "4":
                cls.preset_comprehensive()
                print("✅ Applied: Comprehensive preset (this will be slow!)")
            elif choice == "5":
                cls.configure_quantum()
            elif choice == "6":
                cls.configure_simulation()
            elif choice == "7":
                cls.configure_security()
            elif choice == "8":
                cls.configure_attacks()
            elif choice == "9":
                cls.VERBOSE_OUTPUT = not cls.VERBOSE_OUTPUT
                cls.SHOW_STATISTICS = not cls.SHOW_STATISTICS
                print(f"✅ Verbosity toggled to: {cls.VERBOSE_OUTPUT}")
            elif choice == "10":
                cls.print_current_config()
            elif choice == "11":
                cls.save_config()
            elif choice == "12":
                cls.load_config()
            elif choice == "0":
                print("\n✅ Configuration complete! Starting experiments...\n")
                break
            else:
                print("❌ Invalid option. Try again.")
    
    @classmethod
    def preset_fast(cls):
        """Fast & Simple: 4 qubits, 5 noise levels, 50 runs"""
        cls.NUM_QUBITS = 4
        cls.NOISE_LEVELS = 5
        cls.MONTE_CARLO_RUNS = 50
        cls.STATISTICAL_RUNS = 50
    
    @classmethod
    def preset_balanced(cls):
        """Balanced: 8 qubits, 10 noise levels, 100 runs (DEFAULT)"""
        cls.NUM_QUBITS = 8
        cls.NOISE_LEVELS = 10
        cls.MONTE_CARLO_RUNS = 200
        cls.STATISTICAL_RUNS = 100
    
    @classmethod
    def preset_detailed(cls):
        """Detailed: 8 qubits, 20 noise levels, 200 runs"""
        cls.NUM_QUBITS = 8
        cls.NOISE_LEVELS = 20
        cls.MONTE_CARLO_RUNS = 200
        cls.STATISTICAL_RUNS = 200
    
    @classmethod
    def preset_comprehensive(cls):
        """Comprehensive: 12 qubits, 15 noise levels, 300 runs"""
        cls.NUM_QUBITS = 12
        cls.NOISE_LEVELS = 15
        cls.MONTE_CARLO_RUNS = 300
        cls.STATISTICAL_RUNS = 300
    
    @classmethod
    def configure_quantum(cls):
        """Interactively configure quantum settings"""
        print("\n" + "-"*50)
        print("QUANTUM SYSTEM CONFIGURATION")
        print("-"*50)
        
        try:
            qubits = input(f"Number of qubits (current: {cls.NUM_QUBITS}, recommended: 4-12): ").strip()
            if qubits:
                q = int(qubits)
                if 1 <= q <= 20:
                    cls.NUM_QUBITS = q
                    print(f"✅ Set qubits to {q}")
                else:
                    print("❌ Qubits must be between 1-20")
            
            min_n = input(f"Min noise (0-1, current: {cls.MIN_NOISE}): ").strip()
            if min_n:
                cls.MIN_NOISE = float(min_n)
                print(f"✅ Set min noise to {cls.MIN_NOISE*100:.1f}%")
            
            max_n = input(f"Max noise (0-1, current: {cls.MAX_NOISE}): ").strip()
            if max_n:
                cls.MAX_NOISE = float(max_n)
                print(f"✅ Set max noise to {cls.MAX_NOISE*100:.1f}%")
                
        except ValueError:
            print("❌ Invalid input. Keeping current values.")
    
    @classmethod
    def configure_simulation(cls):
        """Interactively configure simulation settings"""
        print("\n" + "-"*50)
        print("SIMULATION CONFIGURATION")
        print("-"*50)
        
        try:
            levels = input(f"Noise levels (current: {cls.NOISE_LEVELS}): ").strip()
            if levels:
                cls.NOISE_LEVELS = int(levels)
                print(f"✅ Set noise levels to {cls.NOISE_LEVELS}")
            
            runs = input(f"Monte Carlo runs (current: {cls.MONTE_CARLO_RUNS}): ").strip()
            if runs:
                cls.MONTE_CARLO_RUNS = int(runs)
                print(f"✅ Set Monte Carlo runs to {cls.MONTE_CARLO_RUNS}")
            
            stat_runs = input(f"Statistical runs per level (current: {cls.STATISTICAL_RUNS}): ").strip()
            if stat_runs:
                cls.STATISTICAL_RUNS = int(stat_runs)
                print(f"✅ Set statistical runs to {cls.STATISTICAL_RUNS}")
                
        except ValueError:
            print("❌ Invalid input. Keeping current values.")
    
    @classmethod
    def configure_security(cls):
        """Interactively configure security settings"""
        print("\n" + "-"*50)
        print("SECURITY CONFIGURATION")
        print("-"*50)
        
        try:
            threshold = input(f"QBER threshold % (current: {cls.QBER_THRESHOLD*100:.1f}%): ").strip()
            if threshold:
                cls.QBER_THRESHOLD = float(threshold) / 100
                print(f"✅ Set QBER threshold to {cls.QBER_THRESHOLD*100:.1f}%")
            
            honest = input(f"Honest QBER % (current: {cls.HONEST_QBER*100:.2f}%): ").strip()
            if honest:
                cls.HONEST_QBER = float(honest) / 100
                print(f"✅ Set honest QBER to {cls.HONEST_QBER*100:.2f}%")
            
            method = input(f"Privacy amplification (xor/sha256, current: {cls.PRIVACY_AMPLIFICATION_METHOD}): ").strip()
            if method and method.lower() in ["xor", "sha256"]:
                cls.PRIVACY_AMPLIFICATION_METHOD = method.lower()
                print(f"✅ Set method to {cls.PRIVACY_AMPLIFICATION_METHOD}")
                
        except ValueError:
            print("❌ Invalid input. Keeping current values.")
    
    @classmethod
    def configure_attacks(cls):
        """Interactively configure which attacks to enable"""
        print("\n" + "-"*50)
        print("ATTACK SIMULATION CONFIGURATION")
        print("-"*50)
        
        pns = input(f"Enable PNS attack? (y/n, current: {'Yes' if cls.ENABLE_PNS_ATTACK else 'No'}): ").strip().lower()
        if pns in ['y', 'n']:
            cls.ENABLE_PNS_ATTACK = (pns == 'y')
            print(f"✅ PNS attack: {'Enabled' if cls.ENABLE_PNS_ATTACK else 'Disabled'}")
        
        intercept = input(f"Enable intercept-resend? (y/n, current: {'Yes' if cls.ENABLE_INTERCEPT_RESEND else 'No'}): ").strip().lower()
        if intercept in ['y', 'n']:
            cls.ENABLE_INTERCEPT_RESEND = (intercept == 'y')
            print(f"✅ Intercept-resend: {'Enabled' if cls.ENABLE_INTERCEPT_RESEND else 'Disabled'}")
        
        trojan = input(f"Enable trojan horse? (y/n, current: {'Yes' if cls.ENABLE_TROJAN_HORSE else 'No'}): ").strip().lower()
        if trojan in ['y', 'n']:
            cls.ENABLE_TROJAN_HORSE = (trojan == 'y')
            print(f"✅ Trojan horse: {'Enabled' if cls.ENABLE_TROJAN_HORSE else 'Disabled'}")
    
    @classmethod
    def save_config(cls, filename=None):
        """Save current configuration to file"""
        import json
        try:
            config_dict = {
                'NUM_QUBITS': cls.NUM_QUBITS,
                'NUM_BASES': cls.NUM_BASES,
                'MIN_NOISE': cls.MIN_NOISE,
                'MAX_NOISE': cls.MAX_NOISE,
                'NOISE_LEVELS': cls.NOISE_LEVELS,
                'MONTE_CARLO_RUNS': cls.MONTE_CARLO_RUNS,
                'STATISTICAL_RUNS': cls.STATISTICAL_RUNS,
                'QBER_THRESHOLD': cls.QBER_THRESHOLD,
                'HONEST_QBER': cls.HONEST_QBER,
                'PRIVACY_AMPLIFICATION_METHOD': cls.PRIVACY_AMPLIFICATION_METHOD,
                'PRIVACY_COMPRESSION_RATIO': cls.PRIVACY_COMPRESSION_RATIO,
                'ENABLE_PNS_ATTACK': cls.ENABLE_PNS_ATTACK,
                'ENABLE_INTERCEPT_RESEND': cls.ENABLE_INTERCEPT_RESEND,
                'ENABLE_TROJAN_HORSE': cls.ENABLE_TROJAN_HORSE,
                'VERBOSE_OUTPUT': cls.VERBOSE_OUTPUT,
            }
            if filename is None:
                filename = input("Filename (default: custom_config.json): ").strip() or "custom_config.json"
            with open(filename, 'w') as f:
                json.dump(config_dict, f, indent=2)
            print(f"✅ Configuration saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving config: {e}")
    
    @classmethod
    def load_config(cls, filename=None):
        """Load configuration from file"""
        import json
        try:
            if filename is None:
                filename = input("Filename (default: custom_config.json): ").strip() or "custom_config.json"
            with open(filename, 'r') as f:
                config_dict = json.load(f)
            
            for key, value in config_dict.items():
                if hasattr(cls, key):
                    setattr(cls, key, value)
            print(f"✅ Configuration loaded from {filename}")
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
        except Exception as e:
            print(f"❌ Error loading config: {e}")
