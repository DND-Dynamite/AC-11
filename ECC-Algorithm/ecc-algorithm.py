import random
import hashlib
from typing import Tuple, Optional

class EllipticCurve:
    """
    Represents an elliptic curve in the form: y^2 = x^3 + ax + b (mod p)
    """
    def __init__(self, a: int, b: int, p: int, order: int = None, generator: Tuple[int, int] = None):
        self.a = a
        self.b = b
        self.p = p
        self.order = order  # Order of the curve (number of points)
        self.generator = generator  # Generator point
        
        # Verify the curve parameters
        discriminant = (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p
        if discriminant == 0:
            raise ValueError("Invalid curve parameters: discriminant is zero")

    def is_on_curve(self, point: Tuple[int, int]) -> bool:
        """
        Check if a point lies on the curve
        """
        if point is None:
            return True  # Point at infinity
        
        x, y = point
        left_side = (y * y) % self.p
        right_side = (pow(x, 3, self.p) + self.a * x + self.b) % self.p
        return left_side == right_side

    def point_add(self, P1: Tuple[int, int], P2: Tuple[int, int]) -> Tuple[int, int]:
        """
        Add two points on the elliptic curve
        """
        if P1 is None:
            return P2
        if P2 is None:
            return P1
        
        x1, y1 = P1
        x2, y2 = P2
        
        if x1 == x2:
            if y1 == y2:
                # Point doubling
                return self.point_double(P1)
            else:
                # Points are inverses of each other
                return None
        
        # Calculate slope
        numerator = (y2 - y1) % self.p
        denominator = (x2 - x1) % self.p
        denominator_inv = pow(denominator, self.p - 2, self.p)  # Modular inverse
        slope = (numerator * denominator_inv) % self.p
        
        # Calculate resulting point
        x3 = (slope * slope - x1 - x2) % self.p
        y3 = (slope * (x1 - x3) - y1) % self.p
        
        result = (x3, y3)
        if not self.is_on_curve(result):
            raise ValueError("Point addition resulted in invalid point")
        
        return result

    def point_double(self, P: Tuple[int, int]) -> Tuple[int, int]:
        """
        Double a point on the elliptic curve (P + P)
        """
        if P is None:
            return None
        
        x, y = P
        
        # Calculate slope for point doubling
        numerator = (3 * x * x + self.a) % self.p
        denominator = (2 * y) % self.p
        denominator_inv = pow(denominator, self.p - 2, self.p)  # Modular inverse
        slope = (numerator * denominator_inv) % self.p
        
        # Calculate resulting point
        x3 = (slope * slope - 2 * x) % self.p
        y3 = (slope * (x - x3) - y) % self.p
        
        result = (x3, y3)
        if not self.is_on_curve(result):
            raise ValueError("Point doubling resulted in invalid point")
        
        return result

    def scalar_multiply(self, k: int, P: Tuple[int, int]) -> Tuple[int, int]:
        """
        Multiply a point by a scalar using double-and-add algorithm
        """
        if k % self.p == 0 or P is None:
            return None
        
        if k < 0:
            # k * P = (-k) * (-P)
            return self.scalar_multiply(-k, self.point_negate(P))
        
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1
        
        return result

    def point_negate(self, P: Tuple[int, int]) -> Tuple[int, int]:
        """
        Negate a point (find its inverse)
        """
        if P is None:
            return None
        x, y = P
        return (x, (-y) % self.p)

class ECC:
    """
    Elliptic Curve Cryptography implementation
    """
    
    # Common standardized curves
    
    # secp256k1 (used in Bitcoin)
    SECP256K1 = EllipticCurve(
        a=0,
        b=7,
        p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
        order=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
        generator=(
            0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        )
    )
    
    # NIST P-256
    NIST_P256 = EllipticCurve(
        a=-3,
        b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B,
        p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF,
        order=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551,
        generator=(
            0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
            0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
        )
    )
    
    def __init__(self, curve: EllipticCurve = SECP256K1):
        self.curve = curve
        self.G = curve.generator  # Generator point
    
    def generate_key_pair(self) -> Tuple[int, Tuple[int, int]]:
        """
        Generate a private-public key pair
        Returns: (private_key, public_key)
        """
        # Private key: random number in [1, order-1]
        private_key = random.randint(1, self.curve.order - 1)
        
        # Public key: private_key * G
        public_key = self.curve.scalar_multiply(private_key, self.G)
        
        return private_key, public_key
    
    def ecdh(self, private_key: int, other_public_key: Tuple[int, int]) -> Tuple[int, int]:
        """
        Elliptic Curve Diffie-Hellman key exchange
        Returns shared secret point
        """
        if not self.curve.is_on_curve(other_public_key):
            raise ValueError("Other public key is not on the curve")
        
        shared_secret = self.curve.scalar_multiply(private_key, other_public_key)
        return shared_secret
    
    def ecdsa_sign(self, private_key: int, message: bytes) -> Tuple[int, int]:
        """
        ECDSA signature generation
        Returns: (r, s)
        """
        # Hash the message
        message_hash = int.from_bytes(hashlib.sha256(message).digest(), 'big')
        message_hash = message_hash % self.curve.order
        
        while True:
            # Generate random k
            k = random.randint(1, self.curve.order - 1)
            
            # Calculate r = (k * G).x mod order
            R = self.curve.scalar_multiply(k, self.G)
            r = R[0] % self.curve.order
            
            if r == 0:
                continue
            
            # Calculate s = k^(-1) * (hash + r * private_key) mod order
            k_inv = pow(k, self.curve.order - 2, self.curve.order)
            s = (k_inv * (message_hash + r * private_key)) % self.curve.order
            
            if s == 0:
                continue
            
            return (r, s)
    
    def ecdsa_verify(self, public_key: Tuple[int, int], message: bytes, signature: Tuple[int, int]) -> bool:
        """
        ECDSA signature verification
        Returns: True if signature is valid, False otherwise
        """
        r, s = signature
        
        # Verify signature components
        if not (1 <= r < self.curve.order and 1 <= s < self.curve.order):
            return False
        
        # Hash the message
        message_hash = int.from_bytes(hashlib.sha256(message).digest(), 'big')
        message_hash = message_hash % self.curve.order
        
        # Calculate w = s^(-1) mod order
        w = pow(s, self.curve.order - 2, self.curve.order)
        
        # Calculate u1 and u2
        u1 = (message_hash * w) % self.curve.order
        u2 = (r * w) % self.curve.order
        
        # Calculate point = u1 * G + u2 * public_key
        point1 = self.curve.scalar_multiply(u1, self.G)
        point2 = self.curve.scalar_multiply(u2, public_key)
        point = self.curve.point_add(point1, point2)
        
        if point is None:
            return False
        
        # Verify r == point.x mod order
        return r == point[0] % self.curve.order
    
    def encrypt_message(self, public_key: Tuple[int, int], message: str) -> dict:
        """
        Simple ECC encryption (for demonstration purposes)
        In practice, use hybrid encryption with ECC for key exchange and symmetric encryption for data
        """
        # Generate ephemeral key pair
        ephemeral_private, ephemeral_public = self.generate_key_pair()
        
        # Calculate shared secret
        shared_secret_point = self.ecdh(ephemeral_private, public_key)
        shared_secret = shared_secret_point[0]  # Use x-coordinate as shared secret
        
        # Simple XOR encryption (for demonstration - use proper AEAD in practice)
        message_bytes = message.encode('utf-8')
        key = hashlib.sha256(str(shared_secret).encode()).digest()
        
        encrypted = bytearray()
        for i, byte in enumerate(message_bytes):
            encrypted.append(byte ^ key[i % len(key)])
        
        return {
            'ephemeral_public_key': ephemeral_public,
            'encrypted_message': bytes(encrypted)
        }
    
    def decrypt_message(self, private_key: int, encrypted_data: dict) -> str:
        """
        Simple ECC decryption
        """
        ephemeral_public_key = encrypted_data['ephemeral_public_key']
        encrypted_message = encrypted_data['encrypted_message']
        
        # Calculate shared secret
        shared_secret_point = self.ecdh(private_key, ephemeral_public_key)
        shared_secret = shared_secret_point[0]  # Use x-coordinate as shared secret
        
        # Decrypt
        key = hashlib.sha256(str(shared_secret).encode()).digest()
        
        decrypted = bytearray()
        for i, byte in enumerate(encrypted_message):
            decrypted.append(byte ^ key[i % len(key)])
        
        return decrypted.decode('utf-8')

def main():
    """
    Demonstration of ECC operations
    """
    print("Elliptic Curve Cryptography Implementation")
    print("=" * 50)
    
    # Initialize ECC with secp256k1 curve
    ecc = ECC(ECC.SECP256K1)
    
    # Generate key pairs for Alice and Bob
    print("1. Key Generation")
    alice_private, alice_public = ecc.generate_key_pair()
    bob_private, bob_public = ecc.generate_key_pair()
    
    print(f"Alice's private key: {hex(alice_private)[:20]}...")
    print(f"Alice's public key: ({hex(alice_public[0])[:20]}..., {hex(alice_public[1])[:20]}...)")
    print(f"Bob's private key: {hex(bob_private)[:20]}...")
    print(f"Bob's public key: ({hex(bob_public[0])[:20]}..., {hex(bob_public[1])[:20]}...)")
    print()
    
    # ECDH Key Exchange
    print("2. ECDH Key Exchange")
    alice_shared = ecc.ecdh(alice_private, bob_public)
    bob_shared = ecc.ecdh(bob_private, alice_public)
    
    print(f"Alice's shared secret: ({hex(alice_shared[0])[:20]}..., {hex(alice_shared[1])[:20]}...)")
    print(f"Bob's shared secret: ({hex(bob_shared[0])[:20]}..., {hex(bob_shared[1])[:20]}...)")
    print(f"Shared secrets match: {alice_shared == bob_shared}")
    print()
    
    # ECDSA Signatures
    print("3. ECDSA Signatures")
    message = b"Hello, ECC World!"
    signature = ecc.ecdsa_sign(alice_private, message)
    
    print(f"Message: {message.decode()}")
    print(f"Signature r: {hex(signature[0])[:20]}...")
    print(f"Signature s: {hex(signature[1])[:20]}...")
    
    # Verify signature
    is_valid = ecc.ecdsa_verify(alice_public, message, signature)
    print(f"Signature valid: {is_valid}")
    
    # Test with wrong message
    wrong_message = b"Wrong message"
    is_valid_wrong = ecc.ecdsa_verify(alice_public, wrong_message, signature)
    print(f"Signature valid for wrong message: {is_valid_wrong}")
    print()
    
    # Encryption/Decryption demo
    print("4. Encryption/Decryption Demo")
    plaintext = "Secret message for Bob"
    print(f"Original message: {plaintext}")
    
    # Bob encrypts message for Alice
    encrypted_data = ecc.encrypt_message(alice_public, plaintext)
    print(f"Encrypted message length: {len(encrypted_data['encrypted_message'])} bytes")
    
    # Alice decrypts the message
    decrypted_text = ecc.decrypt_message(alice_private, encrypted_data)
    print(f"Decrypted message: {decrypted_text}")
    print(f"Decryption successful: {plaintext == decrypted_text}")

if __name__ == "__main__":
    main()