from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import os
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hmac, hashes


def passwordkey(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=200000, backend=default_backend())
    return kdf.derive(password)


def fixpath(filepath):
    if filepath[0] == "\"" or filepath[0] == "\'":
        filepath = filepath[1:]
    if filepath[-1] == "\"" or filepath[-1] == "\'":
        filepath = filepath[:-1]
    filepath = filepath.replace("\\", "/")
    filepath = filepath.replace("\\\\", "/")
    return filepath


file = input("Enter File Path: ").strip()
file = fixpath(file)

p = Path(file)
filepath = p.parent
filename = p.stem
fileextension = p.suffix
if p.suffix == '.enc':
    print(f"{filename} is already encrypted. Try another file.")
    exit(1)
newfile = filepath / (filename + fileextension + ".enc")

password = input("Password: ").encode('utf-8')

readsize = 512 * 1024  # 512 KB
nonce = os.urandom(12)
salt = os.urandom(16)

key = passwordkey(password, salt)
cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
encryptor = cipher.encryptor()

h = hmac.HMAC(key, hashes.SHA256())
h.update(salt)
passkey = h.finalize()

with open(file, "rb") as finput, open(newfile, "wb") as foutput:
    foutput.write(salt)
    foutput.write(nonce)
    foutput.write(passkey)
    while True:
        data = finput.read(readsize)  # try to read upto readsize and return it
        if not data:
            break
        ciphertext = encryptor.update(data)
        foutput.write(ciphertext)

    foutput.write(encryptor.finalize())
    foutput.write(encryptor.tag)

print("Original file size:", os.path.getsize(file))
print("Encrypted file size:", os.path.getsize(newfile))
