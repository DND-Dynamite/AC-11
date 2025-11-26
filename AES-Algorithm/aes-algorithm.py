import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class AESCipher:
    def __init__(self):
        # AES block size is always 128 bits (16 bytes)
        self.block_size = 128
        self.backend = default_backend()

    def generate_key(self):
        """
        Generates a secure random 32-byte (256-bit) key.
        Save this key securely! If you lose it, you cannot decrypt the data.
        """
        return os.urandom(32)

    def encrypt(self, plaintext, key):
        """
        Encrypts text using AES-256-CBC.
        """
        # 1. Generate a random Initialization Vector (IV)
        # The IV must be random for every encryption but doesn't need to be secret.
        iv = os.urandom(16)

        # 2. Pad the data
        # AES blocks must be 128 bits. If the text isn't a multiple of 16 bytes,
        # we add padding using PKCS7 standard.
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        # 3. Create the Cipher object
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # 4. Encrypt data
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Return the IV prepended to the ciphertext (needed for decryption)
        return iv + ciphertext

    def decrypt(self, encrypted_data, key):
        """
        Decrypts bytes using AES-256-CBC.
        """
        # 1. Extract the IV (first 16 bytes) and the actual ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        # 2. Create the Cipher object
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        # 3. Decrypt the data
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # 4. Remove padding
        unpadder = padding.PKCS7(self.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode('utf-8')

# --- Main execution block to demonstrate usage ---
if __name__ == "__main__":
    # Initialize our helper class
    aes = AESCipher()

    print("--- AES-256 Encryption Demo ---")

    # 1. Generate a Key
    secret_key = aes.generate_key()
    print(f"Generated Key (Hex): {secret_key.hex()}")

    # 2. Define a message
    original_text = "This is a secret message! 🔒"
    print(f"Original Text: {original_text}")

    # 3. Encrypt
    encrypted_bytes = aes.encrypt(original_text, secret_key)
    print(f"Encrypted (Hex): {encrypted_bytes.hex()}")

    # 4. Decrypt
    try:
        decrypted_text = aes.decrypt(encrypted_bytes, secret_key)
        print(f"Decrypted Text: {decrypted_text}")
    except ValueError as e:
        print("Decryption failed. Invalid key or corrupted data.")

    # 5. Proof that changing the key fails decryption
    print("\n--- Testing Invalid Key ---")
    wrong_key = aes.generate_key()
    try:
        aes.decrypt(encrypted_bytes, wrong_key)
    except Exception:
        print("Success: Decryption failed with the wrong key as expected.")