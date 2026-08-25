import numpy as np

def finite_key_correction(qber, n, confidence=1.96):
    """
    Apply finite-key statistical penalty.
    """
    if n == 0:
        return qber

    sigma = np.sqrt(qber*(1-qber)/n)
    return qber + confidence * sigma
