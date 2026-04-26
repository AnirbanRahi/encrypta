import hashlib
import zipfile

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidTag


class Decryptor:
    def __init__(self, readsize=512 * 1024, iteration=200000):
        self.readsize = readsize
        self.iterations = iteration
        self.backend = default_backend()

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

        is_dir = filename.endswith(".dir")
        if is_dir:
            filename = filename[:-4]
            newfile = filepath / (filename + ".zip")
        else:
            newfile = filepath / filename
        try:
            with open(file, "rb") as finput, open(newfile, "wb") as foutput:
                salt = finput.read(16)
                nonce = finput.read(12)
                stored_verifier = finput.read(16)
                password = password.encode('utf-8')

                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=self.iterations,
                    backend=self.backend
                )
                keybytes = kdf.derive(password)

                expected = hashlib.sha256(keybytes).digest()[:16]
                if expected != stored_verifier:
                    raise ValueError("Wrong password")

                filesize = os.path.getsize(file)
                encryptedsize = filesize - 16 - 12 - 16 - 16  # total ciphertext size
                tagposition = filesize - 16
                finput.seek(tagposition)
                tag = finput.read(16)
                cipher = Cipher(algorithms.AES(keybytes), modes.GCM(nonce, tag), backend=self.backend)
                decryptor = cipher.decryptor()

                finput.seek(16 + 12 + 16)
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
                    os.remove(newfile)
                    raise ValueError("Decryption failed: wrong password or corrupted file")
        except Exception as e:
            if newfile.exists():
                try:
                    os.remove(newfile)
                except:
                    pass
            raise e

        if is_dir:
            foldername = filepath / filename
            with zipfile.ZipFile(newfile, "r") as zip_ref:
                zip_ref.extractall(foldername)
            os.remove(newfile)
            os.remove(file)
            return foldername
        else:
            os.remove(file)
            return newfile
