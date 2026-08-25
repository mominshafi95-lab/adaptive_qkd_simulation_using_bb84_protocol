import numpy as np
from core.bb84_engine import BB84Engine
from utils.visualization import plot_bar

def run_attack_analysis():

    attack_types = ["none", "intercept", "biased", "partial"]
    results = {}

    for attack in attack_types:
        qbers = []

        for _ in range(100):
            engine = BB84Engine(8)
            # Use engine.run() with attack_type parameter
            result = engine.run(attack_type=attack)
            # Skip if no sifted key was generated (qber key missing)
            if "qber" in result:
                qbers.append(result["qber"])

        results[attack] = np.mean(qbers) if qbers else 0.0

    plot_bar(results.keys(), results.values(),
             "Attack Type", "Average QBER",
             "Impact of Attack Type on QBER")

    for k, v in results.items():
        print(k, ":", v)
