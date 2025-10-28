# Diffie Helman Key Exchange Algorithm

The Diffie-Hellman (DH) key exchange algorithm is a method for two parties to securely establish a shared secret key over an insecure channel without exchanging the key itself. It uses public key cryptography and relies on the mathematical difficulty of the discrete logarithm problem. The process involves agreeing on public parameters, each party choosing a private key and calculating a public key, and then exchanging public keys to derive the same shared secret key privately.

## How it works 

1. Agree on public parameters: Two parties, say Alice and Bob, agree on a large prime number () and a generator (), which are publicly known. 
2. Choose private keys: Alice chooses a secret integer  and Bob chooses a secret integer . 
3. Calculate public keys: 

	• Alice calculates her public key . 
	• Bob calculates his public key . 

4. Exchange public keys: Alice sends  to Bob, and Bob sends  to Alice. An eavesdropper can see these public keys but cannot easily use them to find the private keys. 
5. Compute the shared secret: 

	• Alice computes the shared secret by using Bob's public key: . 
	• Bob computes the shared secret by using Alice's public key: . 

6. Result: Since  is the same as , both Alice and Bob arrive at the same shared secret (), which can then be used for symmetric encryption.

<img width="764" height="350" alt="image" src="https://github.com/user-attachments/assets/8522a0be
