from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag, InvalidSignature
from cryptography.hazmat.primitives import hmac, hashes


class Decryptor:
    def __init__(self, readsize=512 * 1024, iteration=200000):
        self.readsize = readsize
        self.iterations = iteration
        self.backend = default_backend()

    def _passwordkey(self, password, salt):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=self.iterations,
                         backend=self.backend)
        return kdf.derive(password)

    def _fixpath(self, filepath):
        if not filepath:
            raise ValueError("Empty file path")
        if filepath[0] == "\"" or filepath[0] == "\'":
            filepath = filepath[1:]
        if filepath[-1] == "\"" or filepath[-1] == "\'":
            filepath = filepath[:-1]
        filepath = filepath.replace("\\", "/")
        filepath = filepath.replace("\\\\", "/")
        return filepath

    def decrypt(self, file: str, password: str):

        file = self._fixpath(file)
        p = Path(file)
        filepath = p.parent
        filename = p.stem
        if p.suffix != '.enc':
            raise ValueError(f"{filename} is not encrypted. Try another file.")

        newfile = filepath / filename
        password = password.encode('utf-8')

        with open(file, "rb") as finput, open(newfile, "wb") as foutput:
            salt = finput.read(16)
            nonce = finput.read(12)
            passkey = finput.read(32)
            key = self._passwordkey(password, salt)
            h = hmac.HMAC(key, hashes.SHA256())
            h.update(salt)
            try:
                h.verify(passkey)
            except InvalidSignature:
                foutput.close()
                os.remove(newfile)
                raise ValueError("Wrong password")
            filesize = os.path.getsize(file)
            encryptedsize = filesize - 16 - 12 - 16 - 32  # total ciphertext size
            tagposition = filesize - 16
            finput.seek(tagposition)
            tag = finput.read(16)
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=self.backend)
            decryptor = cipher.decryptor()

            finput.seek(16 + 12 + 32)  # skip salt + nonce
            remaining = encryptedsize
            while remaining > 0:
                data = finput.read(min(self.readsize, remaining))
                if not data:
                    break
                originaldata = decryptor.update(data)
                foutput.write(originaldata)
                remaining = remaining - len(data)
            try:
                decryptor.finalize()
            except InvalidTag:
                foutput.close()
                os.remove(newfile)
                raise ValueError("Decryption failed: wrong password or corrupted file")

        print("Successfully decrypted")
        return newfile
