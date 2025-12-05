#!/usr/bin/env python3
import time
import hmac
import hashlib
import struct
import base64
from datetime import datetime

# 1. Read hex seed from /data/seed.txt
seed_file = '/data/seed.txt'
try:
    with open(seed_file, 'r') as f:
        hex_seed = f.read().strip()
except FileNotFoundError:
    print(f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} - Seed file not found")
    exit(1)

# Convert hex → bytes
seed_bytes = bytes.fromhex(hex_seed)

# 2. TOTP setup
time_step = 30
t = int(time.time() // time_step)

# Convert counter to 8-byte big-endian
counter = struct.pack(">Q", t)

# 3. HMAC-SHA1
hmac_hash = hmac.new(seed_bytes, counter, hashlib.sha1).digest()

# 4. Dynamic Truncation (RFC 4226)
offset = hmac_hash[-1] & 0x0F
code = (
    ((hmac_hash[offset] & 0x7F) << 24) |
    ((hmac_hash[offset+1] & 0xFF) << 16) |
    ((hmac_hash[offset+2] & 0xFF) << 8) |
    (hmac_hash[offset+3] & 0xFF)
)

# 6-digit TOTP
totp_code = code % 1000000

# Print result
timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
print(f"{timestamp} - 2FA Code: {totp_code:06d}")
