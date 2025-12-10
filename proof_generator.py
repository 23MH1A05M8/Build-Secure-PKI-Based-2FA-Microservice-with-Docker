#!/usr/bin/env python3

import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


# Helper: Load private key
def load_private_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )


# Helper: Load public key
def load_public_key(path: str):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )


# Function 1: Sign message using RSA-PSS-SHA256
def sign_message(message: str, private_key) -> bytes:
    """
    Sign commit hash string (ASCII) using RSA-PSS-SHA256.
    """
    message_bytes = message.encode("utf-8") 

    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256()
    )

    return signature


# Function 2: Encrypt signature using RSA-OAEP-SHA256
def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """
    Encrypt signature bytes using RSA-OAEP-SHA256.
    """
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted


# MAIN SCRIPT
def main():

    # 1. Replace with your real commit hash
    commit_hash = "a4ea32e6decf400a2d18f259ebd4f1ac17883430"  

    # 2. Load student private key
    student_private = load_private_key("student_private.pem")

    # 3. Sign commit hash
    signature = sign_message(commit_hash, student_private)

    # 4. Load instructor public key
    instructor_public = load_public_key("instructor_public.pem")

    # 5. Encrypt the signature
    encrypted_signature = encrypt_with_public_key(signature, instructor_public)

    # 6. Base64 encode
    encrypted_b64 = base64.b64encode(encrypted_signature).decode()

    print("\n==============================")
    print(" Commit Proof Generated")
    print("==============================")
    print(f"Commit Hash: {commit_hash}")
    print(f"Encrypted Signature: {encrypted_b64}\n")


if __name__ == "__main__":
    main()