#include <iostream>
#include <numeric> // For std::gcd
#include <cmath>   // For std::pow or custom power function

// Function to compute (base^expo) % m
long long power(long long base, long long expo, long long m) {
    long long res = 1;
    base %= m;
    while (expo > 0) {
        if (expo % 2 == 1) { // If expo is odd
            res = (res * base) % m;
        }
        base = (base * base) % m;
        expo /= 2;
    }
    return res;
}

// Function to find modular inverse of e modulo phi (d such that (e * d) % phi == 1)
long long modInverse(long long e, long long phi) {
    for (long long d = 2; d < phi; d++) {
        if ((e * d) % phi == 1) {
            return d;
        }
    }
    return -1; // Should not happen with valid inputs
}

// RSA Key Generation
void generateKeys(long long& p, long long& q, long long& e, long long& d, long long& n) {
    // Choose two distinct prime numbers (for simplicity, hardcoded small primes)
    p = 13; // Example prime 1
    q = 11; // Example prime 2

    n = p * q; // Calculate n

    long long phi = (p - 1) * (q - 1); // Calculate Euler's totient function

    // Choose e such that 1 < e < phi and gcd(e, phi) == 1
    for (e = 2; e < phi; e++) {
        if (std::gcd(e, phi) == 1) {
            break;
        }
    }

    // Compute d such that (e * d) % phi == 1
    d = modInverse(e, phi);
}

// Encrypt message using public key (e, n)
long long encrypt(long long message, long long e, long long n) {
    return power(message, e, n);
}

// Decrypt message using private key (d, n)
long long decrypt(long long ciphertext, long long d, long long n) {
    return power(ciphertext, d, n);
}

int main() {
    long long p, q, e, d, n;

    // Key Generation
    generateKeys(p, q, e, d, n);

    std::cout << "Prime p: " << p << std::endl;
    std::cout << "Prime q: " << q << std::endl;
    std::cout << "Modulus n (p * q): " << n << std::endl;
    std::cout << "Public Key (e, n): (" << e << ", " << n << ")" << std::endl;
    std::cout << "Private Key (d, n): (" << d << ", " << n << ")" << std::endl;

    // Message to be encrypted
    long long originalMessage = 123;
    std::cout << "\nOriginal Message: " << originalMessage << std::endl;

    // Encrypt the message
    long long encryptedMessage = encrypt(originalMessage, e, n);
    std::cout << "Encrypted Message: " << encryptedMessage << std::endl;

    // Decrypt the message
    long long decryptedMessage = decrypt(encryptedMessage, d, n);
    std::cout << "Decrypted Message: " << decryptedMessage << std::endl;

    return 0;
}
