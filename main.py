# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import base64
import time
import hmac
import hashlib
import binascii
import struct

app = FastAPI(title="PKI-Based 2FA Microservice")

# --- TOTP Functions ---
def hex_to_bytes(hex_seed: str) -> bytes:
    if len(hex_seed) != 64:
        raise ValueError("hex_seed must be 64 characters")
    return binascii.unhexlify(hex_seed)

def _hotp(key: bytes, counter: int, digits: int = 6) -> str:
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[-1] & 0x0F
    val = struct.unpack(">I", h[o:o+4])[0] & 0x7FFFFFFF
    return str(val % (10 ** digits)).zfill(digits)

def generate_totp_code(hex_seed: str, period: int = 30, digits: int = 6) -> str:
    key = hex_to_bytes(hex_seed)
    counter = int(time.time()) // period
    return _hotp(key, counter, digits)

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1, period: int = 30, digits: int = 6) -> bool:
    if not (code.isdigit() and len(code) == digits):
        return False
    key = hex_to_bytes(hex_seed)
    counter = int(time.time()) // period
    for delta in range(-valid_window, valid_window + 1):
        if _hotp(key, counter + delta, digits) == code:
            return True
    return False

# --- Request Models ---
class SeedRequest(BaseModel):
    encrypted_seed: str

class CodeRequest(BaseModel):
    code: str

# --- Load decrypted seed initially ---
try:
    with open("data/seed.txt", "r") as f:
        decrypted_seed = f.read().strip()
except FileNotFoundError:
    decrypted_seed = None

# --- Endpoints ---
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(request: SeedRequest):
    try:
        # Load private key
        with open("student_private.pem", "r") as f:
            private_key = RSA.import_key(f.read())
        cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        # Base64 decode
        encrypted_bytes = base64.b64decode(request.encrypted_seed)
        # Decrypt
        decrypted_bytes = cipher_rsa.decrypt(encrypted_bytes)
        seed = decrypted_bytes.decode("utf-8")
        # Validate
        if len(seed) != 64:
            raise ValueError("Decrypted seed must be 64 characters")
        global decrypted_seed
        decrypted_seed = seed
        # Save to file
        import os
        os.makedirs("data", exist_ok=True)
        with open("data/seed.txt", "w") as f:
            f.write(seed)
        return {"decrypted_seed": seed}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

@app.get("/totp")
def get_totp():
    if not decrypted_seed:
        raise HTTPException(status_code=400, detail="Seed not available. Decrypt first.")
    code = generate_totp_code(decrypted_seed)
    return {"totp": code}

@app.post("/verify")
def verify_code(request: CodeRequest):
    if not decrypted_seed:
        raise HTTPException(status_code=400, detail="Seed not available. Decrypt first.")
    valid = verify_totp_code(decrypted_seed, request.code)
    return {"valid": valid, "message": "Code is valid" if valid else "Code is invalid"}
