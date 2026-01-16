from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag, InvalidSignature
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
if p.suffix != '.enc':
    print(f"{filename} is not encrypted. Try another file.")
    exit(1)
newfile = filepath / filename

password = input("Password: ").encode('utf-8')

readsize = 512 * 1024  # 512 KB

with open(file, "rb") as finput, open(newfile, "wb") as foutput:
    salt = finput.read(16)
    nonce = finput.read(12)
    passkey = finput.read(32)
    key = passwordkey(password, salt)
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(salt)
    try:
        h.verify(passkey)
    except InvalidSignature:
        print("Wrong password")
        foutput.close()
        os.remove(newfile)
        exit(1)
    filesize = os.path.getsize(file)
    encryptedsize = filesize - 16 - 12 - 16 - 32  # total ciphertext size
    tagposition = filesize - 16
    finput.seek(tagposition)
    tag = finput.read(16)
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    finput.seek(16 + 12 + 32)  # skip salt + nonce
    remaining = encryptedsize
    while remaining > 0:
        data = finput.read(min(readsize, remaining))
        if not data:
            break
        originaldata = decryptor.update(data)
        foutput.write(originaldata)
        remaining = remaining - len(data)
    try:
        decryptor.finalize()
    except InvalidTag:
        print("Decryption failed: wrong password or corrupted file")
        foutput.close()
        os.remove(newfile)
        exit(1)

print("Successfully decrypted")
