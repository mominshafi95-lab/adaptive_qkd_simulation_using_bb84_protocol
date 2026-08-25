import numpy as np
import hashlib

class PrivacyAmplifier:
    """
    Implements privacy amplification using
    universal hashing and QBER-based compression.
    """

    def __init__(self, rng):
        self.rng = rng

    def compute_final_length(self, sifted_length, qber):
        """
        Compute final secure key length.
        """
        if qber > 0.11:
            return 0

        return int(sifted_length * max(0, 1 - 2*qber))

    def universal_hash(self, key_bits, final_length):
        """
        Universal hash via random binary matrix multiplication.
        """

        if final_length == 0 or len(key_bits) == 0:
            return np.array([])

        key = np.array(key_bits)
        n = len(key)

        # Random binary matrix
        hash_matrix = self.rng.rng.integers(
            0, 2, size=(final_length, n)
        )

        compressed = np.mod(hash_matrix @ key, 2)

        return compressed

    def sha256_hash(self, key_bits, final_length):
        """
        Alternative hash using SHA-256
        """
        if final_length == 0 or len(key_bits) == 0:
            return ""

        key_string = ''.join(map(str, key_bits))
        digest = hashlib.sha256(key_string.encode()).hexdigest()

        # Convert hex to binary
        binary = bin(int(digest, 16))[2:].zfill(256)

        return binary[:final_length]
