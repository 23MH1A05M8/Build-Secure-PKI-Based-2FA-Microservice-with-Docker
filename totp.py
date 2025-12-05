# totp.py
import time
import hmac
import hashlib
import binascii
import base64
import struct
from typing import Tuple

def hex_to_bytes(hex_seed: str) -> bytes:
    if len(hex_seed) != 64:
        raise ValueError("hex_seed must be 64 characters")
    try:
        return binascii.unhexlify(hex_seed)
    except:
        raise ValueError("hex_seed must be valid hex")

def hex_to_base32(hex_seed: str) -> str:
    b = hex_to_bytes(hex_seed)
    b32 = base64.b32encode(b).decode()
    return b32.rstrip("=")

def _hotp(key: bytes, counter: int, digits: int = 6) -> str:
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[-1] & 0x0F
    part = h[o:o+4]
    val = struct.unpack(">I", part)[0] & 0x7FFFFFFF
    return str(val % (10 ** digits)).zfill(digits)

def generate_totp_code(hex_seed: str, period: int = 30, digits: int = 6) -> str:
    key = hex_to_bytes(hex_seed)
    now = int(time.time())
    counter = now // period
    return _hotp(key, counter, digits)

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1, period: int = 30, digits: int = 6) -> bool:
    if not (code.isdigit() and len(code) == digits):
        return False

    key = hex_to_bytes(hex_seed)
    now = int(time.time())
    ctr = now // period

    for delta in range(-valid_window, valid_window + 1):
        if _hotp(key, ctr + delta, digits) == code:
            return True

    return False

def demo_sample(hex_seed: str) -> Tuple[str, str]:
    return generate_totp_code(hex_seed), hex_to_base32(hex_seed)
