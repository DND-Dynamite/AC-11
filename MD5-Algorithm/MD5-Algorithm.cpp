#include <openssl/evp.h>
#include <openssl/err.h>
#include <string>
#include <iostream>
#include <iomanip>
#include <vector>
#include <sstream>
#include <stdexcept>

class MD5Authenticator {
private:
    std::string computeMD5(const std::string& input) {
        EVP_MD_CTX* context = EVP_MD_CTX_new();
        unsigned char hash[EVP_MAX_MD_SIZE];
        unsigned int hashLength = 0;

        if (!context) {
            throw std::runtime_error("Failed to create EVP context");
        }

        // Initialize the digest operation
        if (EVP_DigestInit_ex(context, EVP_md5(), nullptr) != 1) {
            EVP_MD_CTX_free(context);
            throw std::runtime_error("Failed to initialize digest");
        }

        // Provide the message to digest
        if (EVP_DigestUpdate(context, input.c_str(), input.length()) != 1) {
            EVP_MD_CTX_free(context);
            throw std::runtime_error("Failed to update digest");
        }

        // Finalize the digest
        if (EVP_DigestFinal_ex(context, hash, &hashLength) != 1) {
            EVP_MD_CTX_free(context);
            throw std::runtime_error("Failed to finalize digest");
        }

        EVP_MD_CTX_free(context);

        // Convert to hex string
        std::string hexHash;
        for (unsigned int i = 0; i < hashLength; i++) {
            char hex[3];
            snprintf(hex, sizeof(hex), "%02x", hash[i]);
            hexHash += hex;
        }
        return hexHash;
    }

public:
    // Generate signature for a message
    std::string generateSignature(const std::string& message, const std::string& secretKey) {
        std::string dataToSign = message + ":" + secretKey;
        return computeMD5(dataToSign);
    }

    // Verify signature
    bool verifySignature(const std::string& message, const std::string& signature, const std::string& secretKey) {
        std::string expectedSignature = generateSignature(message, secretKey);
        return (signature == expectedSignature);
    }

    // Create signed message package
    std::string createSignedMessage(const std::string& message, const std::string& secretKey) {
        std::string signature = generateSignature(message, secretKey);
        return message + "|" + signature;
    }

    // Verify and extract message from signed package
    std::pair<bool, std::string> verifySignedMessage(const std::string& signedMessage, const std::string& secretKey) {
        size_t separatorPos = signedMessage.find('|');
        if (separatorPos == std::string::npos) {
            return {false, "Invalid message format: no separator found"};
        }

        std::string message = signedMessage.substr(0, separatorPos);
        std::string receivedSignature = signedMessage.substr(separatorPos + 1);

        bool isValid = verifySignature(message, receivedSignature, secretKey);
        return {isValid, isValid ? message : "TAMPERED_MESSAGE"};
    }
};

// Utility function to demonstrate tampering
std::string tamperWithMessage(const std::string& signedMessage) {
    std::string tampered = signedMessage;
    if (tampered.length() > 5) {
        tampered[2] = 'X'; // Modify a character in the message part
    }
    return tampered;
}

// Demo function showing various scenarios
void demonstrateAuthentication() {
    MD5Authenticator authenticator;
    std::string secretKey = "MySecretKey123!";
    
    std::cout << "=== MD5 Signature Authentication Demo ===" << std::endl;
    std::cout << "Secret Key: " << secretKey << std::endl << std::endl;

    // Test Case 1: Normal successful authentication
    std::cout << "1. Normal Authentication:" << std::endl;
    std::string originalMessage = "Hello, this is a secure message!";
    std::string signedMessage = authenticator.createSignedMessage(originalMessage, secretKey);
    
    auto [isValid1, result1] = authenticator.verifySignedMessage(signedMessage, secretKey);
    std::cout << "Original Message: " << originalMessage << std::endl;
    std::cout << "Signed Package: " << signedMessage << std::endl;
    std::cout << "Verification: " << (isValid1 ? "✓ AUTHENTIC" : "✗ TAMPERED") << std::endl;
    std::cout << "Extracted Message: " << result1 << std::endl << std::endl;

    // Test Case 2: Tampered message detection
    std::cout << "2. Tampered Message Detection:" << std::endl;
    std::string tamperedMessage = tamperWithMessage(signedMessage);
    auto [isValid2, result2] = authenticator.verifySignedMessage(tamperedMessage, secretKey);
    std::cout << "Tampered Package: " << tamperedMessage << std::endl;
    std::cout << "Verification: " << (isValid2 ? "✓ AUTHENTIC" : "✗ TAMPERED") << std::endl;
    std::cout << "Result: " << result2 << std::endl << std::endl;

    // Test Case 3: Wrong secret key
    std::cout << "3. Wrong Secret Key:" << std::endl;
    std::string wrongKey = "WrongSecretKey!";
    auto [isValid3, result3] = authenticator.verifySignedMessage(signedMessage, wrongKey);
    std::cout << "Using wrong key: " << wrongKey << std::endl;
    std::cout << "Verification: " << (isValid3 ? "✓ AUTHENTIC" : "✗ TAMPERED") << std::endl;
    std::cout << "Result: " << result3 << std::endl << std::endl;

    // Test Case 4: Manual signature verification
    std::cout << "4. Manual Signature Verification:" << std::endl;
    std::string testMessage = "Manual verification test";
    std::string signature = authenticator.generateSignature(testMessage, secretKey);
    std::cout << "Message: " << testMessage << std::endl;
    std::cout << "Generated Signature: " << signature << std::endl;
    std::cout << "Manual Verify: " << (authenticator.verifySignature(testMessage, signature, secretKey) ? "✓ VALID" : "✗ INVALID") << std::endl << std::endl;

    // Test Case 5: Empty message
    std::cout << "5. Empty Message:" << std::endl;
    std::string emptyMsg = "";
    std::string emptySigned = authenticator.createSignedMessage(emptyMsg, secretKey);
    auto [isValid5, result5] = authenticator.verifySignedMessage(emptySigned, secretKey);
    std::cout << "Empty Message Package: " << emptySigned << std::endl;
    std::cout << "Verification: " << (isValid5 ? "✓ AUTHENTIC" : "✗ TAMPERED") << std::endl;
    std::cout << "Extracted Message: '" << result5 << "'" << std::endl << std::endl;
}

// Function to simulate real-world usage
void simulateRealWorldScenario() {
    std::cout << "=== Real-World Simulation ===" << std::endl;
    
    MD5Authenticator auth;
    std::string apiSecret = "APISecret2024!";
    
    // Simulate API request
    std::string apiRequest = "GET /api/users?page=1&limit=10";
    std::string timestamp = "2024-01-15T10:30:00Z";
    std::string requestData = apiRequest + "&timestamp=" + timestamp;
    
    // Generate signature for API request
    std::string signature = auth.generateSignature(requestData, apiSecret);
    
    std::cout << "API Request Simulation:" << std::endl;
    std::cout << "Request: " << requestData << std::endl;
    std::cout << "Signature: " << signature << std::endl;
    
    // Verify on server side
    bool isValid = auth.verifySignature(requestData, signature, apiSecret);
    std::cout << "Server Verification: " << (isValid ? "✓ REQUEST AUTHENTIC" : "✗ REQUEST TAMPERED") << std::endl;
    
    // Simulate tampered request
    std::string tamperedRequest = "GET /api/users?page=1&limit=100&timestamp=2024-01-15T10:30:00Z";
    bool isTamperedValid = auth.verifySignature(tamperedRequest, signature, apiSecret);
    std::cout << "Tampered Request Verification: " << (isTamperedValid ? "✓ REQUEST AUTHENTIC" : "✗ REQUEST TAMPERED") << std::endl;
}

int main() {
    try {
        demonstrateAuthentication();
        std::cout << std::string(50, '=') << std::endl;
        simulateRealWorldScenario();
        
        std::cout << std::endl << "=== Security Note ===" << std::endl;
        std::cout << "MD5 is cryptographically broken and should not be used" << std::endl;
        std::cout << "for security-sensitive applications in production." << std::endl;
        std::cout << "This demo is for educational purposes only." << std::endl;
        std::cout << "Use SHA-256 or better for real applications." << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
