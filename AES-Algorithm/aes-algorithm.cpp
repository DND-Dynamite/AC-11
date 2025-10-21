#include <iostream>
#include <string>
#include <cryptopp/aes.h>
#include <cryptopp/filters.h>
#include <cryptopp/hex.h>
#include <cryptopp/modes.h>
#include <cryptopp/osrng.h>

using namespace CryptoPP;

int main() {
    // Input data
    std::string plainText = "Hello, AES Encryption!";
    std::string cipherText, decryptedText;

    // Generate a random key and IV
    SecByteBlock key(AES::DEFAULT_KEYLENGTH);
    SecByteBlock iv(AES::BLOCKSIZE);
    AutoSeededRandomPool prng;
    prng.GenerateBlock(key, key.size());
    prng.GenerateBlock(iv, iv.size());

    try {
        // Encryption
        CBC_Mode<AES>::Encryption encryptor(key, key.size(), iv);
        StringSource(plainText, true,
            new StreamTransformationFilter(encryptor,
                new StringSink(cipherText)
            )
        );

        // Decryption
        CBC_Mode<AES>::Decryption decryptor(key, key.size(), iv);
        StringSource(cipherText, true,
            new StreamTransformationFilter(decryptor,
                new StringSink(decryptedText)
            )
        );

        // Output results
        std::cout << "Plaintext: " << plainText << std::endl;
        std::cout << "Ciphertext (Hex): ";
        StringSource(cipherText, true, new HexEncoder(new FileSink(std::cout)));
        std::cout << std::endl;
        std::cout << "Decrypted Text: " << decryptedText << std::endl;

    } catch (const Exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}

