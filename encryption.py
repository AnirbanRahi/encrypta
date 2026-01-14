from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import os
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


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

password = input("Password: ").encode('utf-8')

readsize = 512 * 1024  # 512 KB
nonce = os.urandom(12)
salt = os.urandom(16)

key = passwordkey(password, salt)
cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
encryptor = cipher.encryptor()

p = Path(file)
filepath = p.parent
filename = p.stem
fileextension = p.suffix
newfile = filepath / (filename + ".enc")
print(filepath)
print(filename)
print(fileextension)

with open(file, "rb") as finput, open(newfile, "wb") as foutput:
    foutput.write(salt)
    foutput.write(nonce)
    while True:
        data = finput.read(readsize)  # try to read upto readsize and return it
        if not data:
            break
        ciphertext = encryptor.update(data)
        foutput.write(ciphertext)
        # binary_str = ''.join(f'{byte:08b}' for byte in data)
        # f'{value:specific_format}', 08b b means binary with 8 bit with zero leading(left)
        # print(binary_str)
    encryptor.finalize()
    foutput.write(encryptor.tag)
    print("Authentication Key: " + encryptor.tag.hex())
