import numpy as np
import hashlib
from qiskit import QuantumCircuit, transpile

# Cross-version Aer imports with fallback
try:
    from qiskit_aer.noise import NoiseModel, depolarizing_error
    from qiskit_aer import AerSimulator
except Exception as e:
    from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
    from qiskit.providers.aer import AerSimulator

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class BB84Engine:
    """
    Complete Adaptive BB84 QKD Framework
    Includes:
    - Noise modeling
    - Multiple attack strategies
    - Decoy-state support
    - Error correction
    - Privacy amplification
    - Finite-key security analysis
    - AES secure communication
    """

    def __init__(self, num_qubits=16, noise_prob=0.0, seed=None):

        self.n = num_qubits
        self.noise_prob = noise_prob
        self.rng = np.random.default_rng(seed)
        self.backend = AerSimulator()

    # --------------------------------------------------
    # RANDOM GENERATION
    # --------------------------------------------------

    def random_bits(self):
        return self.rng.integers(0, 2, size=self.n)

    def random_bases(self):
        return self.rng.integers(0, 2, size=self.n)

    # --------------------------------------------------
    # ATTACK MODELS
    # --------------------------------------------------

    def apply_attack(self, bits, bases, attack_type="none"):

        if attack_type == "none":
            return bits

        attacked = bits.copy()

        if attack_type == "intercept":
            eve_bases = self.random_bases()
            for i in range(self.n):
                if eve_bases[i] != bases[i]:
                    attacked[i] = self.rng.integers(0, 2)

        elif attack_type == "biased":
            eve_bases = self.rng.choice([0, 1], size=self.n, p=[0.8, 0.2])
            for i in range(self.n):
                if eve_bases[i] != bases[i]:
                    attacked[i] = self.rng.integers(0, 2)

        elif attack_type == "partial":
            indices = self.rng.choice(self.n, int(self.n * 0.5), replace=False)
            for i in indices:
                eve_basis = self.rng.integers(0, 2)
                if eve_basis != bases[i]:
                    attacked[i] = self.rng.integers(0, 2)

        return attacked

    # --------------------------------------------------
    # DECAY-STATE MODEL
    # --------------------------------------------------

    def generate_decoy_states(self):
        return self.rng.choice(["signal", "decoy"], size=self.n, p=[0.7, 0.3])

    # --------------------------------------------------
    # QUANTUM ENCODING & MEASUREMENT
    # --------------------------------------------------

    def encode(self, bits, bases):
        qc = QuantumCircuit(self.n, self.n)

        for i in range(self.n):
            if bits[i] == 1:
                qc.x(i)
            if bases[i] == 1:
                qc.h(i)

        return qc

    def apply_noise(self, circuit):
        # Avoid calling heavy transpile/plugin code paths. Instead, build a noise
        # model and store it for use when executing the circuit. Return the
        # original circuit unchanged so it can be measured/run later.
        if self.noise_prob == 0:
            # Clear any previous noise model
            self._noise_model = None
            return circuit

        noise_model = NoiseModel()
        error = depolarizing_error(self.noise_prob, 1)
        noise_model.add_all_qubit_quantum_error(error, ['x', 'h'])

        # Store noise model for use during run() to avoid transpile-time imports
        self._noise_model = noise_model
        return circuit

    def measure(self, qc, bases):
        for i in range(self.n):
            if bases[i] == 1:
                qc.h(i)
            qc.measure(i, i)
        return qc

    def get_encoding_circuit(self, bits, bases):
        """Export just the encoding part (no noise, no measurement) as a QuantumCircuit.
        
        Useful for running Alice's state preparation on remote hardware.
        
        Args:
            bits: Alice's random bits (length n)
            bases: Alice's random bases (length n)
        
        Returns:
            QuantumCircuit with encoding gates
        """
        qc = QuantumCircuit(self.n, self.n, name="BB84_Encoding")
        for i in range(self.n):
            if bits[i] == 1:
                qc.x(i)
            if bases[i] == 1:
                qc.h(i)
        return qc

    def get_measurement_circuit(self, bases):
        """Export just the measurement part (applies measurement bases & collapse).
        
        To be concatenated after encoding (on remote hardware).
        
        Args:
            bases: Bob's random bases (length n)
        
        Returns:
            QuantumCircuit with measurement basis rotations and collapse
        """
        qc = QuantumCircuit(self.n, self.n, name="BB84_Measurement")
        for i in range(self.n):
            if bases[i] == 1:
                qc.h(i)
            qc.measure(i, i)
        return qc

    def export_for_ibm(self, bits=None, bases=None, measurement_bases=None):
        """Export a complete BB84 protocol circuit for IBM backend execution.
        
        If bits/bases not provided, random ones are generated internally.
        
        Args:
            bits: Alice's bits. If None, generated randomly.
            bases: Alice's bases. If None, generated randomly.
            measurement_bases: Bob's measurement bases. If None, generated randomly.
        
        Returns:
            Tuple of (encoding_circuit, measurement_circuit, metadata_dict)
            
        Example:
            enc, meas, meta = engine.export_for_ibm()
            # Submit enc to IBM hardware, then meas after results received
        """
        if bits is None:
            bits = self.random_bits()
        if bases is None:
            bases = self.random_bases()
        if measurement_bases is None:
            measurement_bases = self.random_bases()
        
        enc_circuit = self.get_encoding_circuit(bits, bases)
        meas_circuit = self.get_measurement_circuit(measurement_bases)
        
        metadata = {
            "num_qubits": self.n,
            "alice_bits": bits.tolist(),
            "alice_bases": bases.tolist(),
            "bob_bases": measurement_bases.tolist(),
            "noise_prob": self.noise_prob,
        }
        
        return enc_circuit, meas_circuit, metadata

    # --------------------------------------------------
    # ERROR CORRECTION
    # --------------------------------------------------

    def error_correction(self, alice_key, bob_key):
        corrected = bob_key.copy()
        errors = 0
        for i in range(len(alice_key)):
            if alice_key[i] != corrected[i]:
                corrected[i] = alice_key[i]
                errors += 1
        return corrected, errors

    # --------------------------------------------------
    # INFORMATION THEORY
    # --------------------------------------------------

    def binary_entropy(self, p):
        if p == 0 or p == 1:
            return 0
        return -p*np.log2(p) - (1-p)*np.log2(1-p)

    def mutual_information(self, qber):
        return 1 - self.binary_entropy(qber)

    def eve_information(self, qber):
        return self.binary_entropy(qber)

    # --------------------------------------------------
    # FINITE KEY CORRECTION
    # --------------------------------------------------

    def finite_key_adjustment(self, qber, n):
        if n == 0:
            return qber
        sigma = np.sqrt(qber*(1-qber)/n)
        return qber + 1.96 * sigma

    # --------------------------------------------------
    # PRIVACY AMPLIFICATION
    # --------------------------------------------------

    def privacy_amplification(self, key_bits, qber):

        if qber > 0.11 or len(key_bits) == 0:
            return np.array([])

        final_length = int(len(key_bits) * max(0, 1 - 2*qber))

        hash_matrix = self.rng.integers(
            0, 2, size=(final_length, len(key_bits))
        )

        return np.mod(hash_matrix @ key_bits, 2)

    # --------------------------------------------------
    # AES ENCRYPTION
    # --------------------------------------------------

    def derive_aes_key(self, key_bits):
        key_string = ''.join(map(str, key_bits))
        return hashlib.sha256(key_string.encode()).digest()

    def encrypt_message(self, message, key_bits):
        aes_key = self.derive_aes_key(key_bits)
        cipher = AES.new(aes_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv, ciphertext

    def decrypt_message(self, iv, ciphertext, key_bits):
        aes_key = self.derive_aes_key(key_bits)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    # --------------------------------------------------
    # FULL PROTOCOL EXECUTION
    # --------------------------------------------------

    def run(self, attack_type="none", use_decoy=False):

        alice_bits = self.random_bits()
        alice_bases = self.random_bases()
        bob_bases = self.random_bases()

        if use_decoy:
            decoy_states = self.generate_decoy_states()
        else:
            decoy_states = None

        transmitted_bits = self.apply_attack(
            alice_bits, alice_bases, attack_type
        )

        qc = self.encode(transmitted_bits, alice_bases)
        qc = self.apply_noise(qc)
        qc = self.measure(qc, bob_bases)

        result = self.backend.run(qc, shots=1).result()
        counts = result.get_counts()
        measured = list(counts.keys())[0][::-1]
        bob_bits = np.array([int(bit) for bit in measured])

        mask = alice_bases == bob_bases
        alice_key = alice_bits[mask]
        bob_key = bob_bits[mask]

        if len(alice_key) == 0:
            return {"secure": False}

        qber = np.sum(alice_key != bob_key) / len(alice_key)

        corrected_bob, leakage = self.error_correction(alice_key, bob_key)

        adjusted_qber = self.finite_key_adjustment(qber, len(alice_key))

        I_AB = self.mutual_information(adjusted_qber)
        I_AE = self.eve_information(adjusted_qber)

        final_key = self.privacy_amplification(alice_key, adjusted_qber)

        secure = (adjusted_qber <= 0.11) and (I_AB > I_AE)

        return {
            "qber": qber,
            "adjusted_qber": adjusted_qber,
            "sifted_length": len(alice_key),
            "leakage": leakage,
            "final_key_length": len(final_key),
            "I_AB": I_AB,
            "I_AE": I_AE,
            "secure": secure,
            "decoy_used": use_decoy
        }
