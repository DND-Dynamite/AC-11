import secrets

def generate_alphanumeric_string(length):
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

# Generate a 16-character random alphanumeric string
print(generate_alphanumeric_string(16))
