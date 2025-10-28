# Function for Modular Exponentiation: (base^exp) % mod
# Python's built-in pow() function handles this efficiently and securely
# for large numbers, using an optimized algorithm.
def power(base, exp, mod):
    return pow(base, exp, mod)

def diffie_hellman():
    # 1. Public Agreement (Shared Parameters)
    # In a real-world scenario, p and g would be extremely large prime numbers.
    p = 23  # A large prime number (modulus)
    g = 5   # A primitive root/generator

    print("--- Diffie-Hellman Key Exchange ---")
    print(f"Publicly agreed parameters: p={p}, g={g}")
    print("-" * 34)

    # --- Alice's Side ---
    # 2. Private Key Selection
    a_private = 6  # Alice's secret private key
    print(f"Alice's Private Key (a): {a_private}")

    # 3. Public Key Calculation (A = g^a mod p)
    A_public = power(g, a_private, p)
    print(f"Alice's Public Key (A): {A_public}")

    # --- Bob's Side ---
    # 2. Private Key Selection
    b_private = 15 # Bob's secret private key
    print(f"Bob's Private Key (b): {b_private}")

    # 3. Public Key Calculation (B = g^b mod p)
    B_public = power(g, b_private, p)
    print(f"Bob's Public Key (B): {B_public}")
    print("-" * 34)

    # **Exchange of Public Keys (A and B occurs here)**
    print(f"**Exchange: Alice sends A={A_public} to Bob. Bob sends B={B_public} to Alice.**")
    print("-" * 34)

    # 4. Shared Secret Calculation

    # Alice calculates Shared Secret (S1 = B^a mod p)
    S1_shared_secret = power(B_public, a_private, p)

    # Bob calculates Shared Secret (S2 = A^b mod p)
    S2_shared_secret = power(A_public, b_private, p)

    print("Shared Secrets Calculated:")
    print(f"Alice's Shared Secret (S1 = B^a mod p): {S1_shared_secret}")
    print(f"Bob's Shared Secret (S2 = A^b mod p): {S2_shared_secret}")
    print("-" * 34)

    if S1_shared_secret == S2_shared_secret:
        print(f"✅ Key Exchange SUCCESS! The Shared Secret Key is: **{S1_shared_secret}**")
    else:
        print("❌ Key Exchange FAILED!")

if __name__ == "__main__":
    diffie_hellman()
