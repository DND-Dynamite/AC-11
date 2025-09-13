#include <bits/stdc++.h>
using namespace std;

// Global variables
string plain_text = "001010010010";
string key = "101001000001";
int n = 3;
vector<int> pt, key_list, key_stream, cipher_text,
    original_text;

// Function to convert binary string to decimal
int binaryToDecimal(string binary)
{
    int decimal = 0;
    int base = 1;
    for (int i = binary.size() - 1; i >= 0; i--) {
        if (binary[i] == '1')
            decimal += base;
        base = base * 2;
    }
    return decimal;
}

// Function to convert decimal to binary string
string decimalToBinary(int decimal)
{
    string binary = "";
    while (decimal > 0) {
        binary = (decimal % 2 == 0 ? "0" : "1") + binary;
        decimal /= 2;
    }
    while (binary.size() < n)
        binary = "0" + binary;
    return binary;
}

// Function to perform KSA
void KSA(vector<int>& S)
{
    int j = 0;
    int N = S.size();
    for (int i = 0; i < N; i++) {
        j = (j + S[i] + key_list[i]) % N;
        swap(S[i], S[j]);
        cout << i << "  ";
        for (int s : S)
            cout << s << " ";
        cout << endl;
    }
    cout << "\nThe initial permutation array is : ";
    for (int s : S)
        cout << s << " ";
    cout << endl;
}

// Function to perform PRGA
void PRGA(vector<int>& S)
{
    int N = S.size();
    int i = 0, j = 0;
    for (int k = 0; k < pt.size(); k++) {
        i = (i + 1) % N;
        j = (j + S[i]) % N;
        swap(S[i], S[j]);
        int t = (S[i] + S[j]) % N;
        key_stream.push_back(S[t]);
        cout << k << "  ";
        for (int s : S)
            cout << s << " ";
        cout << endl;
    }
    cout << "Key stream : ";
    for (int ks : key_stream)
        cout << ks << " ";
    cout << endl;
}

// Function to perform XOR
void XOR(vector<int>& text, vector<int>& key_stream)
{
    for (int i = 0; i < text.size(); i++) {
        int result = key_stream[i] ^ text[i];
        text[i] = result;
    }
}

// Function for encryption
void encryption()
{
    // Convert plain_text and key to decimal
    for (int i = 0; i < plain_text.size(); i += n) {
        pt.push_back(
            binaryToDecimal(plain_text.substr(i, n)));
        key_list.push_back(
            binaryToDecimal(key.substr(i, n)));
    }

    // Initialize state vector array
    vector<int> S(pow(2, n));
    iota(S.begin(), S.end(), 0);

    // Perform KSA
    KSA(S);

    // Perform PRGA
    PRGA(S);

    // Perform XOR
    XOR(pt, key_stream);

    // Convert encrypted text to bits form
    cipher_text = pt;
}

// Function for decryption
void decryption()
{
    // Initialize state vector array
    vector<int> S(pow(2, n));
    iota(S.begin(), S.end(), 0);

    // Perform KSA
    KSA(S);

    // Perform PRGA
    PRGA(S);

    // Perform XOR
    XOR(cipher_text, key_stream);

    // Convert decrypted text to bits form
    original_text = cipher_text;
}

int main()
{
    cout << "Plain text :  " << plain_text << endl;
    cout << "Key :  " << key << endl;
    cout << "n :  " << n << endl;
    cout << "\nS :  ";
    for (int i = 0; i < pow(2, n); i++)
        cout << i << " ";
    cout << endl;
    cout << "Plain text ( in array form ):  ";
    for (int i = 0; i < plain_text.size(); i += n)
        cout << binaryToDecimal(plain_text.substr(i, n))
             << " ";
    cout << endl;
    cout << "Key list :  ";
    for (int i = 0; i < key.size(); i += n)
        cout << binaryToDecimal(key.substr(i, n)) << " ";
    cout << endl;

    cout << "\nKSA iterations : \n";
    encryption();
    cout << "\nCipher text : ";
    for (int i : cipher_text)
        cout << decimalToBinary(i);
    cout << endl;

    cout << "\n--------------------------------------------"
            "-------------\n";

    cout << "\nKSA iterations : \n";
    decryption();
    cout << "\nDecrypted text : ";
    for (int i : original_text)
        cout << decimalToBinary(i);
    cout << endl;

    return 0;
}