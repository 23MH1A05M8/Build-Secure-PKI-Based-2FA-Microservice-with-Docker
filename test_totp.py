from totp import generate_totp_code, verify_totp_code, demo_sample

# read seed from data folder
with open("data/seed.txt", "r") as f:
    hex_seed = f.read().strip()

print("Hex seed =", hex_seed)

code = generate_totp_code(hex_seed)
print("Generated TOTP:", code)

valid = verify_totp_code(hex_seed, code)
print("Verification:", valid)

sample_code, base32_secret = demo_sample(hex_seed)
print("Base32 secret:", base32_secret)
