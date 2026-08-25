from core.information_theory import mutual_information_ab, eve_information_estimate
from core.finite_key import finite_key_correction

class SecurityAnalyzer:

    def analyze(self, qber, sifted_length):

        adjusted_qber = finite_key_correction(qber, sifted_length)

        i_ab = mutual_information_ab(adjusted_qber)
        i_ae = eve_information_estimate(adjusted_qber)

        secure = (adjusted_qber <= 0.11) and (i_ab > i_ae)

        return {
            "adjusted_qber": adjusted_qber,
            "I_AB": i_ab,
            "I_AE": i_ae,
            "secure": secure
        }
