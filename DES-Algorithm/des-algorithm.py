import binascii

class DES:
    # Initial Permutation Table
    IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    # Final Permutation Table (Inverse of Initial Permutation)
    FP = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

    # Expansion Table
    E = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

    # S-boxes
    S_BOX = [
        # S1
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        # S2
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        # S3
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        # S4
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        # S5
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        # S6
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        # S7
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        # S8
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]

    # Permutation Table
    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

    # PC-1 Table (Key Permutation)
    PC1 = [57, 49, 41, 33, 25, 17, 9,
           1, 58, 50, 42, 34, 26, 18,
           10, 2, 59, 51, 43, 35, 27,
           19, 11, 3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15,
           7, 62, 54, 46, 38, 30, 22,
           14, 6, 61, 53, 45, 37, 29,
           21, 13, 5, 28, 20, 12, 4]

    # PC-2 Table (Compression Permutation)
    PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
           15, 6, 21, 10, 23, 19, 12, 4,
           26, 8, 16, 7, 27, 20, 13, 2,
           41, 52, 31, 37, 47, 55, 30, 40,
           51, 45, 33, 48, 44, 49, 39, 56,
           34, 53, 46, 42, 50, 36, 29, 32]

    # Shift Table
    SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def __init__(self, key):
        self.key = key
        self.subkeys = self.generate_subkeys()

    def string_to_bit_array(self, text):
        """Convert a string to a list of bits"""
        array = []
        for char in text:
            binval = self.bin_value(char, 8)
            array.extend([int(x) for x in list(binval)])
        return array

    def bit_array_to_string(self, array):
        """Convert a list of bits to a string"""
        res = []
        for i in range(0, len(array), 8):
            byte = array[i:i+8]
            res.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(res)

    def bin_value(self, val, bitsize):
        """Return the binary value as a string of given bitsize"""
        binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
        if len(binval) > bitsize:
            raise ValueError("Binary value larger than the expected size")
        while len(binval) < bitsize:
            binval = "0" + binval
        return binval

    def permute(self, block, table):
        """Permute the given block using the specified table"""
        return [block[x-1] for x in table]

    def left_shift(self, key, n):
        """Left shift the given key by n positions"""
        return key[n:] + key[:n]

    def generate_subkeys(self):
        """Generate the 16 subkeys for DES"""
        # Convert key to bit array
        key = self.string_to_bit_array(self.key)
        
        # Apply PC-1 permutation
        key = self.permute(key, self.PC1)
        
        # Split into left and right halves
        left = key[:28]
        right = key[28:]
        
        subkeys = []
        
        # Generate 16 subkeys
        for i in range(16):
            # Shift left and right halves
            left = self.left_shift(left, self.SHIFT[i])
            right = self.left_shift(right, self.SHIFT[i])
            
            # Combine halves
            combined = left + right
            
            # Apply PC-2 permutation to get subkey
            subkey = self.permute(combined, self.PC2)
            subkeys.append(subkey)
            
        return subkeys

    def xor(self, a, b):
        """XOR two lists of bits"""
        return [x ^ y for x, y in zip(a, b)]

    def f_function(self, right, subkey):
        """The F function used in each round of DES"""
        # Expansion permutation
        expanded = self.permute(right, self.E)
        
        # XOR with subkey
        xored = self.xor(expanded, subkey)
        
        # S-box substitution
        sbox_output = []
        for i in range(8):
            # Get 6 bits for this S-box
            chunk = xored[i*6:(i+1)*6]
            row = (chunk[0] << 1) + chunk[5]
            col = (chunk[1] << 3) + (chunk[2] << 2) + (chunk[3] << 1) + chunk[4]
            val = self.S_BOX[i][row][col]
            
            # Convert to 4-bit binary
            sbox_output.extend([int(x) for x in self.bin_value(val, 4)])
        
        # Permutation
        return self.permute(sbox_output, self.P)

    def encrypt_block(self, block):
        """Encrypt a single 64-bit block"""
        # Convert block to bit array
        block = self.string_to_bit_array(block)
        
        # Initial permutation
        block = self.permute(block, self.IP)
        
        # Split into left and right halves
        left = block[:32]
        right = block[32:]
        
        # 16 rounds of Feistel network
        for i in range(16):
            # Save previous left
            previous_left = left.copy()
            
            # Current left becomes previous right
            left = right
            
            # F function applied to right and XORed with previous left
            right = self.xor(previous_left, self.f_function(right, self.subkeys[i]))
        
        # Final swap and permutation
        combined = right + left
        cipher_block = self.permute(combined, self.FP)
        
        # Convert back to string
        return self.bit_array_to_string(cipher_block)

    def decrypt_block(self, block):
        """Decrypt a single 64-bit block"""
        # Convert block to bit array
        block = self.string_to_bit_array(block)
        
        # Initial permutation
        block = self.permute(block, self.IP)
        
        # Split into left and right halves
        left = block[:32]
        right = block[32:]
        
        # 16 rounds of Feistel network (in reverse order)
        for i in range(15, -1, -1):
            # Save previous left
            previous_left = left.copy()
            
            # Current left becomes previous right
            left = right
            
            # F function applied to right and XORed with previous left
            right = self.xor(previous_left, self.f_function(right, self.subkeys[i]))
        
        # Final swap and permutation
        combined = right + left
        plain_block = self.permute(combined, self.FP)
        
        # Convert back to string
        return self.bit_array_to_string(plain_block)

    def pad(self, text):
        """PKCS5 padding"""
        pad_length = 8 - (len(text) % 8)
        return text + chr(pad_length) * pad_length

    def unpad(self, text):
        """Remove PKCS5 padding"""
        pad_length = ord(text[-1])
        return text[:-pad_length]

    def encrypt(self, plaintext):
        """Encrypt plaintext using DES"""
        # Pad the plaintext
        plaintext = self.pad(plaintext)
        
        # Encrypt each 8-byte block
        ciphertext = []
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            ciphertext.append(self.encrypt_block(block))
        
        return ''.join(ciphertext)

    def decrypt(self, ciphertext):
        """Decrypt ciphertext using DES"""
        # Decrypt each 8-byte block
        plaintext = []
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            plaintext.append(self.decrypt_block(block))
        
        # Remove padding
        return self.unpad(''.join(plaintext))

# Example usage and testing
def main():
    # Test with a sample key and plaintext
    key = "12345678"  # 8-byte key
    plaintext = "Hello DES! This is a test message."
    
    print("Original Text:", plaintext)
    print("Key:", key)
    
    # Create DES instance
    des = DES(key)
    
    # Encrypt
    ciphertext = des.encrypt(plaintext)
    print("Ciphertext (hex):", binascii.hexlify(ciphertext.encode()).decode())
    
    # Decrypt
    decrypted = des.decrypt(ciphertext)
    print("Decrypted Text:", decrypted)
    
    # Verify
    print("Encryption/Decryption Successful:", plaintext == decrypted)

if __name__ == "__main__":
    main()