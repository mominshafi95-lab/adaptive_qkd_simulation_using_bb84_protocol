import numpy as np

class ErrorCorrector:
    """
    Simplified parity-based error correction model.
    """

    def reconcile(self, alice_key, bob_key):

        if len(alice_key) == 0:
            return alice_key, bob_key, 0

        corrected_bob = bob_key.copy()
        error_count = 0

        for i in range(len(alice_key)):
            if alice_key[i] != corrected_bob[i]:
                corrected_bob[i] = alice_key[i]
                error_count += 1

        leakage = error_count  # Bits revealed during correction

        return alice_key, corrected_bob, leakage
