from crypto_utils import load_private_key, decrypt_seed

private_key = load_private_key("student_private.pem")

encrypted_seed = """
QF9G/V0R85LNZC6g5W1WqbQk9i2oDX7d/Evram+Jb0LY7RNNETkIHMNvRBUYTw9Nc77l/6DabzMp4iz4ma7Nm+1+A2Y3QCAVxWO2m0b2T5WeDkMOJiAMD0ACIEJjBsuut1Ie6IzLkd+c30w7+MTFv4w0tUW0SUu1rHmlMGCExiaQjOEpASS5yFJ8hqZKLMK1BcaFFSw6Lkt6lVsIvueBwWSX5+hOEDgKtYxXz280da737AVzyTVhCGjp4+u3ZWA/YRyV9xmiNn+cxaJKzg209NFoIUZrPZO7aksBTaWfnr6Hlb2p5DxPEfPbGcsu4nlB+LLlsH1QkXey/kwohDB3RA/KCcgn44O2uwvn20wd2d8gz7kYazIn5UgbvgIE+iCl1FPvMQPfVecNGmkbbR/UGUWeBe3h0hxVFw14cw6UcsOQAbt0d39LDA6x4GMfJbbF5KymCwRnAISAgRhLjdU7gU9KezQ2RsFG0o+0GCP1wEinLRBlYpDYD83nCn76BZZghQGC8D5kccvu9tUDQ/wet9xNkePaEyMj+Kty5nfqI9USUGkkcJnZHrMhPTLF6L7sh3mVBSgSK2v/EaaedcyMcr7bMF2VyqAY5/bD3W0PRzd0dR/aiNxLPBu0Qh5UX9D/WOLMyJZersH5u2jCJUCXB0YbyMEgVk8B2YhbUXThNjI=
"""

encrypted_seed = encrypted_seed.strip()

try:
    seed = decrypt_seed(encrypted_seed, private_key)
    print("Decrypted seed:", seed)
except Exception as e:
    print("Error:", e)