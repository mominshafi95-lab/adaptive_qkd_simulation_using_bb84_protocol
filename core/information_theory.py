import numpy as np

def binary_entropy(p):
    if p == 0 or p == 1:
        return 0
    return -p*np.log2(p) - (1-p)*np.log2(1-p)

def mutual_information_ab(qber):
    return 1 - binary_entropy(qber)

def eve_information_estimate(qber):
    """
    Upper bound on Eve information under intercept-resend.
    """
    return binary_entropy(qber)
