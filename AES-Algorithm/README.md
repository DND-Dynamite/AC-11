#   ADVANCED ENCRYPTION ALGORITHM (AES)

#   INTRODUCTION

- Advanced Encryption Standard (AES) is a highly trusted encryption algorithm used to secure data by converting it into an unreadable format without the proper key.
- It is developed by the National Institute of Standards and Technology (NIST) in 2001. 
- AES uses various key lengths (128, 192 & 256)
- This is a industry standard cryptography algorithm used to secure sensitive data and prevent cyber threats

- AES is a block cipher
- Encrypts data in blocks of 128 bits each

#   WORKING OF THE CIPHER

- AES performs operations on bytes of data rather than in bits. Since the block size is 128 bits, the cipher processes 128 bits.
- 10 rounds for 128 bits, 12 rounds for 192 bits &  14 rounds for 256 bits


- rounds keys are calculated from first key, which will be rounded to get differnet keys


#   ENCRYPTION

- AES considers 16-byte as a column major arrangement of 4byte * 4byte
- This are passed through rounds
- Each round is made up of 4 steps:
    1. SubBytes
    2. ShiftRows
    3. MixColumns
    4. Add Round Key

##   STEP1: Subbytes
- each bytes are substituted by different bytes from a lookup table called the S-box. In this way certain unqiueness of the bytes is maintained

##   STEP2: Shiftrows
- each row is shifted certain number of times.

##  STEP3: MixColumns
- This step is a  matrix multiplication, that tries to chnage the position of the byte thus the position of each byte in the coloumn is changed

##   STEP4: RoundKeys
- Now the resultant output of the previous stage is XOR-ed with the corresponding round key. Here, the 16 bytes are not considered as a grid but just as 128 bits of data

#   DECRYPTION
- The stages of each round of decryption are as follows :
    1. Add round key
    2. Inverse MixColumns
    3. ShiftRows
    4. Inverse SubByte

#   Inverse Mixcolumns
    1. This step is similar to the Mix Columns step in encryption but differs in the matrix used to carry out the operation
    2. Mix Columns Operation each column is mixed independent of the other.
    3. Matrix multiplication is used. The output of this step is the matrix multiplication of the old values and a constant matrix

#   Inverse SubBytes
- Inverse SubBytes
- Inverse S-box is used as a lookup table and using which the bytes are substituted during decryption.
- Function Substitute performs a byte substitution on each byte of the input word. For this purpose, it uses an S-box.

#   CODING KEY POINTS
- Crypto++ Library: This example uses the Crypto++ library, which you can install from its official website or package manager.
- Modes: The example uses CBC (Cipher Block Chaining) mode for encryption and decryption.
- Random Key/IV: A secure random key and initialization vector (IV) are generated using AutoSeededRandomPool
