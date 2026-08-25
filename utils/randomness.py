import numpy as np

class RandomnessManager:
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)

    def random_bits(self, n):
        return self.rng.integers(0, 2, size=n)

    def random_bases(self, n):
        return self.rng.integers(0, 2, size=n)

    def biased_bases(self, n, bias):
        return self.rng.choice([0, 1], size=n, p=[bias, 1 - bias])
