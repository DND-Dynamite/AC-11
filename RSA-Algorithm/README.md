\# RSA Algorithm in cryptography



\## Introduction



* RSA(Rivest-Shamir-Adleman) Algorithm is an asymmetric or public-key cryptography algorithm which means it works on two different keys: Public Key and Private Key. 
* The Public Key is used for encryption and is known to everyone, while the Private Key is used for decryption and must be kept secret by the receiver. 
* RSA Algorithm is named after Ron Rivest, Adi Shamir and Leonard Adleman, who published the algorithm in 1977.



\## RSA Algorithm



RSA Algorithm is based on factorization of large number and modular arithmetic for encrypting and decrypting data. It consists of three main stages:



* Key Generation: Creating Public and Private Keys
* Encryption: Sender encrypts the data using Public Key to get cipher text.
* Decryption: Decrypting the cipher text using Private Key to get the original data.





1\. Key Generation



Choose two large prime numbers, say p and q. These prime numbers should be kept secret.

Calculate the product of primes, n = p \* q. This product is part of the public as well as the private key.

Calculate Euler Totient FunctionΦ(n) as Φ(n) = Φ(p \* q) = Φ(p) \* Φ(q) = (p - 1) \* (q - 1).

Choose encryption exponent e, such that

1 < e < Φ(n), and

gcd(e, Φ(n)) = 1, that is e should be co-prime with Φ(n).

Calculate decryption exponent d, such that

(d \* e) ≡ 1 mod Φ(n), that is d is modular multiplicative inverse of e mod Φ(n). Some common methods to calculate multiplicative inverse are: Extended Euclidean Algorithm, Fermat's Little Theorem, etc.

We can have multiple values of d satisfying (d \* e) ≡ 1 mod Φ(n) but it does not matter which value we choose as all of them are valid keys and will result into same message on decryption.

Finally, the Public Key = (n, e) and the Private Key = (n, d).



2\. Encryption



To encrypt a message M, it is first converted to numerical representation using ASCII and other encoding schemes. Now, use the public key (n, e) to encrypt the message and get the cipher text using the formula:



C = Me mod n, where C is the Cipher text and e and n are parts of public key.



3\. Decryption



To decrypt the cipher text C, use the private key (n, d) and get the original data using the formula:



M = Cd mod n, where M is the message and d and n are parts of private key.



\## Idea behind RSA Algorithm



* The idea of RSA is based on the fact that it is difficult to factorize a large integer. The Public Key is (n, e), where n and e are publicly known, while the Private Key is (n, d). Since only the receiver knows the value of d, only they can decrypt the message. But is it possible to find the value of d using n and e?



* We know that (d \* e) ≡ 1 mod Φ(n), so if we can calculate the value of Φ(n), we can find the value of d. But Φ(n) = (p - 1) \* (q - 1). So, we need the value of p and q. Now, one might think that it's quite easy to find the value of p and q as n = p \* q and n is already publicly known but RSA Algorithm takes the value of p and q to be very large which in turn makes the value of n extremely large and factorizing such a large value is computationally impossible.



* Therefore encryption strength lies in the values of p and q. RSA keys can be typically 1024 or 2048 bits long, but experts believe that 1024-bit keys could be broken shortly. But till now it seems to be an infeasible task.



Note: If someone gets to know the value of p and q, then he can calculate the value of d and decrypt the message.





\## Advantages

* Security: RSA algorithm is considered to be very secure and is widely used for secure data transmission.
* Public-key cryptography: RSA algorithm is a public-key cryptography algorithm, which means that it uses two different keys for encryption and decryption. The public key is used to encrypt the data, while the private key is used to decrypt the data.
* Key exchange: RSA algorithm can be used for secure key exchange, which means that two parties can exchange a secret key without actually sending the key over the network.
* Digital signatures: RSA algorithm can be used for digital signatures, which means that a sender can sign a message using their private key, and the receiver can verify the signature using the sender's public key.
* Widely used: Online banking, e-commerce, and secure communications are just a few fields and applications where the RSA algorithm is extensively developed.



\## Disadvantages

* Slow processing speed: RSA algorithm is slower than other encryption algorithms, especially when dealing with large amounts of data.
* Large key size: RSA algorithm requires large key sizes to be secure, which means that it requires more computational resources and storage space.
* Vulnerability to side-channel attacks: RSA algorithm is vulnerable to side-channel attacks, which means an attacker can use information leaked through side channels such as power consumption, electromagnetic radiation, and timing analysis to extract the private key.
* Limited use in some applications: RSA algorithm is not suitable for some applications, such as those that require constant encryption and decryption of large amounts of data, due to its slow processing speed.
* Complexity: The RSA algorithm is a sophisticated mathematical technique that some individuals may find challenging to comprehend and use.
* Key Management: The secure administration of the private key is necessary for the RSA algorithm, although in some cases this can be difficult.
* Vulnerability to Quantum Computing: Quantum computers have the ability to attack the RSA algorithm, potentially decrypting the data.







\## RSA and Digital Signature



* RSA and digital signatures are crucial elements in modern cybersecurity. RSA, a widely used encryption algorithm, ensures secure data transmission by encrypting and decrypting information. Digital signatures, on the other hand, authenticate the identity of the sender and guarantee the integrity of the message. 
* Together, RSA and digital signatures provide a robust framework for secure communication, protecting sensitive data from unauthorized access and ensuring that messages are not tampered with during transmission.





\## What is Digital Signature?



* As the name sounds are the new alternative to signing a document digitally. It ensures that the message is sent by the intended user without any tampering by any third party (attacker). In simple words, digital signatures are used to verify the authenticity of the message sent electronically.
* Digital signatures authenticate the identity of the sender and guarantee the integrity of the message. By using a private key to create a unique signature and a public key to verify it, digital signatures ensure that messages are not tampered with during transmission. This technology is vital for ensuring trust and security in various online transactions and communications, making it an indispensable tool in modern cybersecurity.



\## RSA Signature Scheme





* Step 1: Sender A uses the SHA-1 Message Digest Algorithm to calculate the message digest (MD1) over the original message M.

![](image.png)

* Step 2 : A now encrypts the message digest with its private key. The output of this process is called Digital Signature (DS) of A.

* Step 3 : Now sender A sends the digital signature (DS) along with the original message (M) to B.


* Step 4 : When B receives the Original Message(M) and the Digital Signature(DS) from A, it first uses the same message-digest algorithm as was used by A and calculates its own Message Digest (MD2) for M.

* Step 5 : Now B uses A's public key to decrypt the digital signature because it was encrypted by A's private key. The result of this process is the original Message Digest (MD1) which was calculated by A.


* Step-6 : If MD1==MD2, the following facts are established as follows.
B accepts the original message M as the correct, unaltered message from A.

![alt text](graph.png)