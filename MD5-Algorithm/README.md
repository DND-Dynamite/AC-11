# Authenticating signature using MD5 Hash Algorithm

## Issues faced when trying to implement MD5-Algorithm in cpp

- Had to install openssl library for md5.h header file, using command ```bash sudo apt install libssl-dev```
- Deprecation Warning (MD5 function deprecated since OpenSSL 3.0): OpenSSL 3.0 removed the legacy MD5 API and deprecated it.
  This is safe for now but you should update to modern APIs if you plan to maintain the code long-term.
- In earlier code from resources std::hex and used += operator which throwed error as it is not a string but a hex, needed to use std::string
- Changed compilation command to include the openssl libraries and their header files
  ```bash g++ -I/usr/include/openssl -o MD5-Algorithm MD5-Algorithm.cpp -L/usr/lib -lcrypto```
- Since we are used openssl 3.0+ version which has deprycated low level MD5 function. Here are 2 ways to resolve, the one i used is EVP Interface
### Advantages
  - Forward compatibility: EVP interface is the modern OpenSSL API
  - Consistency: Same pattern works for other hash algorithms (SHA1, SHA256, etc.)
  - Better error handling: More robust error checking
  - Security: Follows OpenSSL best practices

### Conclusion
- Included all real world examples and test cases
