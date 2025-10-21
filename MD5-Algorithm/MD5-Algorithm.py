import hashlib
import hmac

class MD5SignatureAuth:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def create_signed_message(self, message):
        """Create message with MD5 signature"""
        signature = hashlib.md5(
            (message + self.secret_key).encode()
        ).hexdigest()
        
        return {
            'message': message,
            'signature': signature
        }
    
    def verify_signed_message(self, signed_message):
        """Verify MD5 signed message"""
        expected_signature = hashlib.md5(
            (signed_message['message'] + self.secret_key).encode()
        ).hexdigest()
        
        return hmac.compare_digest(
            expected_signature, 
            signed_message['signature']
        )


if __name__ == "__main__":

    """Run a small demonstration of the MD5SignatureAuth usage."""
    auth = MD5SignatureAuth("super_secret_key")

    # Create signed message
    signed_msg = auth.create_signed_message("Important transaction data")
    print(f"Signed message: {signed_msg}")

    # Verify signature
    is_authentic = auth.verify_signed_message(signed_msg)
    print(f"Authentication successful: {is_authentic}")

    # Tamper detection example
    signed_msg['message'] = "Modified transaction data"
    is_authentic_after_tamper = auth.verify_signed_message(signed_msg)
    print(f"After tampering - Authentic: {is_authentic_after_tamper}")
    print(f"New Signed message: {signed_msg}")