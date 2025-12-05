import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


def decrypt_seed(encrypted_seed_b64: str, private_key_path="student_private.pem") -> str:
    # Read private key
    with open(private_key_path, "r") as f:
        priv_key = RSA.import_key(f.read())

    # Base64 decode ciphertext
    ciphertext = base64.b64decode(encrypted_seed_b64)

    # Configure RSA OAEP with SHA-256
    cipher = PKCS1_OAEP.new(
        key=priv_key,
        hashAlgo=SHA256
    )

    # Decrypt
    decrypted = cipher.decrypt(ciphertext)

    # Convert bytes to string
    seed = decrypted.decode("utf-8")

    # Validation
    if len(seed) != 64:
        raise ValueError("Seed must be 64 characters")

    for c in seed:
        if c not in "0123456789abcdef":
            raise ValueError("Seed contains invalid hex characters")

    return seed


if __name__ == "__main__":
    # read encrypted_seed.txt
    with open("encrypted_seed.txt", "r") as f:
        encrypted_b64 = f.read().strip()

    seed = decrypt_seed(encrypted_b64)
    print("Decrypted seed:", seed)

    # Save to data folder
    import os
    os.makedirs("data", exist_ok=True)

    with open("data/seed.txt", "w") as f:
        f.write(seed)

    print("Saved to data/seed.txt")
