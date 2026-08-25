from experiments.noise_sweep import run_noise_sweep
from experiments.monte_carlo import run_monte_carlo
from experiments.attack_analysis import run_attack_analysis
from experiments.security_deep_dive import run_security_deep_dive
from experiments.error_correction_demo import run_error_correction_demo
from experiments.decoy_state_demo import run_decoy_state_demo
from experiments.privacy_amplification_demo import run_privacy_amplification_demo
from experiments.secure_communication_demo import run_secure_communication_demo
from experiments.advanced_attack_demo import run_advanced_attack_analysis
from experiments.randomness_analysis import run_randomness_analysis
from experiments.statistical_analysis import run_statistical_analysis
from config import ExperimentConfig

def show_startup_menu():
    """Show startup configuration menu"""
    print("\n" + "="*70)
    print("BB84 QKD FRAMEWORK - STARTUP OPTIONS")
    print("="*70)
    print("\n1. Configure Experiment Parameters")
    print("2. View Current Configuration")
    print("3. Load Saved Configuration")
    print("4. Skip Configuration")
    print("0. Exit Program\n")
    
    choice = input("Select option (0-4): ").strip()
    
    if choice == "1":
        ExperimentConfig.interactive_configuration()
    elif choice == "2":
        ExperimentConfig.print_current_config()
        input("\nPress Enter to continue...")
        show_startup_menu()
    elif choice == "3":
        ExperimentConfig.load_config()
        input("\nPress Enter to continue...")
        show_startup_menu()
    elif choice == "4":
        print("\nUsing default configuration")
    elif choice == "0":
        print("\nGoodbye!")
        exit()
    else:
        print("\nInvalid option. Try again.")
        show_startup_menu()

def main():
    show_startup_menu()
    
    while True:
        print("\n" + "="*70)
        print("BB84 QKD FRAMEWORK")
        print("="*70)
        print(f"\nCurrent: {ExperimentConfig.NUM_QUBITS} qubits, {ExperimentConfig.MIN_NOISE*100:.1f}%-{ExperimentConfig.MAX_NOISE*100:.1f}% noise, {ExperimentConfig.NOISE_LEVELS} levels")
        
        print("\n[EXPERIMENTS]")
        print("1.  Noise Sweep")
        print("2.  Monte Carlo")
        print("3.  Attack Analysis")
        print("4.  Security Deep Dive")
        print("5.  Error Correction")
        print("6.  Decoy State")
        print("7.  Privacy Amplification")
        print("8.  Secure Communication")
        print("9.  Advanced Attacks")
        print("10. Randomness Analysis")
        print("11. Statistical Analysis")
        
        print("\n[CONTROL]")
        print("12. Reconfigure")
        print("13. View Config")
        print("0.  Exit")
        
        print("\n" + "-"*70)
        choice = input("Select (0-13): ").strip()

        if choice == "1":
            run_noise_sweep()
        elif choice == "2":
            run_monte_carlo()
        elif choice == "3":
            run_attack_analysis()
        elif choice == "4":
            run_security_deep_dive()
        elif choice == "5":
            run_error_correction_demo()
        elif choice == "6":
            run_decoy_state_demo()
        elif choice == "7":
            run_privacy_amplification_demo()
        elif choice == "8":
            run_secure_communication_demo()
        elif choice == "9":
            run_advanced_attack_analysis()
        elif choice == "10":
            run_randomness_analysis()
        elif choice == "11":
            run_statistical_analysis()
        elif choice == "12":
            ExperimentConfig.interactive_configuration()
        elif choice == "13":
            ExperimentConfig.print_current_config()
        elif choice == "0":
            print("\nGoodbye!\n")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    import sys
    # CLI flags to control automatic plot saving
    if "--no-plots" in sys.argv:
        ExperimentConfig.SAVE_PLOTS = False
    if "--save-plots" in sys.argv:
        ExperimentConfig.SAVE_PLOTS = True
    main()
