import numpy as np

class AttackEngine:

    def __init__(self, rng):
        self.rng = rng

    def intercept_resend(self, bits, bases):
        eve_bases = self.rng.random_bases(len(bits))
        eve_bits = np.zeros(len(bits), dtype=int)

        for i in range(len(bits)):
            if eve_bases[i] == bases[i]:
                eve_bits[i] = bits[i]
            else:
                eve_bits[i] = self.rng.random_bits(1)[0]

        return eve_bits

    def biased_basis_attack(self, bits, bases, bias=0.7):
        eve_bases = self.rng.biased_bases(len(bits), bias)
        eve_bits = np.zeros(len(bits), dtype=int)

        for i in range(len(bits)):
            if eve_bases[i] == bases[i]:
                eve_bits[i] = bits[i]
            else:
                eve_bits[i] = self.rng.random_bits(1)[0]

        return eve_bits

    def partial_interception(self, bits, bases, fraction=0.5):
        n = len(bits)
        eve_bits = bits.copy()
        indices = self.rng.rng.choice(n, int(n*fraction), replace=False)

        for i in indices:
            eve_basis = self.rng.random_bits(1)[0]
            if eve_basis != bases[i]:
                eve_bits[i] = self.rng.random_bits(1)[0]

        return eve_bits
