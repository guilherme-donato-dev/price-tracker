import secrets

def generate_secret_key(length=32):
    """Gera uma chave secreta segura em formato hexadecimal."""
    return secrets.token_hex(length)

if __name__ == "__main__":
    key = generate_secret_key()
    print(f"Sua nova chave secreta: {key}")
