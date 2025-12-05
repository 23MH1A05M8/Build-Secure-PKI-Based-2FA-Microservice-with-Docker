# request_seed.py
import requests
import json

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
STUDENT_ID = "23MH1A05M8"  # replace with your student id

def read_pubkey():
    with open("student_public.pem", "r") as f:
        return f.read()

def request_seed(student_id, github_repo_url):
    pubkey = read_pubkey()
    payload = {
        "student_id": "23MH1A05M8" ,
        "github_repo_url": "https://github.com/23MH1A05M8/Build-Secure-PKI-Based-2FA-Microservice-with-Docker" ,
        "public_key": pubkey  # HTTP libraries preserve line breaks
    }
    r = requests.post(API_URL, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "success":
        raise RuntimeError("Instructor API error: " + str(data))
    enc = data["encrypted_seed"]
    with open("encrypted_seed.txt", "w") as f:
        f.write(enc)
    print("Encrypted seed saved to encrypted_seed.txt")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 request_seed.py <github_repo_url>")
        sys.exit(1)
    repo_url = sys.argv[1]
    request_seed("23MH1A05M8", "https://github.com/23MH1A05M8/Build-Secure-PKI-Based-2FA-Microservice-with-Docker")
