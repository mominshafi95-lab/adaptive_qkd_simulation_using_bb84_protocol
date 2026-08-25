import numpy as np

def sift_keys(a_bits, b_bits, a_bases, b_bases):
    mask = a_bases == b_bases
    return a_bits[mask], b_bits[mask]

def calculate_qber(a_key, b_key):
    if len(a_key) == 0:
        return 0
    return np.sum(a_key != b_key) / len(a_key)

def secure_key_rate(qber):
    if qber > 0.11:
        return 0
    return max(0, 1 - 2*qber)
