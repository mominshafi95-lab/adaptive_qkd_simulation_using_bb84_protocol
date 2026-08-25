import numpy as np

class DecoyStateBB84:
    """
    Implements a simplified decoy-state mechanism.
    """

    def __init__(self, rng):
        self.rng = rng

    def generate_states(self, n, signal_prob=0.7):
        """
        Generates signal and decoy states.
        """
        states = self.rng.rng.choice(
            ["signal", "decoy"],
            size=n,
            p=[signal_prob, 1 - signal_prob]
        )
        return states

    def estimate_channel_loss(self, detection_results, states):
        """
        Compare signal vs decoy detection rates.
        """
        signal_detect = np.sum((states == "signal") & (detection_results == 1))
        decoy_detect = np.sum((states == "decoy") & (detection_results == 1))

        return {
            "signal_rate": signal_detect / max(1, np.sum(states == "signal")),
            "decoy_rate": decoy_detect / max(1, np.sum(states == "decoy"))
        }
