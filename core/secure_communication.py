from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib

class SecureCommunication:

    def derive_aes_key(self, qkd_key_bits):
        key_string = ''.join(map(str, qkd_key_bits))
        return hashlib.sha256(key_string.encode()).digest()

    def encrypt(self, message, aes_key):
        cipher = AES.new(aes_key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv, ct_bytes

    def decrypt(self, iv, ciphertext, aes_key):
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return pt.decode()
